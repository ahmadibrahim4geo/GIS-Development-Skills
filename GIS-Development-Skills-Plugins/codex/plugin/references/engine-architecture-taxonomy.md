# Unified Geospatial Software Taxonomy, Build Models & Intent Guide

> **Status:** Authoritative P01 reference (`Engine Architecture Reuse Plan V2` §§3–4, §22.1, §33).  
> **Related policy:** [Build vs Reuse Policy](build-vs-reuse-policy.md) · [Free-First Policy](free-first-policy.md) · [UI & Engine Contract](ui-engine-architecture-contract.md) · [Atomic Capability Taxonomy](engine-capability-taxonomy.json).

---

## 1. Software Entity Taxonomy (24 Canonical Types)

Distinguish component roles precisely instead of calling every framework or viewer a GIS engine. A single product may carry one `primary_role` plus zero or more `secondary_roles` (for example: QGIS Desktop = `application`; QGIS Core = `core` / `library`; QGIS Processing = `engine`; QGIS Server = `service`). Ambiguous names such as **`UI.js` / `UJS`** stay marked **`unresolved`** until repository URL, package identity, role, version, and license are verified—never infer `Vue.js` from spelling similarity.

| # | Entity Type | Practical Engineering Meaning | Representative Examples | Mandatory Verification Questions |
|---|---|---|---|---|
| 1 | `Application` | Complete interactive or CLI end-user product | QGIS Desktop, FreeCAD | Use as host, study as behavioral reference, or evaluate source fork? |
| 2 | `Engine` | Specialized subsystem coordinating complex domain operations | CesiumJS, GRASS GIS | Verified atomic capabilities, limits, threading, and boundaries? |
| 3 | `Core` | Foundational non-UI model/data layer depended on by higher shells | QGIS Core (`src/core`) | What lives in Core vs GUI vs Processing? |
| 4 | `Kernel` | Specialized mathematical/geometric computation core | Open CASCADE (OCCT) | Numerical precision, tolerances, boolean robustness? |
| 5 | `Library` | Directly callable API library linked/imported in code | GDAL/OGR, GEOS, PROJ | Language bindings, ABI, license, packaging size? |
| 6 | `Framework` | Application shell/lifecycle/UI/routing scaffolding | Qt, WPF, Vue, Flutter | Target OS, RTL, accessibility, docking, NOT a GIS engine |
| 7 | `Renderer` | Visual display engine for geometry, tiles, styles, cameras | MapLibre GL JS, OpenLayers, Leaflet | Projection support, label collision, picking (Rendering != Analysis) |
| 8 | `Graphics API` | Low-level GPU drawing/compute interface | Vulkan, WebGPU | Driver complexity; not ready-made GIS cartography |
| 9 | `SDK` | Bundled dev libraries, headers, docs, build tooling | ArcGIS Pro SDK, Cesium Native | Does runtime work standalone without a commercial host? Terms? |
| 10 | `API` | Local or remote programmatic interface contract | PyQGIS, OGC API Features | Version pinning, auth, rate/area limits, error semantics |
| 11 | `Runtime` | Execution environment binaries, assets, shared libraries | .NET Runtime, QGIS runtime, Qt | Bundling rights, clean-machine dependencies, VC++/PROJ grids |
| 12 | `Binding/Wrapper` | Language bridge exposing a native core in another language | pyproj, Shapely, GDAL Python | Exact underlying native version, ABI, GIL/memory ownership |
| 13 | `Adapter` | Interface wrapper isolating component specifics behind project contract | `ICrsTransformer` adapter | Prevents leaking vendor types into domain contracts |
| 14 | `Plugin/Add-in` | Extension hosted inside and bound to parent host lifecycle | QGIS plugin, ArcGIS Pro add-in | Host API constraints, host install/license requirement |
| 15 | `Fork` | Derivative maintained from an upstream open-source codebase | Cleaned QGIS fork | GPL/upstream compliance, patch queue, rebase maintenance cost |
| 16 | `Starter/Template` | Customizable project seed repository | QGIS plugin template, WEB-01..18 | Upstream template license vs user product license |
| 17 | `Reference application` | Product studied cleanly for workflow behavior without asset copying | ArcGIS Pro, Google Earth Pro | Clean-room behavioral boundary; never copy binaries/icons/DAML |
| 18 | `CLI` | Non-GUI executable command workflow | `gdalwarp`, `qgis_process` | Exit codes, safe arg-array invocation, output readback |
| 19 | `Service` | Process accessed over IPC, localhost socket, or HTTP/gRPC | GeoServer, OSRM, Martin, TiTiler | Local vs cloud cost, auth, SSRF, network offline fallback |
| 20 | `Algorithm/Recipe` | Specific spatial method or pipeline definition | D8 flow accumulation, NDVI | Units, NoData/QA handling, numeric tolerances |
| 21 | `Model` | Scientific physical solver or ML/GeoAI architecture + weights | MODFLOW 6, SWMM, SAM2 | Weight license separate from code, calibration boundaries |
| 22 | `Standard/Format` | Interoperability specification or geospatial data container | GeoPackage, OGC API, IFC, 3D Tiles | Per-driver feature loss (Z/M/CRS/styles/IDs), not just file extension |
| 23 | `Asset` | Icons, fonts, textures, sprites, sample models, basemap tiles | Lucide, Material Symbols, OSM data | Asset/tile license distinct from code license (e.g., OSM ODbL != tiles) |
| 24 | `Package/Distribution` | Delivery/installer container and environment manager | OSGeo4W, NuGet, pip, MSI/ZIP | Never confuse package manager or installer format with underlying engine |

