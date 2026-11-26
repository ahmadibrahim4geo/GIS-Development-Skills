# Web GIS Products Map (`W01–W12`), 8-Layer Architecture & Selection Matrix

> Consult via [`geospatial-web-mapping`](../skills/geospatial-web-mapping/SKILL.md) alongside [`geospatial-engine-selection`](../skills/geospatial-engine-selection/SKILL.md) (`scripts/discover_engines.py`, `scripts/recommend_stack.py`). Never force a single framework across unrelated Web GIS workloads (`REQ-WM-004`, `REQ-WM-006`, `REQ-WM-008`).

---

## 1. Twelve Web GIS Product Classes (`W01–W12`)

| ID | Product Class | Typical Stack Pattern | Key Requirements & Templates |
|---|---|---|---|
| `W01` | Static GIS Showcase / Landing Page | Semantic HTML/CSS/ESM, Astro/Vite static build, subpath-safe assets | Fast first load, bilingual EN/AR RTL, accessible keyboard nav (`WEB-01`, `WEB-TPL-01`) |
| `W02` | Interactive Web Map Viewer & Cartographic Atlas | MapLibre GL JS / OpenLayers / Leaflet + vector tiles / PMTiles | Layer visibility/opacity, legend, scalebar, URL permalink state (`WEB-02`, `WEB-TPL-02`) |
| `W03` | Browser Spatial Editing Studio & Workbench | OpenLayers Draw/Modify/Snap or Terra Draw + Turf/JSTS/Proj4js | Vertex editing, snapping, topology validity gate, undo/redo, export + readback (`WEB-03`, `WEB-04`) |
| `W04` | Multiuser Full-Stack Collaborative GIS | React/Vue/Svelte + FastAPI/GeoDjango/PostGIS | Revision conflict detection, RBAC auth, audit log (`WEB-11`) |
| `W05` | Spatial Analytics & GeoBI Dashboard | MapLibre + deck.gl + ECharts/D3 + DuckDB-Wasm | Cross-filtered linked table/charts, WCAG accessible list fallback (`WEB-08`, `WEB-QA-15`) |
| `W06` | 3D Web Globe & Digital Twin | CesiumJS / Three.js + 3d-tiles-renderer-js + OGC 3D Tiles | Ellipsoidal vs local ENU coordinates, non-blocking terrain failure recovery (`WEB-07`, `WEB-08`) |
| `W07` | Remote Sensing & EO Raster Explorer | STAC API/Browser + COG + TiTiler / GeoTIFF.js / plotty | True satellite acquisition metadata, band math, NoData masking (`WEB-05`, `WEB-06`) |
| `W08` | Installable Offline-First Web PWA | MapLibre + self-hosted PMTiles + Workbox + IndexedDB/Dexie/OPFS | Cold airplane-mode launch, manual export backup, ban OSM bulk scrape (`WEB-12`, `WEB-17`, `WEB-18`) |
| `W09` | Spatial Data Portal / Open SDI | PostGIS + pygeoapi / GeoServer / STAC FastAPI + CKAN | OGC API Features/Tiles/Maps, downloadable metadata & license cards (`WEB-10`) |
| `W10` | QGIS-Published Web Mapping Project | QGIS Desktop project -> QGIS Server + Lizmap / QWC2 | Desktop QML style, print layout, expressions, forms parity (`WEB-15`) |
| `W11` | Live Asset Tracker & Routing Web App | MapLibre + WebSocket/SSE + Valhalla / OSRM / GraphHopper | Cursor deduplication, reconnect backoff, geofence & PII controls (`WEB-09`, `WEB-14`) |
| `W12` | Geospatial StoryMap & Gazetteer Portal | CesiumJS/MapLibre + narrative keyframes / Nominatim-Photon | Synced camera keyframes, authentic photo attribution, bilingual search (`WEB-13`, `WEB-16`) |

---

## 2. Shared 8 Logical Architecture Layers (`REQ-WM-008`)

Keep domain math, persistence, and credentials cleanly decoupled from UI and map rendering adapters:

1. **`L1` UI Shell & Navigation:** Responsive layout, ribbon/panels, bilingual EN/AR RTL switch, keyboard focus management, accessible tabular fallback (`WEB-QA-15`).
2. **`L2` Map Scene Adapter:** Wraps `MapLibre` / `OpenLayers` / `Leaflet` / `CesiumJS` behind uniform view/camera/selection interfaces without storing canonical business state inside DOM markers or SDK internals.
3. **`L3` GIS Domain Core:** Coordinate projection (`Proj4js`), geometry validation, topology rules, measurement formulas, edit command stack (`Undo`/`Redo`), NoData & raster stretch math.
4. **`L4` Data Access & Network Services:** Typed clients for OGC API, STAC, COG byte ranges, PMTiles, WebSocket streams, and format import/export codecs (`RFC 7946`, `FlatGeobuf`, `GeoPackage`, `KML/KMZ`).
5. **`L5` Offline Storage & Sync Queue:** Versioned `IndexedDB` / `Dexie` / `OPFS` outbox with deterministic revision tokens (no blind `LWW`), `Service Worker` asset cache, and manual export backup (`REQ-WM-047`).
6. **`L6` Security, Auth & Licensing Gate:** HTML popup XSS sanitization, CSP headers, proxy/token isolation (zero client-bundled private secrets), and upstream tile/data attribution enforcement.
7. **`L7` Device & Browser Capabilities:** User-gesture permissions for Geolocation (`HTTPS`), File System Access, WebGPU detection with CPU/WASM fallback, clipboard/share.
8. **`L8` Diagnostics, Telemetry & QA:** Subpath URL testing, memory/frame budgets, and independent export readback via Python/OGR/QGIS.

---

## 3. Non-Dogmatic Decision Engine (16 Conditions × 12 Criteria)

Invoke [`scripts/compare_engines.py`](../scripts/compare_engines.py) and [`scripts/recommend_stack.py`](../scripts/recommend_stack.py) evaluating **16 selection conditions**:
`(1)` product class `W01–W12`, `(2)` non-Mercator 2D projection requirement (`OpenLayers` + `Proj4js` over `MapLibre`), `(3)` 3D ellipsoid vs planar CAD (`CesiumJS` vs `Three.js`), `(4)` offline cold-boot requirement (`PMTiles` + `Workbox` + `Dexie`), `(5)` edit complexity & topology (`OL` + `JSTS` vs `Terra Draw`), `(6)` client raster/COG vs server tiler (`GeoTIFF.js` vs `TiTiler`), `(7)` multiuser transactions (`PostGIS` + conflict revision), `(8)` QGIS project parity (`QGIS Server` + `Lizmap`/`QWC2`), `(9)` dataset volume (`1k` GeoJSON vs `1M+` Vector Tiles/DuckDB-Wasm), `(10)` Arabic RTL glyphs/labels, `(11)` strict Free-First (`no key/no billing`), `(12)` static subpath deploy (`/repo/`), `(13)` `COOP`/`COEP` header control (single- vs multi-thread WASM), `(14)` accessibility/keyboard table fallback, `(15)` real-time WS/MQTT cursoring, and `(16)` host browser memory/GPU limits.

Score eligible alternatives across **12 quantitative criteria**: coordinate/datum accuracy, driver roundtrip fidelity, offline/no-key readiness, bundle size/startup budget, peak heap/VRAM under target feature count, projection breadth, Arabic RTL/BiDi rendering quality, license compatibility (`SPDX`), security isolation (`XSS`/`CORS`/`SRI`), accessibility (`WCAG 2.2`), maintainer/OSGeo health, and clean subpath deployment.
