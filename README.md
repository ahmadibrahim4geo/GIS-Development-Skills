<p align="center">
  <img src="assets/brand/banner-dark.svg" alt="GIS Development Skills — The Heart of Geospatial Innovation" width="1200">
</p>

<p align="center"><sub>Official vector identity: <a href="assets/brand/README.md">brand assets and usage guide</a> · <a href="assets/brand/logo-light.svg">transparent logo</a> · <a href="assets/brand/icon.svg">standalone icon</a></sub></p>



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

<p align="center"><strong>21 installable GIS skills</strong> · <strong>148 curated geospatial references</strong> · <strong>52 public API sources</strong> · <strong>24 curated data repositories</strong></p>

<p align="center">
  <a href="README.ar.md">العربية</a> ·
  <a href="skills/gis-development/SKILL.md">Install the core skill</a> ·
  <a href="references/project-catalog.json">Explore project catalog</a> ·
  <a href="CONTRIBUTING.md">Contribute</a> ·
  <a href="https://ahmadibrahim4geo.github.io/GIS-Development-Skills/">Project website ↗</a>
</p>

## Agent Development Journal & Project Memory — 25 October 2026

The new [Agent Development Journal skill](skills/agent-development-journal/SKILL.md) adds project-local **numbered reports** for every user requirement, implementation milestone, revision, cancellation and verification. Its [offline Python journal tool](scripts/development_journal.py) creates immutable linked JSON records and generated Markdown reports/INDEX.md/STATE.md in each target project's `.agent-development-log/`. See [recovery and lifecycle](references/agent-development-journal-guide.md), [external skills comparison](references/agent-memory-skill-references.md) and [offline example](examples/development-journal/README.md).

