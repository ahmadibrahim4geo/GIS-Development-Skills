# Website, Brand Kit 3.1, Catalog Counters & CI Contracts

> Operational details offloaded from [`AGENTS.md`](../../AGENTS.md) via progressive disclosure. These rules remain binding whenever repository documentation, website pages, catalogs, assets, or CI workflows are inspected or modified.

## 1. User-Facing Website & Documentation Structure

- **Primary How-to-Use Surface:** `index.html` at the repository root serves as the primary interactive guide for end users. Install prompts across clients/platforms must be copyable and bilingual (English + Arabic), backed by `assets/home-redesign.css` and responsive workflow cards.
- **Bilingual Guides:** Maintain [`docs/HOW_TO_USE.md`](../../docs/HOW_TO_USE.md) and [`docs/HOW_TO_USE.ar.md`](../../docs/HOW_TO_USE.ar.md) linked from `index.html` and `explorer.html`, exposing clear prerequisites, manual and agent routes, real copyable requests, honest test/permission caveats, and intact creator/footer metadata. Keep `README.md` / `README.ar.md` and `docs/HOW_TO_USE*.md` synchronized for user-facing capabilities.
- **GitHub Pages Subpath Safety:** `index.html`, `explorer.html`, `project-wizard.html`, and `assets/` must resolve using project-relative (`./`) subpaths on GitHub Pages, not only domain-root paths.
- **Single Catalog Data Source:** Project cards and GIS API cards must load dynamically from canonical JSON files (`references/project-catalog.json`, `references/gis-apis.json`). Never hardcode a duplicate catalog inside HTML/JS or represent third-party web services as unrestricted.
- **Language Switch, RTL & Accessibility:** Preserve the English/Arabic language switcher, RTL directional layout support, and keyboard-accessible search/filter controls across all website pages. Keep English as the default technical developer presentation while supporting Arabic switching cleanly.
- **Administrator Settings Boundary:** GitHub repository sidebar About, topics, homepage URL, Discussions toggle, and GitHub Pages source branch are repository administrator settings; never claim that committing Markdown modifies them.

## 2. Brand Kit 3.1 & Author Panel Contract

- **Approved Brand Title & Tagline:** **GIS Development Skills** — **The Heart of Geospatial Innovation**. Keep both intact in `assets/logo.svg` and the homepage hero.
- **Verbatim English Mission Statement:** Preserve the following sentence **verbatim** immediately below the hero logo in `index.html` and in `README.md`:
  `Build GIS tools, plugins and geospatial applications with a verifiable development workflow.`
- **Logo & Icon Consistency:** Visual identity follows **Brand Kit 3.1** — a geometric `G` containing a four-square teal grid (`#0F3D5E` navy on light surfaces / white on dark surfaces). Keep [`assets/icon.svg`](../../assets/icon.svg) synchronized with [`assets/logo.svg`](../../assets/logo.svg), follow [`assets/README.md`](../../assets/README.md), and keep SVGs and the 6:1 banner at their intrinsic proportions.
- **Plugin Card Credit Alignment:** Generated plugin manifests use `"icon": "assets/icon.svg"`, `"author": {"name": "Ahmad Ibrahim", "url": "https://ahmadibrahim4geo.github.io/MIRSAD/"}`, and `"description": "The Heart of Geospatial Innovation — By Ahmed Ibrahim"`.
- **Author Panel (`#author`):** Based on Ahmad Ibrahim's published biography and portrait on `https://ahmadibrahim4geo.github.io/MIRSAD/`. Preserve exact markup and contact links when redesigning other page areas (palette refinements only), keep raw phone digits hidden in the UI, and never repurpose MIRSAD-specific climate/consulting engagements as claims about this repository. Load enhancements via `assets/brand-refresh.css` after inline base styles without breaking catalog filters or relative links.

## 3. Counters, Frontmatter, CI & Pre-Publish Gates

- **Real Inventory Counters:** Initial project, API, data-repository, and skill counters displayed in documentation and UI must match `references/repository-manifest.json`, `references/project-catalog.json`, `references/gis-apis.json`, `references/geospatial-data-repositories.json`, and `skills/*/SKILL.md`. Never increment a counter manually or overwrite historical entries in `CHANGELOG.md`.
- **Agent Skills YAML Frontmatter:** Every `skills/*/SKILL.md` must keep `name` equal to its folder name (lowercase kebab-case), concise `description` (`<= 1024` characters) written developer-first, and progressive links into `references/`. Label illustrative templates honestly as untested inside host apps until verified (`T2–T4`).
- **Stand-alone vs Extension Paths & Excluded Projects:** Keep standalone GIS applications distinct from ArcGIS SDK extensions and QGIS plugins (`UI.js` ambiguity unresolved until verified). Never re-add excluded immature projects without a fresh maturity review and explicit user approval.
- **Weekly Link Checks:** Automated link availability checks do not prove API licensing, schema validity, or scientific accuracy; keep unverified external services marked unknown until tested against primary terms and endpoints.
- **CI Policy & Pre-Publish Verification:** CI triggers on pull requests and `main` pushes (`docs/GITHUB_ACTIONS_TROUBLESHOOTING.md`), never suppressing failing quality tests to reduce noise. Before any authorized release/publish run:
  - `python scripts/validate_catalog.py`
  - `python scripts/validate_api_catalog.py`
  - `python scripts/validate_skill_pack.py`
  - `python scripts/audit_skill_graph.py`
  - `python scripts/audit_agent_policy.py`
  - `python scripts/security_audit.py --root .`
  - `python scripts/build_manifest.py --check`
  - `python -m unittest discover -s tests -v` (including `tests/test_landing_page.py`, `tests/test_how_to_use.py`, `tests/test_home_redesign.py`)
