# Geospatial Engine Comparison, Hard Gates & Benchmark Guide

> Used by [`scripts/compare_engines.py`](../scripts/compare_engines.py) and [`scripts/recommend_stack.py`](../scripts/recommend_stack.py) alongside [`engine-capability-profiles.json`](engine-capability-profiles.json), [`technology-compatibility.md`](technology-compatibility.md), and [`free-first-policy.md`](free-first-policy.md).

---

## 1. Mandatory Hard Exclusion Gates (`hard_gate`)

Every candidate is screened **before** weighted ranking. A candidate failing any gate receives `status = "rejected"` (or `needs-evidence` when unverified) and **cannot** win rank #1 even if its technical subscores are highest (`E12`–`E15`).

| Gate | Rule & Failure Condition | Resulting Status |
|---|---|---|
| **Security Quarantine** | `security_status == "quarantine-reference-only"` or unreviewed external agent skill | `rejected` (`quarantine-reference-only`) |
| **Free-First Cost / API** | When `free_only = true`: `cost_classification` in `{commercial, trial}`, `commercial-terms`, paid/keyed API requirement, or `"Required"` proprietary host dependency | `rejected` (`free-only-gate`) |
| **Unknown Cost / License** | When license status is `verify-upstream`, `cost_classification == "unknown"`, or required capability metadata is missing / `unknown` | `needs-evidence` (never auto-`eligible`) |
| **License Compatibility** | Copyleft (`GPL`/`AGPL`) embedded directly inside a non-compatible (`permissive-only`) target without approved `worker-service` / process isolation | `rejected` (`license-incompatible`) |
| **Platform & OS Support** | Required `target_os` missing from `supported_os`/`platforms` without `cross-platform` support or viable isolated worker boundary | `rejected` (`platform-unsupported`) |
| **Atomic Capability Fit** | Any mandatory atomic `capability_id` marked `unsupported` | `rejected` (`capability-unsupported`) |

---

## 2. Canonical Weighted Scoring Rubric (`100 Points Total`, Scale `0–5` per Criterion)

$$
\text{WeightedScore} = \sum_{i=1}^{7} \left(\frac{\text{score}_i}{5.0}\right) \times w_i, \quad \sum w_i = 100
$$

| # | Dimension Key | Default Weight (`w_i`) | What Is Measured (`0–5` Anchors) |
|---|---|---|---|
| 1 | `functional_capability` | **25** | Exact match rate across required & optional atomic capabilities (`documented` vs tested) |
| 2 | `geodetic_fidelity` | **20** | Explicit CRS/datum support, `Z`/`M`/NoData preservation, numerical tolerance rigor |
| 3 | `runtime_performance` | **15** | Documented/measured throughput, memory predictability, GPU/streaming support |
| 4 | `license_cost` | **15** | Permissiveness (`MIT`/`BSD`/`Apache`/`ISC` = 5; `LGPL` dynamic = 4; `GPL` isolated = 3; gated/commercial = 0–1) |
| 5 | `integration_cleanliness` | **10** | Native language/ABI alignment, clean contracts, zero GDAL/Qt DLL collision |
| 6 | `deployment_footprint` | **10** | Standalone weight, offline/no-key capability, clean-machine redistributability |
| 7 | `maintenance_hygiene` | **5** | Community/OSGeo governance, documentation clarity, security hygiene (`trust_level`) |

> **Close-Score & Missing-Metric Rule (`E16`):** When top candidates lack empirical benchmark fields (`cold_start_ms`, `peak_rss_mb`, `throughput`, `accuracy_delta`), emit explicit `missing_metrics` + a PoC benchmark plan instead of synthesizing fake tiebreak numbers.

---

## 3. Ten Canonical Pair / Stack Comparisons (`V2 §10.3`)

