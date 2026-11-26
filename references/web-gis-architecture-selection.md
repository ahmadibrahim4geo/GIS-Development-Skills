# Web GIS Architecture, UI Frameworks, 2D Renderers, Portals & Backends

> Authoritative Web GIS engineering catalog index (`REQ-WM-009`, `REQ-WM-010`, `REQ-WM-015`, `REQ-WM-025`). Every GitHub library is registered once in [`project-catalog.json`](project-catalog.json) with capability metadata in [`engine-capability-profiles.json`](engine-capability-profiles.json) — no duplicate catalogs.

---

## 1. General Web UI, State & Visualization Ecosystem (26 Libraries & 17 Delivery Paths)

- **Core Standards & Tooling:** `HTML5` / `CSS3` / `ES2024+` / `TypeScript`, `Vite` (fast ESM bundler + `?base=` subpath builds).
- **UI Component Frameworks:** `React`, `Next.js`, `Vue 3`, `Nuxt`, `Svelte` / `SvelteKit`, `Angular`, `Astro` (content-heavy `W01` portals), `Lit` / standard `Web Components` (portable cross-framework map embeds).
- **Styling & Accessible Primitives:** `Tailwind CSS`, `shadcn/ui`, `Radix UI` (accessible focus/keyboard primitives), `MUI`.
- **State, Tables, Schemas & i18n:** `TanStack Query` (server cache/cancellation), `TanStack Table` + `TanStack Virtual` (high-row attribute grids for `WEB-QA-15`), `Zustand`, `Redux Toolkit`, `Zod` (runtime JSON/API schema guard), `React Hook Form`, `i18next` (EN/AR `dir="rtl"` localization).
- **Charts, Dashboards & Component QA:** `D3.js`, `Observable Plot`, `Apache ECharts`, `Plotly.js`, `Storybook`.
- **17 Delivery Paths:** Static explorer (`W01`), Multi-page docs portal, SPA viewer, SSR/SEO catalog, Island-architecture `Astro`, Custom `<gis-map>` Web Component, Installable Offline PWA, Electron/Tauri WebView2 hybrid desktop widget, GitHub Pages project subpath (`/repo/`), Print/PDF atlas mode, Web Worker geoprocessing workbench, WebGL/Deck Dashboard, 3D Globe view, Screen-reader tabular GIS twin, Offline survey web form, Narrative StoryMap, Multi-tenant admin portal.

---

## 2. Ten 2D Web Map Engines & 18 Mandatory Interactive Features (`§5.2`)

| Map Engine | Model & Cost | CRS Strengths & Limits | Primary Selection Fit |
|---|---|---|---|
| `MapLibre GL JS` | OSS (`BSD-3-Clause`) | WebGL vector tiles, tilt/pitch, RTL plugin; Web Mercator & globe views | Modern high-density vector tiles, `PMTiles`, custom shaders |
| `OpenLayers` | OSS (`BSD-2-Clause`) | Arbitrary projections (`Proj4js`), WMS/WFS/WMTS, native draw/modify/snap | Serious Web GIS (`W03`, `W09`), UTM/local national grids, OGC |
| `Leaflet` | OSS (`BSD-2-Clause`) | Lightweight DOM/Canvas GeoJSON & XYZ; basic plugin projections | Simple lightweight embeds (`W01`, `W02`) with modest vector counts |
| `OpenLayers + QGIS Server` | OSS (`BSD-2`/`GPL`) | Reproduces QGIS Desktop CRS, expressions, `GetPrint` layouts | Municipal/enterprise QGIS-to-Web publishing (`QWC2`, `Lizmap`) |
| `MapTiler SDK JS` | Commercial / Free-Tier | MapLibre wrapper tied cleanly/tightly to MapTiler Cloud keys | Keyed cloud prototype; swap to `MapLibre` + self-hosted tiles for OSS |
| `ArcGIS Maps SDK for JS` | Commercial Terms | Esri portal/services/3D SceneView; strict Esri account/billing TOS | Explicitly requested Esri Enterprise/Portal web apps |
| `Mapbox GL JS` | Proprietary v2+ (`MAU`) | Token-gated billed loads; non-OSS license after v2 | Only when explicitly authorized & budgeted |
| `Google Maps JS` | Commercial Metered | SKU billing per map/places/routes call; forbids offline tile caching | Consumer store locators under approved billing key |
| `Azure Maps Web SDK` | Commercial Metered | Azure key/SAS billing; MapLibre-based client tied to Azure services | Explicitly mandated Azure cloud enterprise stacks |
| `HERE Maps API for JS` | Commercial Metered | Keyed fleet/logistics routing/matrix billing | Explicitly requested commercial logistics stacks |

