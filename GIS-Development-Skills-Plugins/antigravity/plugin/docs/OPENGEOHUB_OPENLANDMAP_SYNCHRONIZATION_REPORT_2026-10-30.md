# OpenGeoHub & OpenLandMap Synchronization and Integration Report

**Date:** 30 October 2026  
**Local Repository:** `d:\My Software\GIS-Development-Skills`  
**Branch:** `main`  
**Merged PR #36 Commit:** `017262d73679318a8d22ac07c38ea63693ebb9e8`  
**Status:** Completed & Verified

---

## 1. Repository State Before and After Synchronization

### Before Synchronization
- Branch: `main`
- Local commit: `c442698` (`fix: report homepage test evidence accurately`)
- Working tree: Clean (no unstaged changes)
- Prior historical counts at that release: 35 skills, 188 project references, 52 API services, 24 geospatial data repositories, and 12 documented code sources in `gis-code-sources.json`.

### After Synchronization and Reconciliation
- Executed `git fetch origin` retrieving PR #36 merge commit `017262d` from `origin/main`.
- Fast-forwarded cleanly via `git merge --ff-only origin/main` without conflicts, data loss, or destructive git reset/clean commands.
- Audited synchronization gaps across routing, discovery catalogs, UI counters, documentation, and regression tests.
- Historical synchronized counts at PR #36 closure: **35 skills**, **193 project references**, **52 API services**, **26 geospatial data repositories**, and **17 documented scientific/code sources**.

---

## 2. Upstream Changes Brought via PR #36

PR #36 (`017262d`) introduced:
1. Five scientific repositories added to `references/project-catalog.json` and `references/gis-code-sources.json`.
2. Two new data directory entries in `references/geospatial-data-repositories.json` (`opengeohub-foundation` and `openlandmap-stac`).
3. Updated `references/geospatial-data-repositories.md` and `references/repository-manifest.json`.
4. Initial `references/opengeohub-openlandmap-integration.md` guide.
5. Initial updates to `skills/geospatial-data-catalogs/SKILL.md`, `skills/geospatial-data-discovery/SKILL.md`, and `skills/gis-code-discovery/SKILL.md`.

---

## 3. Remediated Integration Gaps

| Domain / File | Observed Gap in Initial PR #36 | Fix Applied |
|---|---|---|
| **Intent routing** (`scripts/intent_router.py`) | Bilingual prompts for spatial prediction, soil properties, land cover, COG layers, and research-code comparisons lacked domain keyword hints. | Added precise bilingual domain phrases to `DOMAINS` (`gis-code-discovery`, `geospatial-data-discovery`, `remote-sensing-pipelines`, `geospatial-data-catalogs`). |
| **Code discovery** (`scripts/gis_code_discovery.py`) | Missing `spatial-modeling` pattern in `PLATFORM_PATTERNS`. | Added `spatial-modeling` weighting so `scikit-map` and `spatial-prediction-eml` rank appropriately. |
| **Integration reference** (`references/opengeohub-openlandmap-integration.md`) | Initial 22-line stub lacked repository boundaries and protocol distinctions (Static STAC vs STAC API vs COG vs WMS). | Expanded into full reference covering repository matrix, protocol comparison, data flow, and Z-EARTH Data Explorer UI workflow. |
| **README & Arabic README** (`README.md`, `README.ar.md`) | Stale counters remained at 24 data repositories and 12 code sources. | Synchronized counters (26 data repositories, 17 code sources) and repository license/boundary notes. |
| **Homepage** (`index.html`) | Stale code-discovery counter (`12`) and missing OpenGeoHub review card. | Updated counter to `17` and added OpenGeoHub / OpenLandMap card linking directly to the integration guide. |
| **Explorer** (`explorer.html`) | Stale notice showing 24 data repositories. | Updated notice to `26` guides/portals and linked the integration guide. |
| **Release log** (`CHANGELOG.md`) | Overly brief note missing routing/test updates. | Documented synchronized routing, discovery, UI, and test additions. |
| **Regression tests** (`tests/test_code_discovery.py`) | Missing dedicated checks for the five user scenarios and license boundaries. | Added `test_11`, `test_12`, and `test_13` verifying `scikit-map` lookup, `soildb` unverified-license warnings, and all five routing scenarios. |