1. **GDAL/OGR vs QGIS Core vs Rasterio/pyogrio vs GeoPandas:** Use pure `GDAL/OGR`, `Rasterio`, `pyogrio`, or `GeoPandas` for lightweight CLI/batch pipelines without dragging Qt/QGIS GUI overhead; pick `QGIS Core/Processing` when project files, symbology/layouts, or QGIS providers are required. Pin one GDAL/PROJ installation (`E17`).
2. **MapLibre GL JS vs OpenLayers vs Leaflet:** Pick `MapLibre GL JS` for smooth WebGL vector tiles & pitch/tilt; pick `OpenLayers` for non-Mercator custom projections (`EPSG:32636`, polar), OGC WFS-T/WMTS, and complex vector editing; pick `Leaflet` only for ultra-lightweight GeoJSON/XYZ overlays without vector tiles or custom projections.
3. **CesiumJS / Cesium Native vs osgEarth vs Three.js:** Pick `CesiumJS` (Web/WebView2) or `Cesium Native` (C++ desktop) for global WGS84 ellipsoids, quantized-mesh terrain, and 3D Tiles; pick `osgEarth` for native OpenSceneGraph C++ desktop globes; pair `Three.js` / camera-relative local origins (`ENU`) only for small localized urban/CAD scenes without built-in global geodesy.
4. **QGIS vs GRASS GIS vs SAGA GIS vs WhiteboxTools:** Use `WhiteboxTools` (MIT core) or `GDAL` when permissive distribution matters; use `GRASS GIS` (`r.watershed`, topology) or `QGIS Processing` / `SAGA` cleanly via isolated subprocess/worker when `GPL` isolation is maintained.
5. **SNAP Engine vs Orfeo ToolBox (OTB) vs Rasterio/xarray:** Select `SNAP` (`ESA`) only when Sentinel-1/SAR radiometric/interferometric calibration or S2/S3 mission toolboxes justify JVM overhead; select `OTB` for C++ orthorectification/segmentation/OBIA pipelines; select `Rasterio` + `rioxarray` + `dask` for COG/STAC cloud spectral indices (`NDVI`, `NDWI`, `NBR`).
6. **PostGIS vs DuckDB Spatial vs SpatiaLite:** Select `PostGIS` for concurrent multiuser transactions, MVTs (`ST_AsMVT`), topology, and server persistence; select `DuckDB Spatial` (MIT) for analytical in-memory OLAP over GeoParquet/Arrow; select `SpatiaLite` / GeoPackage for single-file offline desktop/mobile local storage.
7. **OSRM vs Valhalla vs GraphHopper vs pgRouting:** Select `Valhalla` for multimodal/time-dependent routing, isochrones, map-matching, and compact tiled memory footprint; `OSRM` for ultra-fast static CH car matrix throughput; `GraphHopper` for customizable Java elevation/speed profiles; `pgRouting` when graph edits happen live inside PostgreSQL transactions.
8. **Qt 6 (PySide6 / SARibbon / Qt-ADS) vs .NET WPF (Fluent.Ribbon / AvalonDock) vs Tauri / WebView2:** Select `Qt 6` + dynamic LGPL UI libs (`SARibbon`, `Qt-ADS`) for deep C++ GDAL/QGIS/OCCT desktop apps; select `.NET WPF` (`Fluent.Ribbon` + `Mapsui`/`WebView2`) for Windows enterprise shells with isolated Python/QGIS `worker-service`; select `Tauri` when sharing a modern TypeScript web UI (`MapLibre`/`Cesium`) with lightweight Rust backend IPC.
9. **Open CASCADE (OCCT) vs FreeCAD vs CGAL / Clipper2 / earcut:** Use `earcut` (ISC) & `Clipper2` (BSL-1.0) for fast 2D footprint triangulation, booleans, and parcel setbacks; use `CGAL` for exact computational geometry / 3D meshes (`GPL/LGPL` boundary awareness); use `OCCT` (`LGPL-2.1`) or headless `FreeCAD`/`CadQuery` for parametric B-Rep CAD solids and STEP/IGES export.
10. **PDAL vs LASpy / COPC vs CloudCompare / Entwine:** Use `PDAL` for streaming point-cloud pipelines, ground classification (`SMRF`), and COG/COPC conversion; use `laspy` (`lazrs`) for lightweight Python LAS/LAZ array reads; use `COPC` + `Entwine` + `Potree` for browser LOD streaming without loading full point clouds into RAM.

---

## 4. Repeatable PoC Benchmark Protocol (`V2 §32.1`)

Never report unmeasured speedups (`"10x faster"`). Any cross-engine performance claim must execute the same golden fixture on pinned software versions and record:

1. **Test Conditions:** Hardware specs (`CPU`, `RAM`, `GPU`, `OS`, storage SSD), exact package version/SHA, pinned `PROJ`/`GDAL` paths, thread count, and warmup vs cold cache state.
2. **Timed Phases:** Cold startup latency (`ms`), warm repeat latency (median & `p95` across ≥ 5 runs), and peak RSS/VRAM (`MB`).
3. **Correctness Gate:** Independent verification of feature counts, CRS `EPSG` preservation, planar vs geodesic area/length tolerance (`<= threshold`), NoData integrity, and clean serialization roundtrip before comparing speed.
4. **Honesty Rule:** If no local execution ran, set benchmark metrics to `NOT RUN` and `poc_benchmark_required: true`.