**18 Expected Web GIS Interactive Controls:** Layer tree/visibility toggles, opacity & blend controls, dynamic legend, scalebar (metric/imperial), planar + geodesic measurement tools, live cursor/status CRS readout, bilingual search/filter (`WEB-TPL-13`), XSS-safe feature popup/inspector, linked attribute table (`WEB-QA-15`), cartographic print/PDF, split/swipe time compare, spatial clustering/heatmap, attribute-driven styling, active expression filter, theme switch (dark/light), full keyboard navigation (`Tab`/`Esc`/focus restore), shareable URL camera/layer permalink, and non-blocking error recovery banner.

---

## 3. Reference Portals (`17` Apps) & Cartographic Print (`§5.7–5.8`)

- **17 Reference Portals:** `MapStore2`, `Lizmap Web Client`, `QWC2` *(active successor; do NOT deploy legacy deprecated QWC v1)*, `GeoNode`, `GeoNetwork`, `Mapbender`, `uMap`, `qgis2web`, `Kepler.gl`, `GeoLibre`, `OpenGeoS` (`maplibre-gl-components`, `geo-editor`, `layer-control`), `QGIS Server`, `pygeoapi`, `CKAN Geospatial`, `TerriaJS`, `Cesium Stories`, `MapillaryJS` demo.
- **Print & PDF (`A4–A0`):** Prefer vector/SVG/server-rendered layouts (`QGIS Server GetPrint` or `Mapfish Print 3`) when true engineering scale bars, multi-layer legends, and `300+ DPI` `A0` plots are required; browser CSS `@media print` / canvas `toDataURL` suffices only for quick screen snapshots with disclosed scale caveats.

---

## 4. Spatial Databases (`10`), Servers/APIs (`21`), Routing/Geocoding (`10`) & IoT (`§10`)

- **10 Spatial Storage Engines:** `PostgreSQL + PostGIS`, `SQLite + SpatiaLite`, `GeoPackage (SQLite)`, `DuckDB Spatial` (MIT OLAP + GeoParquet), `GeoParquet` / `GeoArrow`, `S3 / MinIO` (COG/PMTiles byte-range object store), `Valkey` (prefer BSD-licensed fork over RSALv2 `Redis`), `Supabase PostGIS`, plus mobile peers (`Room/SQLDelight`, `GRDB`).
- **21 OGC & Geoservice Servers/Frameworks:** `OGC API - Features`, `OGC API - Tiles`, `OGC API - Maps`, `OGC API - Processes`, `OGC WMS/WFS/WCS/WMTS`, `GeoServer`, `QGIS Server`, `pygeoapi`, `MapServer`, `Martin` (Rust MVT/PMTiles), `pg_tileserv`, `pg_featureserv`, `TiTiler`, `Terracotta`, `rio-tiler`, `FastAPI + GeoAlchemy2`, `Node.js / NestJS + PostGIS`, `GeoDjango`, `Apache Sedona`, `GeoMesa`, `STAC FastAPI / pgSTAC`.
- **10 Geocoding & Routing Engines:** `Nominatim`, `Photon`, `Pelias`, `OSRM`, `Valhalla`, `GraphHopper`, `OpenRouteService (ORS)`, `OpenTripPlanner (OTP)`, `GTFS` / `GTFS-RT` transit feeds.
- **Realtime Streams & IoT Telemetry:** `WebSocket` / `SSE` with monotonic event cursors for reconnect deduplication (`WEB-QA-14`), `MQTT`, `OGC SensorThings API` (`FROST-Server`), `PostGIS` server-side geofencing (`ST_DWithin`), and `FCM`/Web Push without leaking user coordinates into unencrypted URLs (`SSRF`/SQLi/authz checks enforced by server).