---

## 4. Audited Repository & License Summary (PR #36 Cohort)

| Repository | Primary Purpose | Languages / Stack | License & Evidence Status | When Agents Should Reference It | When Agents **Must Not** Copy/Assume It |
|---|---|---|---|---|---|
| **`scikit-map`** | Spatial ML & environmental mapping | Python, `scikit-learn`, `rasterio`, GDAL | **MIT** (verified in repo root) | Building spatial CV pipelines resistant to spatial autocorrelation leakage | Plain tabular ML (prefer standard `scikit-learn`) or unbenchmarked huge rasters |
| **`soildb`** | Soil database harmonization & modeling | Python, R, SQL | **verify-upstream** (no explicit root license) | Studying soil profile schemas and SoilGrids covariate structure | **Do not copy code directly**; not an installable CLI tool or live DB service |
| **`GEDTM30`** | 30 m global ensemble terrain model | Python, GDAL, Bash | **verify-upstream** (no explicit root license) | Algorithmic study of multi-DEM fusion (SRTM, ALOS, Copernicus) | **Do not copy code directly**; assume no live tile stream or skip vertical datum checks |
| **`spatial-prediction-eml`** | Ensemble spatial prediction in R | R (`mlr`, `ranger`, `sp`, `raster`) | **CC-BY-SA-4.0** (verified in repo root) | Studying ensemble uncertainty mapping in R | Embedding in closed/proprietary products under ShareAlike restrictions |
| **`spatial-layers`** | Environmental cartographic styles & layer defs | Python, JSON, SLD, QML | **GPL-3.0** (verified in repo root) | Studying scientific color ramps and symbology classifications | **Do not copy into non-GPL software**; follow clean-room authoring rules |

---

## 5. Verified Routing Scenarios (`scripts/intent_router.py`)

Tested against bilingual prompts using offline keyword hints:
1. Spatial prediction Python code -> `gis-code-discovery`, `arcgis-toolbox-engineering`, `gis-security-guardian`.
2. Soil property maps for an AOI -> `geospatial-data-discovery`, `gis-security-guardian`.
3. Land cover products with temporal coverage -> `remote-sensing-pipelines`, `geospatial-data-discovery`, `gis-security-guardian`.
4. Viewing a COG raster inside a GIS app -> `remote-sensing-pipelines`, `gis-security-guardian`.
5. Comparing an open data source vs a research-code repo -> `gis-code-discovery`, `geospatial-data-catalogs`, `gis-security-guardian`.

---

## 6. Historical Validation & Test Results (30 October 2026)

- `python scripts/validate_catalog.py` -> PASS (`193 sources`)
- `python scripts/validate_api_catalog.py` -> PASS (`52 services`)
- `python scripts/validate_data_repositories.py` -> PASS (`26 entries`)
- `python scripts/validate_skill_pack.py` -> PASS (`35 skills`)
- `python scripts/build_manifest.py --check` -> PASS (`35 skills / 193 references / 52 APIs / 26 data repositories`)
- `python -m unittest discover -s tests -v` -> Ran `394 tests -> OK (skipped=1, failures=0)`

---

## 7. Modified Files in Historical Synchronization Cohort

1. `references/opengeohub-openlandmap-integration.md`
2. `scripts/intent_router.py`
3. `scripts/gis_code_discovery.py`
4. `tests/test_code_discovery.py`
5. `README.md` and `README.ar.md`
6. `index.html` and `explorer.html`
7. `CHANGELOG.md`

---

## 8. Residual Boundaries Preserved

- **`soildb` & `GEDTM30` licensing:** Remain flagged `verify-upstream` (`license_verified: false`); direct code copying stays prohibited.
- **Static OpenLandMap STAC architecture:** Hosted as static S3 STAC metadata rather than guaranteed dynamic `/search` CQL2 API.
- **No unapproved remote push:** Local synchronization verification left `origin` untouched pending explicit authorization.
