#!/usr/bin/env python3
"""
KingKira Group — shared data-model validator.

Checks the synthetic datasets under docs/data/ against schema v0.1:
  * ID formats + uniqueness for every entity PK
  * referential integrity across domains (the joins actually resolve)
  * enum conformance (service_line / site / statuses)         [warnings]
  * booking-calendar sanity: crew tallies + no resource double-booking [warnings]

ERRORS fail the build (exit 1). WARNINGS are reported but do not fail, so the
team can iterate on synthetic data without a red build for soft issues.

Pure stdlib; runs on GitHub Actions (ubuntu has python3). No local deps.
"""
import json, re, sys, os, glob
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "docs", "data")

ERRORS, WARNINGS = [], []
def err(m):  ERRORS.append(m)
def warn(m): WARNINGS.append(m)

ID_RE = {
    "customer": re.compile(r"^CUST-\d{3}$"),
    "sale":     re.compile(r"^SALE-\d{4}$"),
    "asset":    re.compile(r"^KK-[A-Z]{2}-\d{3}$"),
    "employee": re.compile(r"^EMP-\d{3}$"),
    "job":      re.compile(r"^JOB-\d{4}$"),
}
SERVICE_LINES = {"Industrial", "Environmental", "Recruitment"}  # billable delivery lines (sale + job)
# Employees may also be overhead/shared-services staff (schema §2): 'Corporate'
# is valid for the employee entity only, never for a sale or job.
EMPLOYEE_SERVICE_LINES = SERVICE_LINES | {"Corporate"}
SITES = {"Perth - Applecross", "Pilbara - Newman", "Pilbara - Tom Price", "Pilbara - Karratha"}
ASSET_STATUS = {"Operational", "Maintenance", "Standby"}
JOB_STATUS = {"Scheduled", "In Progress", "Completed", "Cancelled"}

def load(rel):
    path = os.path.join(DATA, rel)
    if not os.path.exists(path):
        warn(f"{rel}: file not found — skipping its checks")
        return None
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        err(f"{rel}: invalid JSON — {e}")
        return None

def rows(obj, *keys):
    """Normalise a dataset that may be a bare list or wrapped under a key."""
    if obj is None:
        return []
    if isinstance(obj, list):
        return obj
    for k in keys:
        if isinstance(obj.get(k), list):
            return obj[k]
    # fall back to first list value found
    for v in obj.values():
        if isinstance(v, list):
            return v
    return []

def check_ids(items, kind, pk):
    seen = set()
    ok = []
    for i, it in enumerate(items):
        v = it.get(pk)
        if v is None:
            err(f"{kind}[{i}]: missing {pk}")
            continue
        if not ID_RE[kind].match(str(v)):
            err(f"{kind} {v}: bad id format (expected {ID_RE[kind].pattern})")
        if v in seen:
            err(f"{kind} {v}: duplicate {pk}")
        seen.add(v)
        ok.append(it)
    return seen, ok

def parse_d(s):
    try:
        y, m, d = map(int, s.split("-"))
        return date(y, m, d)
    except Exception:
        return None

def overlaps(a1, a2, b1, b2):
    return a1 <= b2 and b1 <= a2