Reviewed inspirations: [Planning with Files](https://github.com/OthmanAdi/planning-with-files), [Superpowers](https://github.com/obra/superpowers), [GitHub Spec Kit](https://github.com/github/spec-kit), without copying their hooks or tools. The **hosting agent must invoke the logger** at action checkpoints; it does not automatically monitor processes, execute code or reverse Git commits.

## Prompt Intent & Execution Orchestrator — 25 October 2026

The new [installable orchestration skill](skills/prompt-intent-orchestrator/SKILL.md) converts informal Arabic/English requests into explicit, testable requirements and task dependencies. Users review, edit and approve each plan revision before implementation. The agent then selects [existing GIS specialists](skills/gis-development/SKILL.md), actual available tools, [GIS Security Guardian](skills/gis-security-guardian/SKILL.md), and T0–T4 acceptance tests.

Read the [workflow contract](references/intent-orchestration-workflow.md), [ZEarth example plan](examples/intent-orchestrator/README.md) and [offline JSON validator / keyword hints](scripts/intent_router.py). The helper is **not** an AI model, does not authenticate user approval and does not execute GIS software; native behavior still requires host tests.

## Google Earth Pro engineering and historical imagery — 2026-10-25

The [Google Earth Pro engineering reference](references/google-earth-pro-engineering.md) extracts practical, independently implementable features from the historical [Google Earth Blog](https://www.gearthblog.com/): Places drag/drop and bulk actions, NetworkLink/Region/LOD, KML/KMZ fidelity, tours, elevation profiles and raster overlays. The dedicated [Historical Imagery Timeline guide](references/historical-imagery-timeline.md) specifies a compact, non-blocking dock, *actual scene dates* rather than invented years, source attribution, playback, licensed multi-provider retrieval and same-viewport image comparison. Links are integrated with the [Desktop](skills/gis-desktop-application-development/SKILL.md), [Web/3D](skills/geospatial-web-mapping/SKILL.md), [KML/KMZ](skills/kml-kmz-engineering/SKILL.md) and core router skills and shown on the bilingual site.

**Status:** documented engineering and static checks only; not a shipped or tested ZEarth historical-imagery implementation. Google Earth Blog is an independent, largely historical source, and its content does not license Google imagery for third-party use.

## Official Esri developer references — 25 October 2026

Ten additional official Esri repositories have been reviewed and linked without duplicate entries in the [Esri integration matrix](references/esri-open-source-integration.md): ArcGIS Pro SDK AI snippets, Arcade profiles, developer troubleshooting, CAD/BIM, network analysis, Geoportal STAC/MCP, JavaScript, geocoding, elevation and raster deep learning.

**Practical additions:** the [offline ArcGIS Pro Python package compatibility checker](references/esri-python-environment-compatibility.md) compares locally observed packages with the original Esri version matrix without modifying the environment. The [Arcade profile guide](references/arcgis-arcade-profiles.md) routes labeling, popup, visualization, attribute rules, dashboard and form expressions safely.

Apache-2.0 sample-code licenses do not grant rights to proprietary ArcGIS products, extensions, SDK runtimes, hosted services, map imagery, third-party models or personal credentials. No Esri proprietary binaries were copied and no ArcGIS-native execution is claimed.

## GIS Security Guardian — cross-cutting protection (25 October 2026)

[**GIS Security Guardian**](skills/gis-security-guardian/SKILL.md) is the 19th installable skill. It accompanies every routed GIS task with permission boundaries, prompt-injection precautions, safe geospatial archive handling, credential and API hygiene, and evidence-based release gates. The [security tool registry](references/security/security-tools.json) links 14 upstream projects, distinguishing local from potentially networked analysis and reporting license status without bundling third-party code. [Offline security audit](scripts/security_audit.py), [archive guard](scripts/security_guardian.py), [unit tests](tests/test_security_guardian.py), [dedicated workflow](.github/workflows/security.yml), [security disclosure policy](SECURITY.md), and the [bilingual homepage](index.html) are included. The stdlib preflight runs without subscriptions or keys; external scanners such as Gitleaks, Bandit, Cisco Skill Scanner, OSV-Scanner and zizmor remain optional and are **not claimed to have run**. Static validation cannot establish full runtime security.

**Free-first audit:** [Cost/licensing and 19 independent skill paths](references/free-first-policy.md). The website now lists all specialists, has incremental project browsing instead of a hard 60-result cut-off, and defaults API discovery to 43 self-hostable or conditionally free entries. Commercial, trial, strictly restricted and unavailable records remain optionally viewable; live provider rights are not guaranteed.

**Practical free workflow upgrade (2026-10-25):** [Original upstream license-file audit](references/upstream-license-audit.md) (8 inspected / 138 linked projects), [offline license evidence scanner](scripts/audit_license_catalog.py), and two complete dependency-free T2 fixtures: [DEM Horn slope](examples/terrain-slope/README.md) and [STAC metadata selection](examples/stac-offline/README.md). The example scripts output real ASCII elevation-slope or JSON metadata files, but **do not** validate external terrain CRS or live satellite services. Upstream data, models, proprietary GIS host and API terms remain independent.

**Maintainer:** [Ahmed Ibrahim](https://github.com/ahmadibrahim4geo). This is an independent community engineering resource, not an official project of Esri, QGIS, GeoRust or other third-party catalog entries. **Documentation v0.3.5** is not a GitHub software release; starter code and GIS host integrations require separate runtime testing.

---

## Google KML/KMZ fidelity upgrade — 2026-10-25

The existing [KML/KMZ Engineering skill](skills/kml-kmz-engineering/SKILL.md) now follows an expanded [Google/OGC interoperability guide](references/google-kml-kmz-compatibility.md) and an [offline styled KML fixture](examples/kml-kmz/README.md). Import must respect **the user's original icons, colors, opacity, shared/highlight styles, folders, ExtendedData, altitude, time and bundled assets** rather than imposing app-wide defaults. View, loss-aware conversion, edit and export are separate modes. KML `aabbggrr` colors, KMZ relative paths, `gx:` extensions, security and explicit target-host acceptance gates are documented. This is documentation and XML contract testing, **not** proof that Google Earth, Cesium or ZEarth Desktop has already passed a rendered round-trip.

## Cartography & device context specialists — 2026-10-25

Two new installable skills extend the toolkit to **18 specialists** (including the recently added [KML/KMZ specialist](skills/kml-kmz-engineering/SKILL.md)):

- [GIS Cartography & Symbology](skills/gis-cartography-symbology/SKILL.md) — vector point/line/polygon symbols, raster ramps, labels, accessible layouts, ArcMap/Pro/QGIS/MapLibre/Cesium adapters and verifiable save/reopen.
- [GIS Device Context](skills/gis-device-context/SKILL.md) — UTC/local date/time, IANA timezone, opt-in device geolocation, scene-vs-device target and live/simulated Sunlight modes.
- [19-source style directory (including 8 icon packs and Cesium PinBuilder)](references/cartographic-style-sources.json), including the [ArcMap Style Collection](https://github.com/ahmadibrahim4geo/ArcMap-Style-Collection), QGIS Resources, OS GeoDataViz, CARTOColors and scientific palette references. Upstream individual style/font rights are **not** automatically granted by hosting.
- Offline [MapLibre point/line/polygon fixture](examples/cartography/README.md) and [Python timezone/context fixture](examples/device-context/README.md) with regression tests; real GIS rendering, GPS permission and sun lighting still require host testing.

The bilingual website adds a searchable **Style sources** catalog tab alongside the existing project, API and data tabs. No third-party style binaries or fonts are bundled.

**Unified GIS Icon Manager (2026-10-25):** [General-use symbol library specification](references/unified-gis-icon-manager.md) covers ArcGIS/QGIS/Cesium/MapLibre/desktop GIS with a **dedicated KML/KMZ new-feature adapter**, not a separate icon library. Try the [offline bilingual SVG/PNG creator](examples/icon-manager/index.html) and [Python new-only KMZ packager](examples/icon-manager/export_new_kmz.py). Source catalog grows to **21** by adding [Streamline](https://www.streamlinehq.com/icons/tag/google-earth-placemark) as mixed-license discovery (not a redistributable standard free-icon picker), [Mapular](https://mapular.com/tools/map-icon-creator) as generator-design reference (site code unlicensed for reuse) and 2026 SVG/PNG support in CC BY-SA Map Icons Collection. **Imported KMZ originals never receive automatic restyling.** The working example is **not installed in ZEarth**.

**Free map marker libraries and imported KMZ styles:** The [map marker icon guide](references/map-marker-icon-library.md) covers Pinhead, Maki, Temaki, Map Icons Collection, Scott de Jonge Map Icons, Leaflet ExtraMarkers, Google Material Symbols, Leaflet AwesomeMarkers, and Cesium PinBuilder, including separate icon/font/plugin licenses. These can style **new/user-restyled** placemarks. On imported KML/KMZ, **preserve original icon assets, styles, colors, StyleMap, opacity and line/polygon and label appearances, without automatic replacement**. See the [KML/KMZ preservation contract](references/kml-kmz-symbol-preservation.md) and [offline KMZ comparison fixture](examples/kml-style-preservation/README.md). This strengthens (does not replace) the existing [Google/OGC KML compatibility guide](references/google-kml-kmz-compatibility.md).

## Global Mapper / Blue Marble Geographics research — 2026-10-25

Added a [Global Mapper Development specialist](skills/global-mapper-development/SKILL.md) and [Blue Marble commercial SDK / GitHub fork reference](references/blue-marble-global-mapper.md). Curated **7 official-organization forks and 1 independent community GMS scripting repository**, bringing the software catalog to **138 references**. The official organization repositories are forks, **not** source releases of the proprietary Global Mapper engine; use commercial SDK only with required development/redistribution licenses. The bilingual [index.html](index.html), lightweight router, desktop, terrain and web/3D specialists and derived manifest are synchronized. No commercial SDK binary is included.

## Earth View satellite globe reference — 2026-10-25

Added [Earth View](https://github.com/colincode0/earth-view) to our [software catalog](references/project-catalog.json), with a [technical architecture review](references/earth-view-architecture.md) linked from the bilingual website, Web Mapping, Desktop, Remote Sensing and API specialists. NASA GIBS and Copernicus Data Space were **already** indexed as APIs, so we did not duplicate them. The [atomic source intake checklist](references/source-intake-workflow.md) helps keep future changes synchronized. **Upstream license not found; architecture reference only, no code copied.**

## OpenGeoS advanced engineering and GIS data repositories — 2026-10-25

The toolkit now curates **24 GIS data source directories and portals** separately from its **52 API records** and **129 software references**. It **links** the user's [GIS Data Repositories Professional 2026](https://github.com/ahmadibrahim4geo/gis-data-repositories-professional-2026) (its own 2,660+ source master index) rather than duplicating those records. New [data repositories explorer](index.html), [24-entry JSON catalog](references/geospatial-data-repositories.json) and [data-provider guide](references/geospatial-data-repositories.md) distinguish an index, a real STAC API, and the actual downloadable scientific asset.

**New installable specialists:** [Data Repositories](skills/geospatial-data-catalogs/SKILL.md), [Geospatial AI Agents](skills/geospatial-ai-agents/SKILL.md) and [Terrain / Hydrology / LiDAR](skills/terrain-hydrology-lidar/SKILL.md). New [OpenGeoS advanced integration review](references/opengeos-advanced-integration.md) and an offline [directory query example](examples/data-catalogs/README.md) show source selection and reproducibility. None of the listed software, data access, or native GIS integration is certified by documentation-only inspection.

## Geocoding & place search — 2026-10-25

The **52-service API directory** now includes **15 cost-ranked geocoding and geographic place-name providers**: Pelias, Photon, Open-Meteo, Nominatim, GeoNames, Geoapify, LocationIQ, geocode.maps.co, Esri, MapTiler, OpenCage, Google Places, Mapbox, HERE and TomTom.

Read the [free-to-commercial selection guide](references/geocoding-place-search.md), with Arabic usage notes and sample requests; or browse [the live bilingual catalog](https://ahmadibrahim4geo.github.io/GIS-Development-Skills/). Production use rights are independent of daily free credits: OpenCage's 2,500/day tier is **for testing only**; Nominatim's OSMF server **prohibits autocomplete**.

This is a source/skill improvement, not a claim of a tested live API or a completed application integration.

## GIS Agent Operating System

The core skill is now a lightweight router with [the complete previous guidance preserved](references/gis-development-full-guidance.md) and a [decision tree](references/agent-decision-tree.md). New resources: [evidence form](templates/GIS_ACCEPTANCE_REPORT.md), [evidence validation](scripts/validate_evidence.py), [test fixtures](fixtures/README.md), [native GIS harness](native_tests/README.md), [security](references/geospatial-security.md), [performance](references/geospatial-performance.md), [before/after examples](references/gis-antipatterns.md), [generated manifest](references/repository-manifest.json) and [weekly provider checks](docs/SERVICE_MONITORING.md).

Previous skills, original guidance, project/API references, brand assets and bilingual content are preserved; native and live provider verification remain separate.

## Production GIS workflows and quality benchmark — 2026-10-24

**Additive upgrade, without deleting any earlier skills, reference sources, templates or site features:** this repository now includes **11 installable GIS agent skills**, **104 curated project references** and **52 public GIS API entries**.

- [Spatial Databases](skills/spatial-databases/SKILL.md): PostGIS/SpatiaLite, spatial indexing and measured query plans.
- [Geospatial Data Processing](skills/geospatial-data-processing/SKILL.md): vector/raster pipelines, safe coordinate transformations and reproducible checks.
- [Remote Sensing Pipelines](skills/remote-sensing-pipelines/SKILL.md): STAC/COG, Earth Engine, radiometric QA and aligned raster grids.
- [Reproducible engineering examples](examples/README.md): topology audit, modeled weather to GeoJSON, batch map PDF export, PostGIS SQL and STAC/COG checklist.
- [GIS Quality Benchmark](docs/QUALITY_BENCHMARK.md): T0–T4 test-evidence levels and native GIS acceptance requirements.
- [Production workflow reference](references/production-workflows.md): implementation safeguards, test limits and examples.

Network and weather examples have synthetic offline fixtures for deterministic unit tests. ArcGIS/QGIS/PostGIS/Windows and live-provider acceptance still need real host evidence.

## What makes this different from an awesome-list?

This repository includes a **working agent skill**: step-by-step architecture selection, compatibility rules, geospatial correctness checks, GIS application pathways, and reference starter code. The catalog is supporting evidence, **not a code-vending collection**. A coding agent must establish requirements, consult the relevant reference, verify package APIs, implement, and test before claiming success.

## Quality audit and standalone GIS development (v0.3.5)

The full source/skill-pack integrity audit introduced:

- [Standalone GIS Desktop Application Development](skills/gis-desktop-application-development/SKILL.md) — a **seventh** independent agent skill covering Qt/PySide, Tauri/Rust, C# WPF/WebView2, geospatial engines, installers and real UI acceptance.
- [Desktop engineering and release checklist](references/desktop-application-engineering.md), including MIRSAD Desktop as a development-stage case study.
- `python scripts/validate_skill_pack.py` — offline checks of all skill frontmatters, local documentation links, website resources, and synchronized project/API/skill counters.
- [Technical audit and outstanding verification](docs/TECHNICAL_AUDIT_2026-10-24.md), with exact test limits and remaining host-runtime checks.

**Current inventory:** 138 curated software references, 52 API service entries, 24 data repositories and **15 installable skills**. The GitHub CI checks this repository's structure, not licensed ArcGIS execution, installed QGIS behavior, or a real Windows installer.

```bash
python scripts/validate_catalog.py
python scripts/validate_api_catalog.py
python scripts/validate_skill_pack.py
python -m unittest discover -s tests -v
```

## Tested-source references from our own GIS projects (v0.3.3)

**104 curated software projects and eight installable agent skills.** Five public source projects developed or curated by Ahmad Ibrahim are now documented as real engineering case studies, including native ArcGIS toolboxes and a standalone Desktop migration path:

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
- **[Free/public API guide](references/free-geospatial-apis.md)** — 52 curated climate, elevation, DEM, STAC, imagery, basemap, boundaries, population, hazards, routing, ocean and biodiversity service entries, with credentials, free-tier constraints and caveats.

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

## GEBCO_2026 — global land/ocean bathymetry and terrain

Two official GEBCO_2026 access methods are indexed: the [WMS](https://www.gebco.net/data-products/gebco-web-services/web-map-service) for ocean/land terrain visualization, and [CEDA OPeNDAP](https://www.gebco.net/data-products/gridded-bathymetry-data) for numeric 15 arc-second bathymetry and topography data. Also documented: the official GeoTIFF/NetCDF/ASCII subset download interface and **TID source-type grid**. Public-domain data with attribution, **not for marine navigation**. See the [scientific usage notes](references/free-geospatial-apis.md).

**Current directory: 39 GIS API entries and eight installable skills.** The 37-entry expansion below is a historical milestone.

## Expanded free and public GIS APIs — 2026-10-24

The catalog now contains **37 provider/service entries** (19 additions): geoBoundaries, WorldPop, GeoNames, NASA FIRMS, NASA CMR/EONET, USGS Earthquake/Water, OpenAQ v3, Open-Meteo Air Quality/Flood, HeiGIT ohsome v2/openrouteservice, HDX HAPI, NOAA CO-OPS/CDO/ERDDAP, World Bank Indicators, and iNaturalist. The bilingual homepage reads the actual JSON directory with live filtering and access labels.

[Provider limitations and examples](references/free-geospatial-apis.md) · [Data discovery skill](skills/geospatial-data-discovery/SKILL.md). Free access does not automatically permit commercial usage, offline mirroring or credential embedding. Modeled, curated and observed records remain clearly distinguished.

Install the dedicated [Geospatial API Integration Skill](skills/geospatial-api-integration/SKILL.md) to build reliable service clients for the new providers. It complements [Geospatial Data Discovery](skills/geospatial-data-discovery/SKILL.md) by covering credentials, pagination, rate controls, provenance, GIS outputs and error-path testing.

~~~bash
npx skills add ahmadibrahim4geo/GIS-Development-Skills --skill geospatial-api-integration
~~~

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

### World Gazetteer: search and reference labels

The [World Gazetteer implementation guide](references/world-gazetteer-reference-layer.md) adds offline-first GeoNames name search and an **independent, scale-aware Reference Layers overlay** for desktop/web GIS (especially future ZEarth integration). It specifies label priority, zoom/detail categories, Arabic/English names, map collision/3D culling, attribution, and preservation of user KML/KMZ styles. A [Python/SQLite 2D demonstrator with unit tests](examples/gazetteer/README.md) is included; it is **not** a completed native GIS/desktop integration.
