<p align="center">
  <img src="assets/readme-banner.svg" alt="GIS Development Skills — The Heart of Geospatial Innovation" width="1200">
</p>

<p align="center">
  <a href="https://github.com/ahmadibrahim4geo/GIS-Development-Skills"><img alt="Open source" src="https://img.shields.io/badge/Open%20Source-GitHub-172B3C?style=for-the-badge&amp;logo=github&amp;logoColor=white"></a>
  <a href="https://github.com/ahmadibrahim4geo/GIS-Development-Skills/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/ahmadibrahim4geo/GIS-Development-Skills?style=for-the-badge&amp;label=Stars&amp;color=F2F5F9&amp;labelColor=172B3C"></a>
  <a href="https://github.com/ahmadibrahim4geo/GIS-Development-Skills/forks"><img alt="GitHub forks" src="https://img.shields.io/github/forks/ahmadibrahim4geo/GIS-Development-Skills?style=for-the-badge&amp;label=Forks&amp;color=F2F5F9&amp;labelColor=172B3C"></a>
  <a href="CHANGELOG.md"><img alt="Documentation version v0.3.5, not a published software release" src="https://img.shields.io/badge/Docs-v0.3.5-2582ED?style=for-the-badge&amp;labelColor=172B3C"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/github/license/ahmadibrahim4geo/GIS-Development-Skills?style=for-the-badge&amp;label=License&amp;color=35D592&amp;labelColor=172B3C"></a>
  <a href="https://ahmadibrahim4geo.github.io/GIS-Development-Skills/"><img alt="Website status" src="https://img.shields.io/website?url=https%3A%2F%2Fahmadibrahim4geo.github.io%2FGIS-Development-Skills%2F&amp;style=for-the-badge&amp;label=Website&amp;labelColor=172B3C"></a>
  <a href="https://github.com/ahmadibrahim4geo/GIS-Development-Skills/actions/workflows/validate.yml"><img alt="Validation workflow status" src="https://img.shields.io/github/actions/workflow/status/ahmadibrahim4geo/GIS-Development-Skills/validate.yml?style=for-the-badge&amp;label=Tests&amp;labelColor=172B3C"></a>
</p>

## Build GIS tools, plugins and geospatial applications with a verifiable development workflow.

A practical development skill and curated reference hub for building reliable ArcGIS tools, QGIS plugins, 2D/3D mapping experiences, desktop applications, and geospatial data workflows.

<table width="100%">
  <tr>
    <td align="center" valign="top" width="16%">
      <a href="skills/arcgis-toolbox-engineering/SKILL.md"><img src="assets/readme-tools.svg" alt="" width="48" height="48"><br><strong>GIS Tools</strong></a><br>
      <sub>ArcGIS, QGIS<br>and Python tools</sub>
    </td>
    <td align="center" valign="top" width="16%">
      <a href="references/free-geospatial-apis.md"><img src="assets/readme-apis.svg" alt="" width="48" height="48"><br><strong>Geospatial APIs</strong></a><br>
      <sub>Datasets and<br>web services</sub>
    </td>
    <td align="center" valign="top" width="16%">
      <a href="skills/gis-development/SKILL.md"><img src="assets/readme-development.svg" alt="" width="48" height="48"><br><strong>Development</strong></a><br>
      <sub>Skills, examples<br>and templates</sub>
    </td>
    <td align="center" valign="top" width="16%">
      <a href="skills/geospatial-web-mapping/SKILL.md"><img src="assets/readme-maps.svg" alt="" width="48" height="48"><br><strong>Maps & 3D</strong></a><br>
      <sub>2D/3D mapping<br>and visualization</sub>
    </td>
    <td align="center" valign="top" width="16%">
      <a href="skills/gis-desktop-application-development/SKILL.md"><img src="assets/readme-desktop.svg" alt="" width="48" height="48"><br><strong>Desktop Apps</strong></a><br>
      <sub>Standalone GIS<br>applications</sub>
    </td>
    <td align="center" valign="top" width="16%">
      <a href="references"><img src="assets/readme-guides.svg" alt="" width="48" height="48"><br><strong>Guides & References</strong></a><br>
      <sub>Curated resources<br>and best practices</sub>
    </td>
  </tr>
</table>

<p align="center"><strong>7 installable GIS skills</strong> · <strong>104 curated geospatial references</strong> · <strong>18 public API sources</strong></p>

<p align="center">
  <a href="README.ar.md">العربية</a> ·
  <a href="skills/gis-development/SKILL.md">Install the core skill</a> ·
  <a href="references/project-catalog.json">Explore project catalog</a> ·
  <a href="CONTRIBUTING.md">Contribute</a> ·
  <a href="https://ahmadibrahim4geo.github.io/GIS-Development-Skills/">Project website ↗</a>
</p>

**Maintainer:** [Ahmed Ibrahim](https://github.com/ahmadibrahim4geo). This is an independent community engineering resource, not an official project of Esri, QGIS, GeoRust or other third-party catalog entries. **Documentation v0.3.5** is not a GitHub software release; starter code and GIS host integrations require separate runtime testing.

---

## What makes this different from an awesome-list?

This repository includes a **working agent skill**: step-by-step architecture selection, compatibility rules, geospatial correctness checks, GIS application pathways, and reference starter code. The catalog is supporting evidence, **not a code-vending collection**. A coding agent must establish requirements, consult the relevant reference, verify package APIs, implement, and test before claiming success.

## Quality audit and standalone GIS development (v0.3.5)

The full source/skill-pack integrity audit introduced:

- [Standalone GIS Desktop Application Development](skills/gis-desktop-application-development/SKILL.md) — a **seventh** independent agent skill covering Qt/PySide, Tauri/Rust, C# WPF/WebView2, geospatial engines, installers and real UI acceptance.
- [Desktop engineering and release checklist](references/desktop-application-engineering.md), including MIRSAD Desktop as a development-stage case study.
- `python scripts/validate_skill_pack.py` — offline checks of all skill frontmatters, local documentation links, website resources, and synchronized project/API/skill counters.
- [Technical audit and outstanding verification](docs/TECHNICAL_AUDIT_2026-10-24.md), with exact test limits and remaining host-runtime checks.

**Current inventory:** 104 curated code/data references, 37 API service entries and **7 installable skills**. The GitHub CI checks this repository's structure, not licensed ArcGIS execution, installed QGIS behavior, or a real Windows installer.

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
- **[Free/public API guide](references/free-geospatial-apis.md)** — 37 curated climate, elevation, DEM, STAC, imagery, basemap, boundaries, population, hazards, routing, ocean and biodiversity service entries, with credentials, free-tier constraints and caveats.

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

## Expanded free and public GIS APIs — 2026-10-24

The catalog now contains **37 provider/service entries** (19 additions): geoBoundaries, WorldPop, GeoNames, NASA FIRMS, NASA CMR/EONET, USGS Earthquake/Water, OpenAQ v3, Open-Meteo Air Quality/Flood, HeiGIT ohsome v2/openrouteservice, HDX HAPI, NOAA CO-OPS/CDO/ERDDAP, World Bank Indicators, and iNaturalist. The bilingual homepage reads the actual JSON directory with live filtering and access labels.

[Provider limitations and examples](references/free-geospatial-apis.md) · [Data discovery skill](skills/geospatial-data-discovery/SKILL.md). Free access does not automatically permit commercial usage, offline mirroring or credential embedding. Modeled, curated and observed records remain clearly distinguished.

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