---

## 2. Architecture & Build Models Matrix (11 Canonical Modes + Compositions)

Combine modes explicitly at the component level when warranted (for example: `reference-inspired-ui` + `embedded-engine` + `worker-service`). Never translate «like QGIS» blindly into a fork, «QGIS engine» blindly into a plugin, or «Ribbon» blindly into ArcGIS SDK.

| Build Model ID | Meaning | Code / UI Origin | Runtime Dependencies | When to Select |
|---|---|---|---|---|
| `extend-host` | Plugin, script tool, or add-in inside existing host | Host public APIs (PyQGIS, Pro SDK, ArcPy) | Host installed (+ licensed if commercial) | User explicitly wants tools operating inside QGIS or ArcGIS |
| `configure-host` | Simplify/restructure host via profiles, settings, toolbars | Host supported config/profiles | Host installed | Hide clutter or tailor UI without maintaining a source fork |
| `source-fork` | Maintain customized derivative of open-source app | Upstream source pinned to tag/SHA | Full app build + runtimes (e.g., Qt/QGIS) | User needs host shell/menus/editing architecture with deep changes |
| `source-component-reuse` | Extract/adapt license-compatible modules from upstream | Selected upstream widgets/algorithms | Compatible module dependencies | Needs proven panels/algorithms without adopting full app shell |
| `embedded-engine` | Original UI shell built directly over linkable engine libs | Original UI + Core/GUI library bindings | Bundled or discovered runtime | Standalone app backed by QGIS Core/GUI, GDAL, MapLibre Native |
| `ui-shell-migration` | Replace/reorganize UI layer while retaining backend engine | New UI + command parity adapters | Existing engine intact | User requests Ribbon or new shell without swapping computation/render |
| `reference-inspired-ui` | Original clean-room UI modeled on reference workflow patterns | Original code + free/licensed assets | Independent; zero reference binaries | Wants ArcGIS Pro or Google Earth Pro workflow freely and legally |
| `multi-engine-composition` | Compose best engine per capability behind shared contracts | Coordinator + typed adapters | Multiple compatible runtimes | Diverse needs across 2D, 3D Globe, CAD/BIM, Remote Sensing, Simulation |
| `worker-service` | Isolate incompatible engine/language in external process/IPC | CLI / JSON-RPC / local HTTP service | Worker env isolated cleanly | Calling Python/GDAL/QGIS headless processing from WPF/.NET/JS shell |
| `custom-component` | Develop missing narrow feature atop verified primitives | Original component code + ADR | Project runtime only | Proven capability gap after exhausting catalog & OSS search |
| `custom-engine` | Purpose-built low-level geospatial or rendering engine | Original architecture + math/GPU | Low-level graphics/IO libs | Explicit strategic product goal; never default recommendation |

---

## 3. Colloquial Arabic & English Intent Disambiguation Patterns (27 Canonical Cases)

