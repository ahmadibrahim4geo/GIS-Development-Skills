<p align="center"><img src="assets/logo.svg" alt="GIS Development Skills logo" width="720"></p>
<p align="center"><strong>Build GIS tools, plugins and geospatial applications with a verifiable development workflow.</strong></p>

# GIS Development Skills 🌍

[![GIS Skill validation](https://github.com/ahmadibrahim4geo/GIS-Development-Skills/actions/workflows/validate.yml/badge.svg)](https://github.com/ahmadibrahim4geo/GIS-Development-Skills/actions/workflows/validate.yml) ![License: MIT](https://img.shields.io/badge/license-MIT-3f8c76) ![Release: v0.3.5](https://img.shields.io/badge/release-v0.3.5-24483d)

**Project homepage:** [GitHub Pages website](https://ahmadibrahim4geo.github.io/GIS-Development-Skills/) *(check publication status in repository Pages settings)* · [View homepage source](index.html) · [English / العربية](README.ar.md) · [Logo](assets/logo.svg).

**Project overview:** A version-aware GIS developer agent skill plus curated references, public geospatial API catalog, and practical starter templates. Supports ArcGIS Pro, ArcMap, QGIS, GeoLibre, RustGIS, desktop applications, web maps, 3D terrain, remote sensing and GeoAI.

**An open, installable Agent Skill for building reliable GIS tools, plugins, web maps, and desktop geospatial applications.**

Created by [Ahmed Ibrahim](https://github.com/ahmadibrahim4geo). Independent community resource; **not affiliated with Esri, QGIS, GeoRust, GeoLibre, or other catalogued projects**.

> **Status:** v0.3.5 expanded open-source GIS catalog, GeoLibre R/RustGIS and public geospatial APIs. Curated source pointers, development workflows, code starter templates and offline catalog tools. Templates are illustrative; production workflows must be tested in the target GIS installation.

[اقرأ بالعربية](README.ar.md) · [Contributing](CONTRIBUTING.md) · [Publishing](PUBLISHING.md) · [Catalog](references/project-catalog.json) · [Skill](skills/gis-development/SKILL.md) · [Free GIS APIs](references/free-geospatial-apis.md) · [GeoLibre integrations](references/geolibre-integration.md) · [Report issues / propose features](https://github.com/ahmadibrahim4geo/GIS-Development-Skills/issues/new/choose)

## What makes this different from an awesome-list?

This repository includes a **working agent skill**: step-by-step architecture selection, compatibility rules, geospatial correctness checks, GIS application pathways, and reference starter code. The catalog is supporting evidence, **not a code-vending collection**. A coding agent must establish requirements, consult the relevant reference, verify package APIs, implement, and test before claiming success.

## Quality audit and standalone GIS development (v0.3.5)

The full source/skill-pack integrity audit introduced:

- [Standalone GIS Desktop Application Development](skills/gis-desktop-application-development/SKILL.md) — a **seventh** independent agent skill covering Qt/PySide, Tauri/Rust, C# WPF/WebView2, geospatial engines, installers and real UI acceptance.
- [Desktop engineering and release checklist](references/desktop-application-engineering.md), including MIRSAD Desktop as a development-stage case study.
- `python scripts/validate_skill_pack.py` — offline checks of all skill frontmatters, local documentation links, website resources, and synchronized project/API/skill counters.
- [Technical audit and outstanding verification](docs/TECHNICAL_AUDIT_2026-10-24.md), with exact test limits and remaining host-runtime checks.

**Current inventory:** 104 curated code/data references, 18 API providers and **7 installable skills**. The GitHub CI checks this repository's structure, not licensed ArcGIS execution, installed QGIS behavior, or a real Windows installer.

```bash
python scripts/validate_catalog.py
python scripts/validate_api_catalog.py
python scripts/validate_skill_pack.py
python -m unittest discover -s tests -v
```

## Tested-source references from our own GIS projects (v0.3.3)

**104 curated software projects and seven installable agent skills.** Five public source projects developed or curated by Ahmad Ibrahim are now documented as real engineering case studies, including native ArcGIS toolboxes and a standalone Desktop migration path:

- [MIRSAD](https://github.com/ahmadibrahim4geo/MIRSAD) — three ArcGIS Python Toolboxes, shared climate calculations, offline/headless and Pro acceptance evidence; separate **development-only** Windows Desktop build.
- [CreateFlowArrow](https://github.com/ahmadibrahim4geo/Create-FlowArrow-Tool) — gravity-network arrows, topology/slope audits and optional in-place geometry changes requiring explicit consent.
- [Geological Cross-Section Toolbox](https://github.com/ahmadibrahim4geo/GeologicalCrossSectionToolbox) — `.pyt`, separate geological engine, DEM and DXF/HTML export.
- [ArcMap Style Collection](https://github.com/ahmadibrahim4geo/ArcMap-Style-Collection) — cartographic/Arabic style references; third-party fonts and styles retain independent rights.
- [GIS Data Repositories Professional 2026](https://github.com/ahmadibrahim4geo/gis-data-repositories-professional-2026) — reusable data discovery and link auditing patterns.

**New** [ArcGIS Toolbox Engineering skill](skills/arcgis-toolbox-engineering/SKILL.md) · [Case-study and test evidence guide](references/ahmad-ibrahim-gis-case-studies.md).

This is an **implementation reference**, not a certification of all claimed features. Static/mocked ArcPy tests, native toolbox load, native geoprocessing execution and Desktop installer validation are reported as separate acceptance tiers.

```bash
npx skills add ahmadibrahim4geo/GIS-Development-Skills --skill arcgis-toolbox-engineering
```

## Esri coordinate systems and GIS development integration (2026-10-24)

**99 projects were cataloged at the CRS milestone** (prior to the six additional author-owned case studies); this included 15 newly reviewed Esri / CRS-source entries. The new specialist **[coordinate-reference-systems](skills/coordinate-reference-systems/SKILL.md)** preserves official ArcGIS Pro labels **Favorites · Layers · Geographic Coordinate Systems · Projected Coordinate Systems · Vertical Coordinate Systems · Custom**, with horizontal/vertical separation, Zone Series guidance, versioned WKID/latestWkid, datum grids and area-of-use safeguards.

- [Esri Projection Engine + SpatialReference.org + PROJ specification](references/esri-crs-and-spatialreference.md)
- [Esri open-source integration matrix](references/esri-open-source-integration.md)
- [Offline CSV/JSON catalog inspector](scripts/crs_catalog.py), with independent tests. Requires user-supplied Esri factory tables; does not bundle Esri's full database or proprietary engine.
- [SpatialReference.org](https://spatialreference.org/) for authority-linked WKT2 / Esri WKT / PROJJSON exports.
- [Official ArcGIS Pro folder structure](https://doc.esri.com/en/arcgis-pro/latest/help/mapping/properties/coordinate-system-folder-structure.html).

Install the specialist:

```powershell
npx skills add ahmadibrahim4geo/GIS-Development-Skills --skill coordinate-reference-systems
```

Explore a downloaded [Esri PE factory CSV/JSON dataset](https://github.com/Esri/projection-engine-db-doc):

```bash
python scripts/crs_catalog.py --source ./projection-engine-db-doc/csv --tree
python scripts/crs_catalog.py --source ./projection-engine-db-doc/csv --kind projcs --query Egypt
python scripts/crs_catalog.py --source ./projection-engine-db-doc/json --kind geogcs --format json --limit 5
```

**Scope and provenance:** this reproduces verified Esri *top-level presentation terminology*, not an unprovided exact country-level folder export. Actual datum transformation requires an installed, tested ArcPy/PROJ/GDAL/QGIS engine and relevant grids. Linked libraries and service plans retain their original terms.

## New in v0.3.2 — Dr. Qiusheng Wu GIS software ecosystem

We reviewed the [official software directory](https://gishub.org/software/) maintained by Dr. Qiusheng Wu and added **40 distinct verified repository links**. Our searchable catalog now contains **84 projects** covering Python, ArcGIS/Whitebox, QGIS, GeoAI, Rust/WebAssembly, MapLibre and metadata-based data discovery.

- [Technology and integration guide](references/gishub-software.md)
- [Geospatial data discovery skill](skills/geospatial-data-discovery/SKILL.md)
- [QGIS plugin development skill](skills/qgis-plugin-development/SKILL.md)
- [Geospatial web mapping skill](skills/geospatial-web-mapping/SKILL.md)

Install individual specialist skills with `npx skills add ahmadibrahim4geo/GIS-Development-Skills --skill qgis-plugin-development` (replace the skill name as needed). The main `gis-development` skill continues to route broader requests.

**Boundary:** a verified GitHub repository is not a guarantee that its examples work in a given GIS release or that its hosted imagery and APIs are free to reuse. Check versions, licenses, authentication and data terms before deployment.

## Target development paths

| Your goal | Preferred starting path | Read |
|---|---|---|
| ArcMap 10.x geoprocessing script | Legacy ArcPy / compatible Python 2.7 | `references/arcmap-legacy.md` |
| ArcGIS Pro `.pyt` or script tool | Modern ArcPy / Python 3 | `references/arcgis-pro.md` |
| QGIS plugin / Processing toolbox | PyQGIS, Processing provider | `references/qgis.md` |
| GIS desktop application | Python/Qt, Tauri/Rust, or C# + interoperable core | `references/desktop-and-web.md`, `references/dotnet-gis.md` |
| 2D maps / web mapping | MapLibre, GeoLibre, appropriate provider | `references/desktop-and-web.md` |
| GeoLibre-native maps, plugins, MCP and Python integration | Official GeoLibre skill, Python package, Plugin API | `references/geolibre-integration.md` |
| 3D globe / terrain | CesiumJS + verified imagery/terrain source | `references/desktop-and-web.md` |
| GIS in R / Rust-native GIS apps | GeoLibre R, RustGIS | `references/rustgis-and-geolibre-r.md` |
| Free/public geospatial services | Weather, DEM, imagery, tiles, OSM, biodiversity | `references/free-geospatial-apis.md` |
| Spatial engines / big data | GDAL, PROJ, GEOS, GeoRust, Rasterio | `references/geospatial-foundations.md` |
| Satellite imagery / AI | Open GeoAI libraries and research **with explicit source availability** | `references/remote-sensing.md`, `references/geoai-satellite-map.md` |

## Exact EarthMapper projects: verified distinction

- **[AliAlkazraji/EarthMapper](https://github.com/AliAlkazraji/EarthMapper)** — Windows GIS product/feature reference (WPF, WebView2, 2D/3D, DEM, Sentinel-2, local GeoAI). **Root currently contains only README.md**; no source code or open-source license available to reuse.
- **[HIT-SIRS/EarthMapper](https://github.com/HIT-SIRS/EarthMapper)** — academic bidirectional satellite↔map generation framework. Inspected repository has README, assets and Apache-2.0 LICENSE, **but no runnable implementation or weights**.
- **[rmkemker/EarthMapper](https://github.com/rmkemker/EarthMapper)** — distinct older remote-sensing segmentation reference.

Read [`references/earthmapper-case-studies.md`](references/earthmapper-case-studies.md) for practical building blocks, caveats and test criteria.

## Public GIS APIs and Rust/R integrations

- **[GeoLibre R](https://github.com/opengeos/geolibre-r)** — MIT R `htmlwidgets` binding for interactive GIS maps in RStudio, Shiny and Quarto.
- **[RustGIS](https://github.com/opengeos/RustGIS)** — Apache-2.0 Rust-native GIS application architecture, command bus, crates and WASM/plugin system; distinct from GeoRust.
- **[Free/public API guide](references/free-geospatial-apis.md)** — 18 curated climate, elevation, DEM, STAC, imagery, basemap, geocoding, OSM, soils and biodiversity services, with credentials, free-tier constraints and caveats.

The API guide **does not** treat public endpoints as unlimited or licensed for any use. SoilGrids REST is marked paused; OSMF tiles and Nominatim have restrictive public usage policies.

## Installation for coding agents

Install from the public repository `ahmadibrahim4geo/GIS-Development-Skills`:

```powershell
npx skills add ahmadibrahim4geo/GIS-Development-Skills --skill gis-development
```

Run inside a project to install to that project; `-g` installs globally. The public CLI is documented at https://github.com/vercel-labs/skills. The `npx` command requires Node.js; confirm your installation meets its current runtime requirements. The published repository is at **https://github.com/ahmadibrahim4geo/GIS-Development-Skills**.

For manual use, copy `skills/gis-development/` into the supported skills directory for your agent, or read `SKILL.md` directly.

## Examples

- "Build an ArcGIS Pro Python toolbox to validate polygons and preserve source attributes."
- "Create an ArcMap 10.8 script tool without Python 3 syntax."
- "Convert a geoprocessing algorithm to a QGIS Processing plugin, with a feature-level QA checklist."
- "Recommend a safe, open technology stack for a Windows GIS desktop app that opens GPKG, Shapefile, KML and GeoTIFF."
- "Compare CesiumJS, MapLibre, and GeoLibre for an offline-capable desktop viewer."

## Starter templates (not packaged GIS binaries)

- `templates/arcgis-pro-toolbox.pyt` — ArcGIS Pro Python toolbox example (copies features safely).
- `templates/arcmap-script-tool.py` — legacy ArcMap script-tool starter.
- `templates/qgis-processing-algorithm.py` — QGIS Processing algorithm starter.
- `templates/standalone-geojson-summary.py` — standard-library, non-destructive file checker.

## Catalog search (Python 3, no external packages)

```bash
python scripts/validate_catalog.py
python scripts/validate_api_catalog.py
python scripts/search_api_catalog.py --category terrain-elevation
python scripts/search_catalog.py --platform arcgis-pro
python scripts/search_catalog.py --query 3d
python -m unittest discover -s tests -v
```

The searchable data lives in [`references/project-catalog.json`](references/project-catalog.json). Project URLs and selected READMEs/root trees were checked during curation on 2026-10-24. **Entries are not a live feed**; check upstream documentation, branch, maintenance, version, security notices, license and service terms before adoption.

## Important safeguards

- Do not treat ArcMap (retired) and ArcGIS Pro as equivalent Python runtimes.
- Never copy third-party code into this repo without its actual license and attribution; linking is not the same as licensing derivative code.
- Verify coordinate reference systems, axis order, linear units, no-data behavior, geometry validity and data attribution.
- Never imply that an example runs in a proprietary GIS environment without testing it there.
- Do not use commercial or API-keyed basemap/terrain services unless licensing and credentials are agreed.

## Roadmap

1. **v0.1.0** — foundation skill, 25 curated references, 4 starter templates and local validation.
2. **v0.2.0** — EarthMapper source audit, Windows .NET stack, additional verified repository pointers, satellite-AI research separation.
3. **v0.3.0** — GeoLibre R / RustGIS source audit and public geospatial API catalog (18 providers) with independent validation and tests.
4. **v0.4 (planned)** — ArcGIS/QGIS environment integration, tested sample data, advanced parameter validation.
5. **v0.5 (planned)** — reference 2D/3D GIS desktop implementation with offline data tests and strict license tracking.

Community proposals and verified pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License and third parties

This repository's **original** scripts, templates and written guidance are MIT licensed; each linked project keeps its **own** license. The catalog does not grant rights to re-use upstream code, imagery, hosted services, trademarks, or data.