#!/usr/bin/env python3
"""Expand the KingKira asset register to a realistic fleet for a ~400-staff
Pilbara industrial/environmental/labour-hire contractor.

Keeps the existing 25 rows VERBATIM (so bookings.json + asset_plan.json joins stay
valid) and appends new assets across expanded categories. Synthetic/demo data.
Deterministic (fixed seed)."""
import csv, json, random, datetime, os

random.seed(42)
HERE = os.path.dirname(os.path.abspath(__file__))
FLEET = os.path.join(HERE, '..', 'docs', 'data', 'fleet')
CSV = os.path.join(FLEET, 'asset_register.csv')
TODAY = datetime.date(2026, 8, 24)

SITES = ['Pilbara - Newman', 'Pilbara - Port Hedland', 'Pilbara - Karratha', 'Perth - Applecross']
SITE_W = [0.42, 0.22, 0.22, 0.14]
IND = 'Industrial Services'; ENV = 'Environmental Services'; REC = 'Recruitment & Labour Hire'; COR = 'Corporate'

# category -> (code, [make_models], (cost_lo, cost_hi), [division weights over (IND,ENV,REC,COR)], start_num, count_to_add)
CATS = {
 'Haul Truck':          ('HT', ['Caterpillar 777G','Komatsu HD785-7','Caterpillar 785C'],           (3.4e6,3.9e6), (0.9,0.1,0,0), 4, 2),
 'Excavator':           ('EX', ['Caterpillar 349','Komatsu PC490LC-11','Hitachi ZX350','Caterpillar 336','Volvo EC480'], (0.9e6,1.3e6), (0.75,0.25,0,0), 13, 4),
 'Dozer':               ('DZ', ['Caterpillar D8T','Komatsu D65PX-18','Caterpillar D9'],              (1.5e6,1.8e6), (0.9,0.1,0,0), 22, 1),
 'Grader':              ('GR', ['Caterpillar 14M','Komatsu GD655','John Deere 772G'],                (0.7e6,1.0e6), (0.85,0.15,0,0), 200, 3),
 'Loader':              ('LO', ['Caterpillar 966M','Komatsu WA380','Volvo L120'],                    (0.6e6,0.95e6),(0.8,0.2,0,0), 210, 3),
 'Water Cart':          ('WC', ['Caterpillar 740 (30kL)','Volvo A40G (30kL)','Komatsu HM400 (30kL)'],(0.7e6,0.85e6),(0.4,0.6,0,0), 32, 2),
 'Skid Steer':          ('SS', ['Bobcat S770','Caterpillar 262D','Kubota SVL75'],                    (85e3,130e3), (0.7,0.3,0,0), 330, 3),
 'Vacuum Truck':        ('VT', ['STG Hydrovac 6000','Vac-U-Digga VUD8000','Isuzu FVZ Wet/Dry Vac','Kenworth T410 Hydrovac'], (420e3,620e3),(0.5,0.5,0,0), 220, 6),
 'Generator':           ('GS', ['Cummins C550 D5 (550kVA)','Cummins C275 D5 (275kVA)','Cummins C900 D5 (900kVA)','FG Wilson P200'], (75e3,190e3),(0.85,0.15,0,0), 52, 3),
 'Compressor':          ('CP', ['Atlas Copco XAS 400','Sullair 375H','Kaeser M250'],                 (55e3,95e3),  (0.9,0.1,0,0), 230, 3),
 'Dewatering Pump':     ('PU', ['Sykes CP150i','Xylem Godwin HL160M','Sykes GP150','Weir Multiflo MF420'], (60e3,90e3),(0.2,0.8,0,0), 62, 2),
 'Elevated Work Platform':('EW',['JLG 600AJ Boom','Genie S-85 Boom','JLG 3394RT Scissor','Snorkel A46JRT'], (95e3,180e3),(0.9,0.1,0,0), 240, 4),
 'Telehandler':         ('TH', ['Manitou MT1840','Merlo P40.17','JCB 540-170'],                      (140e3,210e3),(0.9,0.1,0,0), 250, 3),
 'Forklift':            ('FL', ['Hyster H3.5FT','Toyota 8FG25','Combilift C4000'],                   (45e3,85e3),  (0.85,0.05,0.05,0.05), 260, 3),
 'Mobile Crane':        ('FR', ['Terex Franna AT-20','Terex Franna MAC25'],                          (380e3,520e3),(0.95,0.05,0,0), 270, 2),
 'Lighting Tower':      ('LT', ['Allight SL200','Sunlite BossLite','Atlas Copco HiLight H5'],        (18e3,34e3),  (0.75,0.25,0,0), 280, 5),
 'Road Sweeper':        ('SW', ['MacDonald Johnston CN201','Schwarze A7 Tornado'],                   (280e3,360e3),(0.2,0.8,0,0), 290, 2),
 'Fuel Truck':          ('FT', ['Isuzu FXZ Service/Fuel','Kenworth T410 Fuel/Lube'],                 (240e3,320e3),(0.8,0.15,0,0.05), 300, 2),
 'Environmental Monitor':('EM',['Aeroqual AQS1 Air Quality Station','Thermo Scientific pDR-1500 Dust','Aeroqual Dust Sentry','Hydrolab HL7 Water Quality'], (14e3,45e3),(0.1,0.9,0,0), 72, 1),
 'Workshop Equipment':  ('WS', ['Lincoln Electric Welder Bank','Enerpac Hydraulic Press 50T','Mobile Field Workshop Container'], (30e3,70e3),(0.85,0.05,0.05,0.05), 82, 1),
 'Site Accommodation':  ('AC', ['Modular Ablution Block x4','Modular Office Complex','Modular Sleeper Units x12','Wet Mess / Kitchen Module','Modular Crib Room'], (150e3,340e3),(0.05,0.05,0.85,0.05), 92, 4),
 'Site Office':         ('SC', ['20ft Site Office Container','40ft Site Office Container','Container Ablution','Container Store/Laydown'], (18e3,55e3),(0.3,0.2,0.4,0.1), 310, 4),
 'Crew Bus':            ('CT', ['Toyota Coaster 22-seat','Mercedes-Benz Sprinter 12-seat','Volvo B8R 57-seat Coach'], (95e3,320e3),(0.2,0.1,0.6,0.1), 320, 3),
 'Trailer':             ('TR', ['Float Trailer 4-Row Extendable','Side Tipper Road Train Set','Drop Deck Semi','Dolly + Quad Trailer'], (170e3,340e3),(0.8,0.15,0,0.05), 102, 2),
 'Light Vehicle':       ('LV', ['Toyota LandCruiser 79 Series','Toyota HiLux SR5','Toyota LandCruiser 200 Series','Ford Ranger XLT','Isuzu D-Max'], (72e3,95e3),(0.4,0.2,0.2,0.2), 43, 32),
}
CONDS = ['Excellent','Good','Good','Good','Fair']
def pick_div(w):
    return random.choices([IND,ENV,REC,COR], weights=w)[0]