| # | User Request Pattern (AR / EN) | Initial Architectural Interpretation | Disallowed Assumption |
|---|---|---|---|
| 1 | «عايز أعمل تطبيق جيس على الموبايل يشتغل أوفلاين» | Mobile Field GIS (`M01/M03`) + GeoPackage/SQLite + sync outbox | Do not treat PWA or WebView screenshot as tested native app |
| 2 | «أنا محتاج محرك ثلاثي الأبعاد للويب والديسكتوب» | 3D Globe engine selection (`CesiumJS` / `osgEarth` / `MapLibre`) | Do not treat 3D viewer alone as full GIS editor |
| 3 | «عايز أعيد استخدام كود أو مكتبات QGIS» | Evaluate `source-component-reuse` / `embedded-engine` | Do not pretend non-Qt shell embeds `QgsMapCanvas` directly |
| 4 | «خد QGIS نفسه ونضفه وسيب التحرير والأدوات دي» | Evaluate `configure-host` first, then `source-fork` (`KEEP/HIDE/REMOVE`) | Never delete Core, CRS, Undo, Save, or provider registry without dependency map |
| 5 | «عايز QGIS بس بواجهة Ribbon زي ArcGIS Pro» | QGIS Qt Ribbon customization / independent shell + ArcGIS UX reference | Never pull ArcGIS Pro runtime/DAML or assume free commercial parity |
| 6 | «نفس شاشة وواجهة Google Earth Pro بس مجانية» | `reference-inspired-ui` + CesiumJS (`clean-room`) + KML preservation | Zero Google proprietary binaries, tiles, or protected assets |
| 7 | «عايز برنامج زي ArcGIS Pro بالظبط ومجاني» | Original free stack (`WPF/Qt + Ribbon + QGIS/GDAL/PROJ + Renderer`) | Zero ArcGIS DLLs/icons; never promise 100% proprietary parity |
| 8 | «عايز أداة أو Add-in داخل ArcGIS Pro» | `extend-host` (ArcPy `.pyt` vs C# Pro SDK add-in) + host license notice | Do not silently override explicit commercial host requirement |
| 9 | «ادمج MapLibre للـ 2D مع CesiumJS للـ 3D» | `multi-engine-composition` with canonical `ViewState` sync & separate GIS core | Do not treat MapLibre styles & 3D terrain as identical engines |
| 10 | «اشتق برنامج جديد من GRASS GIS أو OpenJUMP» | `source-fork` w/ license audit, build check, and cleanup inventory | Do not execute upstream scripts or strip copyright notices |
| 11 | «قارن Leaflet مع OpenLayers مع MapLibre» | 2D renderer comparison by projection, vector tiles, OGC, editing | Do not equate map display library with geometry/CRS processing |
| 12 | «اختار أحسن Stack لتطبيق ويب جغرافي وتحرير معالم» | Web stack decision (`OpenLayers/TerraDraw + Turf` or `PostGIS + API`) | Do not force bloated SPA frameworks for simple static viewers |
| 13 | «هل في محرك أسرع أو أخف من GDAL لقراءة Raster/COG؟» | Discovery by workload (`GeoTIFF.js`, `TiTiler`, `rio-tiler`, `pyogrio`) | Remember Rasterio/pyogrio wrap GDAL C libraries |
| 14 | «جرب تكتشف مهارات خارجية ومصادر جديدة من GitHub» | Safe discovery & `reference-only` quarantine (`New Skill/`) | Never auto-install external skills or treat stars as safety proof |
| 15 | «تغيير شريط Ribbon فقط من غير تغيير المحرك» | `ui-reorganization` / `ui-shell-migration` preserving handlers & shortcuts | Do not migrate engine or break existing command bindings |
| 16 | «برنامج مستقل على محرك QGIS بواجهة Qt» | Standalone Qt shell linking QGIS Core/GUI/Processing + clean-machine checks | Explicit GPL-2.0-or-later & Qt/PROJ runtime deployment audit |
| 17 | «عندنا برنامج WPF وعايزين نضيف تحليلات QGIS» | `worker-service` isolated Python/CLI/IPC boundary | Never assume direct C++ QWidget embedding inside .NET WPF |
| 18 | «برنامج صغير يحول إحداثيات ومساقط بس» | Lightweight `PROJ`/`pyproj`/`Proj4js` library route | Do not bundle full desktop GIS suite for standalone CRS conversion |
| 19 | «اعمل Globe و2D بكل المساقط غير Web Mercator» | Separate `ICrsTransformer` from `IMapRenderer`; verify non-Mercator render | PROJ support != every web/3D renderer renders arbitrary projections |
| 20 | «اعمل برنامج تصميم مدن زي CityEngine» | `multi-engine-composition` (OCCT, Clipper2, CGAL, Blender, SUMO) | No single OSS tool replicates full Esri PRT grammar cleanly |
| 21 | «عايز بديل مجاني لـ Global Mapper» | Multi-format desktop stack (`GDAL + PROJ + PDAL + GRASS` + viewer) | Disclose proprietary Global Mapper formats/SDK limits honestly |
| 22 | «بديل ENVI لتحليل مرئيات الأقمار الصناعية وSAR» | Compare `SNAP Engine` vs `OTB` vs `GDAL/Rasterio/xarray` by sensor | Avoid heavy Java SNAP runtime when simple spectral index suffices |
| 23 | «تطبيق ويب PWA يشتغل أوفلاين على الموبايل والكمبيوتر» | `W08` PWA (`Workbox + IndexedDB/Dexie/OPFS + PMTiles`) | Public OSM tiles ban offline bulk prefetch; SW cache != transactional DB |
| 24 | «تطبيق مساحي على الموبايل بمستقبل GNSS RTK خارجي» | `M06` Native mobile (`BLE/USB + NMEA/RTCM + checkpoint`) | Never claim cm accuracy from smartphone GPS or simulator |
| 25 | «عايز أبني محرك GIS خاص بيا بمكتبات مفتوحة» | Composite SDK architecture over licensed OSS components + attribution | Clearly separate original orchestration code from third-party engines |
| 26 | «شغّل `UI.js` مع الخرائط وبايثون» | Record `UI.js` as `unresolved` until exact repo/package/version verified | Never assume `UI.js` means `Vue.js` or build adapters before verification |
| 27 | «اربط كل تحديثات المهارة كبلجن لـ Codex وClaude وAntigravity» | Multi-platform packaging from single canonical repo via adapters | Local package build != live store approval or cloud publish |
