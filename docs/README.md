# KingKira Group — demo site (`/docs`)

Static site published with **GitHub Pages** from `main` → `/docs`. Synthetic-data demo showing
agent-to-agent coordination (ppz). Not an official KingKira asset.

## Layout & ownership

| Path                    | Owner  | Purpose                                   |
|-------------------------|--------|-------------------------------------------|
| `docs/index.html`       | alice  | Shared landing (3 sub-menus)              |
| `docs/assets/css/brand.css` | alice | **Shared brand kit** — do not fork    |
| `docs/assets/js/include.js` | alice | **Shared header/footer injector**     |
| `docs/sales/`           | alice  | Sales dashboard                           |
| `docs/fleet/`           | bob    | Assets dashboard                          |
| `docs/workforce/`       | cindy  | Workforce Planning dashboard              |
| `data/{sales,fleet,workforce}/` | each owner | Synthetic datasets              |
| `data/schema.md`        | bob    | Canonical shared data model               |

**Work only in your own paths. `git pull --rebase` before you push.**

## How to build your section page (Bob & Cindy)

Copy this skeleton into `docs/<your-section>/index.html`:

```html
<!DOCTYPE html>
<html lang="en" data-year="2026">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Assets — KingKira Group</title>
  <link rel="stylesheet" href="../assets/css/brand.css">
</head>
<body>
  <div id="site-header"></div>

  <!-- your content here -->

  <div id="site-footer"></div>
  <script src="../assets/js/include.js" data-active="fleet"></script>
</body>
</html>
```

### The include.js contract
- Put `<div id="site-header"></div>` as the **first** body element and
  `<div id="site-footer"></div>` as the **last**.
- Load the script last: `<script src="../assets/js/include.js" data-active="…"></script>`
- `data-active` ∈ `home | sales | fleet | workforce` — highlights your nav tab.
- The script derives the site root from its own `src`, so **section pages use `../assets/…`**;
  only the landing page (`docs/index.html`) uses `assets/…`. Match that relative depth and
  everything (nav links, font, footer) just works.

## Brand CSS — class list

**Layout:** `.kk-container` · `.kk-section` (`--tint`, `--dark`) · `.kk-grid` (`--2/--3/--4`) ·
`.kk-eyebrow` · `.kk-lead` · `.kk-divider`

**Hero:** `.kk-hero` + `.kk-hero__tag`

**Cards:** `.kk-card` (`--link` for hover-lift) · `.kk-card__icon` · `.kk-card__meta`

**Stat tiles:** `.kk-stat` (`--accent`) · `.kk-stat__label` · `.kk-stat__value` ·
`.kk-stat__delta` (`.up`/`.down`)

**Badges/pills:** `.kk-badge` (`--green` / `--amber` / `--red` / `--navy` / `--orange`) ·
`.kk-pill-row`

**Tables:** wrap in `.kk-table-wrap` → `<table class="kk-table">`; right-align numbers with `.kk-num`

**Buttons:** `.kk-btn` (`--primary` / `--ghost` / `--dark`)

**RISE values:** `.kk-rise` → `.kk-rise__item`

**Utilities:** `.kk-flex` · `.kk-between` · `.kk-center` · `.kk-muted` · `.kk-mt0` · `.kk-mb0` ·
`.kk-demo-note`

### Palette (CSS vars, from kingkira.com.au)
`--kk-orange #f98e2b` · `--kk-gold #ffce00` · `--kk-navy #002839` · `--kk-slate #334c51` ·
`--kk-green #65bc7b` (positive) · `--kk-amber #e6a817` (watch) · `--kk-red #d64545` (risk)

Display font **Yanone Kaffeesatz** (auto-loaded by include.js), body **Inter**.
