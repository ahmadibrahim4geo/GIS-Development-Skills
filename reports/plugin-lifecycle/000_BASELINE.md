# Phase P00 Baseline & Gap Audit Report (`000_BASELINE`)

- **Date (local):** `2026-11-25`
- **Repository root:** `D:/My Software/Skills/GIS Development Skills`
- **Branch:** `codex/engineering-suite`
- **HEAD commit:** `42de4a246a2db1f7d33cc746da9cd3a0f1718a91`
- **Scope:** Strictly read-only repository and toolchain inspection prior to `P01` updates (`AGENTS.md`, taxonomy, contracts). No existing uncommitted changes were reset, dropped, or overwritten.

## 1. Observed Repository Inventory Counts

| Asset / Registry | Observed Baseline Value | Verification Source |
|---|---|---|
| Installed skills (`skills/*/SKILL.md`) | `35` (Manifest `documentation_version: 0.3.5`) | `scripts/build_manifest.py --check`, `scripts/audit_skill_graph.py` (`routed=33`, `lexical domains=30`) |
| Project catalog (`references/project-catalog.json`) | `193` entries (`22` verified license evidence, `171` unverified) | `scripts/validate_catalog.py`, `scripts/audit_license_catalog.py --summary` |
| Urban design registry (`references/urban-design-source-registry.json`) | `78` entries — **confirmed defect:** `UDS-LIB-004` (`DuckDB Spatial`) points to `https://github.com/duckdb/duckdb-skills` with `security_rating: safe` (scheduled fix in `P03`) | Direct JSON audit |
| Free geospatial APIs (`references/free-geospatial-apis.json`) | `53` services | `scripts/validate_api_catalog.py` |
| Geospatial data repositories | `26` entries | `scripts/validate_data_repositories.py` |
| Code discovery sources / recipes | `17` sources / `5` recipes | Direct JSON inspection |
| Quarantined external skills (`New Skill/SKILLS_REGISTRY.json`) | `6` entries | Direct JSON inspection |
| Security audit (`scripts/security_audit.py --root .`) | `PASS` (`35` skills, `0` findings; external scanners `NOT RUN`) | Command execution |
| Evidence tiers (`scripts/validate_evidence_tiers.py`) | `PASS` | Command execution |
| Existing bundle builder | `scripts/build_skill_bundle.py` (`gis-development-suite.zip`, `schema_version: 1.0`; `plans/` excluded from `ALLOWED_ROOT_DIRECTORIES`) | Direct file read |
| Active related plans | `plans/active/0001_Engineering-Suite`, `plans/active/0006_Mobile-and-Web-GIS-Expansion` (`DRAFT`, r1 `T1–T6`), `plans/active/0007_Master-Integration` | Directory inspection |
| Uncommitted pre-existing working tree state | Multiple local modifications preserved (`AGENTS.md`, `skills/gis-development/SKILL.md`, `.agent-development-log/0067..0112`, `PROJECT_STRUCTURE.md`, `New Skill/`, `dist/`, etc.) | `git status -s` |

## 2. Unit Test Baseline (`python -m unittest discover -s tests -q`)

- **Total run:** `518 tests` (`skipped=1` in environment-conditional test), `failures=1` before link cleanup in `01_Master_Integration_Plan.md`:
  - `plans\active\0007_Master-Integration\01_Master_Integration_Plan.md` had 3 external `../../../../GIS_...` links pointing outside the repo (converted to plain code text for CI & link compliance).
  - **Pre-existing non-0007 failure preserved in baseline record:** `dist\user-testing\banner-work\brand-kit-readme.md: assets/brand/banner.png` (`RepositoryInternalLinksTests.test_linked_local_files_exist`).

## 3. Local CLI & Toolchain Probe (Read-Only, Zero Credential Access)

| Tool / Platform CLI | Observed Status (`Get-Command` / `toolchain_discovery.py`) |
|---|---|
| `python` | Found (`C:\Users\ahmad\AppData\Local\Microsoft\WindowsApps\python.exe`) |
| `powershell` | Found (`C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe`) |
| `git` | Found (`GitHubDesktop` Git CLI) |
| `node`, `npm` | Found (`C:\Program Files\nodejs\node.exe`, `npm.ps1`) |
| `pwsh`, `codex`, `claude`, `agy`, `cursor` | `NOT_FOUND` on current `PATH` |
| `adb`, `flutter`, `dart`, `qgis`, `gdalinfo`, `ogr2ogr` | `NOT_FOUND` on current `PATH` |
| `xcodebuild` / Apple toolchain | Unavailable on Windows host (`NOT RUN` for native iOS builds) |

> **Honesty Boundary:** `NOT_FOUND` on `PATH` does not prove absence elsewhere on disk, nor grant permission to auto-install or probe private session files. Native GIS (`QGIS`, `GDAL`), mobile binaries (`Android`, `iOS`), and client sync remain `NOT RUN` until verified in eligible environments.