def d(days):
    return (TODAY + datetime.timedelta(days=days)).isoformat()

# --- keep existing rows verbatim ---
with open(CSV) as f:
    reader = csv.reader(f)
    header = next(reader)
    existing = [row for row in reader]
existing_ids = {r[0] for r in existing}

new_rows = []
for cat,(code, models, (clo,chi), w, start, add) in CATS.items():
    for i in range(add):
        num = start + i
        aid = f'KK-{code}-{num:03d}'
        if aid in existing_ids:
            continue
        year = random.randint(2016, 2025)
        age = 2026 - year
        acq = int(round(random.uniform(clo, chi) / 1000) * 1000)
        book = int(round(acq * max(0.28, 1 - age*0.11) / 1000) * 1000)
        util = random.randint(38, 95)
        roll = random.random()
        status = 'Operational' if roll < 0.85 else ('Maintenance' if roll < 0.93 else 'Standby')
        last = -random.randint(5, 85)
        nxt = last + random.choice([90, 120, 150])
        cond = random.choice(CONDS)
        site = random.choices(SITES, weights=SITE_W)[0]
        if code in ('WS','FR') and random.random() < 0.5:
            site = 'Perth - Applecross'
        div = pick_div(w)
        new_rows.append([aid, cat, random.choice(models), year, site, status,
                         acq, book, util, d(last), d(nxt), cond, div])

# sort new rows by category code then id for tidiness, keep existing first (stable order)
new_rows.sort(key=lambda r: (r[0].split('-')[1], r[0]))
all_rows = existing + new_rows

# migrate legacy 'Pilbara - Tom Price' (not a real KK depot) -> Port Hedland, so the
# whole register matches KingKira's real depot footprint (schema §2 v0.2).
for r in all_rows:
    if r[4] == 'Pilbara - Tom Price':
        r[4] = 'Pilbara - Port Hedland'

with open(CSV, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(header)
    w.writerows(all_rows)

# JSON
ints = {'year','acquisition_cost_aud','current_book_value_aud','utilisation_pct_ytd'}
objs = []
for r in all_rows:
    o = dict(zip(header, r))
    for k in ints: o[k] = int(o[k])
    objs.append(o)
with open(os.path.join(FLEET, 'asset_register.json'), 'w') as f:
    json.dump(objs, f, indent=2)

# report
from collections import Counter
cat_count = Counter(o['category'] for o in objs)
print(f'existing kept: {len(existing)}  new added: {len(new_rows)}  total: {len(all_rows)}')
print('categories:', len(cat_count))
tot_book = sum(o['current_book_value_aud'] for o in objs)
tot_acq = sum(o['acquisition_cost_aud'] for o in objs)
print(f'book value: ${tot_book:,}  acq: ${tot_acq:,}  avg util: {sum(o["utilisation_pct_ytd"] for o in objs)/len(objs):.1f}%')
print('by status:', dict(Counter(o['status'] for o in objs)))
# assert existing ids preserved
assert existing_ids <= {o['asset_id'] for o in objs}, 'LOST an existing id!'
print('all existing ids preserved: OK')