def main():
    print("KingKira data-model validator — schema v0.1\n" + "-" * 46)

    customers = rows(load("sales/customers.json"), "customers")
    sales     = rows(load("sales/sales.json"), "sales")
    assets    = rows(load("fleet/asset_register.json"), "assets")
    employees = rows(load("workforce/employees.json"), "employees")
    jobs      = rows(load("workforce/bookings.json"), "jobs")

    cust_ids, _ = check_ids(customers, "customer", "customer_id")
    sale_ids, sale_ok = check_ids(sales, "sale", "sale_id")
    asset_ids, _ = check_ids(assets, "asset", "asset_id")
    emp_ids, _ = check_ids(employees, "employee", "employee_id")
    job_ids, job_ok = check_ids(jobs, "job", "job_id")

    sale_by_id = {s["sale_id"]: s for s in sales if s.get("sale_id")}

    # --- Sales FK + enums ---
    for s in sales:
        sid = s.get("sale_id", "?")
        if s.get("customer_id") not in cust_ids:
            err(f"sale {sid}: customer_id {s.get('customer_id')!r} not in customers")
        if s.get("service_line") not in SERVICE_LINES:
            warn(f"sale {sid}: service_line {s.get('service_line')!r} not in {sorted(SERVICE_LINES)}")
        rn = s.get("resource_needs") or {}
        for cat in rn.get("asset_categories", []):
            if not re.match(r"^[A-Z]{2}$", str(cat)):
                warn(f"sale {sid}: asset_category {cat!r} is not a 2-letter CAT code")

    # --- Asset enums ---
    for a in assets:
        if a.get("status") not in ASSET_STATUS:
            warn(f"asset {a.get('asset_id')}: status {a.get('status')!r} not in {sorted(ASSET_STATUS)}")
        if a.get("site") not in SITES:
            warn(f"asset {a.get('asset_id')}: site {a.get('site')!r} not in known sites")

    # --- Employee enums ---
    for e in employees:
        if e.get("service_line") not in EMPLOYEE_SERVICE_LINES:
            warn(f"employee {e.get('employee_id')}: service_line {e.get('service_line')!r} unexpected")
        if e.get("site") not in SITES:
            warn(f"employee {e.get('employee_id')}: site {e.get('site')!r} not in known sites")

    # --- Jobs (the calendar): the core cross-domain joins ---
    for j in jobs:
        jid = j.get("job_id", "?")
        sid = j.get("sale_id")
        if sid not in sale_ids:
            err(f"job {jid}: sale_id {sid!r} not in sales")
        else:
            s = sale_by_id[sid]
            if s.get("stage") != "Won":
                warn(f"job {jid}: delivers sale {sid} whose stage is {s.get('stage')!r} (expected Won)")
            if j.get("customer_id") and j["customer_id"] != s.get("customer_id"):
                warn(f"job {jid}: customer_id {j['customer_id']} != sale's {s.get('customer_id')}")
        for aid in j.get("asset_ids", []):
            if aid not in asset_ids:
                err(f"job {jid}: asset_id {aid!r} not in asset register")
        for eid in j.get("employee_ids", []):
            if eid not in emp_ids:
                err(f"job {jid}: employee_id {eid!r} not in employees")
        if j.get("status") not in JOB_STATUS:
            warn(f"job {jid}: status {j.get('status')!r} not in {sorted(JOB_STATUS)}")
        # crew tally sanity
        cb, cr = j.get("crew_booked"), j.get("crew_required")
        if cb is not None and len(j.get("employee_ids", [])) != cb:
            warn(f"job {jid}: crew_booked={cb} but {len(j.get('employee_ids', []))} employee_ids listed")
        if cb is not None and cr is not None and j.get("shortfall") not in (None, cr - cb):
            warn(f"job {jid}: shortfall={j.get('shortfall')} != crew_required-crew_booked ({cr - cb})")

    # --- Resource double-booking (schema §3: no overlap on two jobs) ---
    # Pooled assets (e.g. the shared light-vehicle pool) are exempt: crews draw
    # from the pool so overlapping bookings are intentional, not clashes.
    bookings_obj = load("workforce/bookings.json")
    pooled = set((bookings_obj or {}).get("pooled_asset_ids", []) if isinstance(bookings_obj, dict) else [])
    pooled_overlaps = 0
    windows = []
    for j in jobs:
        s, e = parse_d(j.get("start_date", "")), parse_d(j.get("end_date", ""))
        if s and e:
            windows.append((j.get("job_id"), s, e, j.get("asset_ids", []), j.get("employee_ids", [])))
    for i in range(len(windows)):
        for k in range(i + 1, len(windows)):
            j1, s1, e1, a1, m1 = windows[i]
            j2, s2, e2, a2, m2 = windows[k]
            if overlaps(s1, e1, s2, e2):
                for aid in set(a1) & set(a2):
                    if aid in pooled:
                        pooled_overlaps += 1  # intentional: shared pool, not a clash
                    else:
                        warn(f"asset {aid}: double-booked on {j1} and {j2} (overlapping dates)")
                for eid in set(m1) & set(m2):
                    warn(f"employee {eid}: double-booked on {j1} and {j2} (overlapping dates)")

    # --- Report ---
    print(f"customers={len(customers)} sales={len(sales)} assets={len(assets)} "
          f"employees={len(employees)} jobs={len(jobs)}")
    won = [s for s in sales if s.get('stage') == 'Won']
    delivered = {j.get('sale_id') for j in jobs}
    missing = [s['sale_id'] for s in won if s['sale_id'] not in delivered]
    if missing:
        warn(f"Won sales with no job on the calendar yet: {missing}")
    print(f"joins: {len(delivered & sale_ids)} jobs resolve to sales; "
          f"{len(won)} Won sales, {len(delivered)} scheduled.")
    if pooled:
        print(f"info: {pooled_overlaps} overlapping booking(s) of pooled assets "
              f"{sorted(pooled)} exempted from the §3 no-overlap rule (shared pool).")

    if WARNINGS:
        print(f"\n⚠ {len(WARNINGS)} warning(s):")
        for w in WARNINGS:
            print(f"  - {w}")
    if ERRORS:
        print(f"\n✗ {len(ERRORS)} ERROR(S):")
        for e in ERRORS:
            print(f"  - {e}")
        print("\nFAIL — data-model integrity errors above.")
        sys.exit(1)
    print("\n✓ PASS — all IDs valid, all cross-domain joins resolve.")

if __name__ == "__main__":
    main()
