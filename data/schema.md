# KingKira Group — Shared Data Model (v0.1 — FROZEN)

> Canonical, cross-domain data model for the KingKira Group demo site.
> **Owner of this file:** Bob (Assets). Propose changes in `room` before editing.
> All data is **synthetic** and for demonstration only.

KingKira Group is a 100% Aboriginal female-owned mining & energy **services**
business in Western Australia. It wins work from mining/energy clients (Sales),
delivers that work as jobs that consume **assets** (plant/equipment) and
**people** (employees / labour hire), all scheduled through a shared **booking
calendar** (the `job` entity).

Tagline: *Empowering People, Protecting Country, Creating Opportunity.*

---

## 1. Domains & owners

| Domain               | Owner | Entities owned            | Data path            |
|----------------------|-------|---------------------------|----------------------|
| Sales                | Alice | `customer`, `sale`        | `/data/sales/`       |
| Assets               | Bob   | `asset`                   | `/data/fleet/`       |
| Workforce Planning   | Cindy | `employee`, `job`         | `/data/workforce/`   |

`job` is the shared **booking calendar**: it references Sales (`sale_id`),
Assets (`asset_ids[]`) and Workforce (`employee_ids[]`). Everyone reads it; only
Cindy writes it.

---

## 2. Shared enums

- **service_line**: `Industrial` | `Environmental` | `Recruitment`
- **site**: `Perth - Applecross` (HQ) | `Pilbara - Newman` | `Pilbara - Tom Price` | `Pilbara - Karratha`
- **asset status**: `Operational` | `Maintenance` | `Standby`
- **job status**: `Scheduled` | `In Progress` | `Completed` | `Cancelled`

---

## 3. Entities & IDs

| Entity     | PK            | ID format      | Owner |
|------------|---------------|----------------|-------|
| customer   | customer_id   | `CUST-###`     | Alice |
| sale       | sale_id       | `SALE-####`    | Alice |
| asset      | asset_id      | `KK-<CAT>-###` | Bob   |
| employee   | employee_id   | `EMP-###`      | Cindy |
| job        | job_id        | `JOB-####`     | Cindy |

### customer  (Alice) — `/data/sales/`
`customer_id` `CUST-###`, name, industry (Iron Ore/Gas/Infrastructure…),
site, account_manager, since (date).

### sale  (Alice)
`sale_id` `SALE-####`, customer_id→customer, service_line, description,
value_aud, stage (`Won`|`Proposal`|`Negotiation`|`Lost`), start_date, end_date,
resource_needs { asset_categories:[], employee_roles:[{role,count}] }.
A **Won** sale spawns one or more `job`s (Cindy resolves resource_needs into real
asset_ids + employee_ids on the calendar).

### asset  (Bob) — plant / equipment — see `/data/fleet/asset_register.csv`
`asset_id` `KK-<CAT>-###` (e.g. `KK-HT-001`), category, make_model, year, site,
status (asset status), acquisition_cost_aud, current_book_value_aud,
utilisation_pct_ytd (0–100), last_service_date, next_service_due,
condition (Excellent|Good|Fair), owner_division.

**CAT codes:** HT haul truck · EX excavator · DZ dozer · WC water cart ·
LV light vehicle · GS generator · PU pump · EM env monitor · WS workshop ·
AC accommodation · TR trailer.

### employee  (Cindy) — `/data/workforce/`
`employee_id` `EMP-###`, name, role, service_line, skills[] (tickets/certs),
site (home base), status (`Available`|`On Job`|`Leave`), employment_type
(`Permanent`|`Labour Hire`|`Casual`), indigenous (bool, for empowerment metrics).

### job  (Cindy) — the shared booking CALENDAR
| field | type | notes |
|-------|------|-------|
| job_id | string | `JOB-2001` |
| sale_id | FK→sale | work this job delivers |
| service_line | enum(service_line) | |
| site | enum(site) | |
| start_date | date | booking window start |
| end_date | date | booking window end |
| status | enum(job status) | |
| asset_ids | FK[]→asset | assets booked (e.g. `["KK-HT-001","KK-WC-030"]`) |
| employee_ids | FK[]→employee | crew booked (e.g. `["EMP-007","EMP-012"]`) |

A resource (asset or employee) should not appear on two jobs with overlapping
date ranges — that is the scheduling constraint the calendar enforces.

---

## 4. Relationships

```
customer 1 ──< sale 1 ──< job >── * asset      (job books assets)
                          job >── * employee    (job books crew)
```

- `customer` 1—* `sale`
- `sale` (Won) 1—* `job`
- `job` *—* `asset` (via `asset_ids[]`)
- `job` *—* `employee` (via `employee_ids[]`)

Assets and Workforce are the **delivery resources** that Sales' jobs consume,
connected through the booking calendar (`job`).

## 5. Join keys (foreign keys)

| From | Field          | To       |
|------|----------------|----------|
| sale | customer_id    | customer |
| job  | sale_id        | sale     |
| job  | asset_ids[]    | asset    |
| job  | employee_ids[] | employee |

## 6. Conventions

- IDs: uppercase, hyphenated prefix, zero-padded (see §3).
- Dates ISO `YYYY-MM-DD`. Currency AUD, integer dollars.
- Each owner writes only files under their `/data/<domain>/` path.
- Publish datasets as CSV (spreadsheet-friendly) and/or JSON (site rendering).
- Before pushing: `git pull --rebase`; edit only your own paths to avoid conflicts.

## 7. Key ranges (avoid ID collisions)

- Alice: `CUST-001…`, `SALE-1001…`
- Bob:   `KK-<CAT>-001…` (see asset register)
- Cindy: `EMP-001…`, `JOB-2001…`
