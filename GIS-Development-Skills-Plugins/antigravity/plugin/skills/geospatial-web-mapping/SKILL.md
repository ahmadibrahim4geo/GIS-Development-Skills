---
name: geospatial-web-mapping
description: Build and evaluate web maps and desktop-embedded MapLibre/GeoLibre 2D/3D UIs, with real geometry editing, layer state, PWA offline sync, historical imagery time controls, raster/COG rendering and correctly licensed basemaps.
license: MIT
---

# Geospatial Web Mapping

**Free-first default:** Follow [no-cost GIS workflow and licensing policy](../../references/free-first-policy.md). Do not silently require paid GIS execution, LLM/API credits or expiring trials. Disclose vendor-license limits and offer a separately tested analogous free route where feasible.

Use when the deliverable is a Web GIS product (`W01–W12`), PWA, browser spatial editor/EO viewer, or mapping UI in a desktop shell. For cross-engine choice, multi-engine compositions, or framework selection, invoke [Geospatial Engine Selection](../geospatial-engine-selection/SKILL.md) rather than forcing one stack; the existing [project catalog](../../references/project-catalog.json) and [GIS software source registry](../../references/gis-software-source-registry.md) remain the single source of truth.

## Web GIS Reference Guides (Progressive Disclosure)

- **Products, 8 Layers & Decision Matrix (`W01–W12`):** [web-gis-products-map.md](../../references/web-gis-products-map.md)
- **Web UI Frameworks, 2D Renderers, Portals & Backends:** [web-gis-architecture-selection.md](../../references/web-gis-architecture-selection.md)
- **JS Spatial Math, Editing, 29 Formats & EO/STAC:** [browser-geospatial-js-runtime.md](../../references/browser-geospatial-js-runtime.md)
- **3D Globes, Digital Twins, LiDAR & WebXR:** [geospatial-3d-ar-mobile-web.md](../../references/geospatial-3d-ar-mobile-web.md)
- **PWA, Offline Storage, Tile Policy & 15-Field Sync:** [web-mobile-offline-sync-contract.md](../../references/web-mobile-offline-sync-contract.md)
- **On-Device & Cloud GeoAI Options:** [web-mobile-geoai-options.md](../../references/web-mobile-geoai-options.md)
- **26 Providers & 10 OWASP Security Controls:** [web-mobile-vendor-license-audit.md](../../references/web-mobile-vendor-license-audit.md)
- **Templates (`WEB-01..WEB-18`) & Practical Guide:** [WEB_GIS_GUIDE.md](../../docs/WEB_GIS_GUIDE.md) · [examples/web-gis](../../examples/web-gis/README.md) · [Performance & Budgets](../../docs/PERFORMANCE_RELIABILITY.md)

## Procedure

1. Identify product class (`W01–W12`), delivery shell (standalone static subpath, Vite/SPA, PWA offline, or Tauri/WebView2 desktop), and consult [desktop-and-web.md](../../references/desktop-and-web.md), [geolibre-integration.md](../../references/geolibre-integration.md), and [gishub-software.md](../../references/gishub-software.md).
2. Keep the 8 logical layers separated: mapping renderer (`MapLibre` / `OpenLayers` / `Leaflet` / `CesiumJS`) stays distinct from projection/topology compute (`Proj4js`, `Turf`, `JSTS`, `GDAL/Worker`), offline queue, and auth secrets.
3. Evaluate official [opengeos/maplibre-gl-components](https://github.com/opengeos/maplibre-gl-components) modules (layer-manager, geo-editor, time-slider) **only after version checks** and [external-agent-skills-registry.json](../../references/external-agent-skills-registry.json) security review.
4. Implement end-to-end real editing, undo/redo, topology validity, Arabic UTF-8 RTL preservation, popup XSS sanitization (`escapeHtml` / `textContent`), subpath relative assets, and accessible table/list fallback before adding extra toolbar controls.
5. For historical imagery / EO layers, use real dated sources (`STAC` acquisition dates, `COG` NoData/stretch) — never fake acquisition dates from mosaic publish timestamps or OSM edits.
6. Enforce remote API, tile licensing, CORS, and quota rules via [Geospatial API Integration](../geospatial-api-integration/SKILL.md) and [free-geospatial-apis.md](../../references/free-geospatial-apis.md); **never** scrape or prefetch public `tile.openstreetmap.org` servers for offline PWAs.
7. Run deterministic Node/Python contract & independent GeoJSON/GeoPackage readback checks (`T1`), plus live browser E2E (`WEB-QA-01..15`) when Playwright/browser runtimes exist — otherwise state explicitly what remains `NOT RUN`.

## Acceptance (`GIS-001..014` & `WEB-QA-01..15`)

- [ ] Renderer, domain math (`Proj4js`/topology), persistence, and credentials cleanly separated
- [ ] Buttons, accessible keyboard table view, Arabic RTL/LTR, and subpath `/repo/` links work (not placeholders)
- [ ] Import -> Edit -> Undo/Redo -> Export passes independent OGR/Python readback (`GIS-007`, `GIS-012`)
- [ ] Offline PWA survives cold launch, honors `COOP`/`COEP` / `storage.persist()` fallbacks, exports backup, never scrapes OSM bulk tiles
- [ ] Popups escape HTML (`WEB-QA-10`); 401/403/429 errors leak zero keys; missing terrain/imagery recovers safely

## Blue Marble 3D Tiles and terrain forks

See the [Global Mapper / Blue Marble reference](../../references/blue-marble-global-mapper.md) for forked Cesium 3D Tiles Tools and an older Cesium Terrain Builder. They are independent utilities, not the proprietary Global Mapper renderer. Check terrain tiling scheme, NoData, dataset licensing, 3D Tiles metadata/transform and server support before using in CesiumJS or MapLibre.

## Earth timeline and Google Earth Pro behavior

For browser or embedded-Cesium globe UIs, consult [Google Earth Pro patterns](../../references/google-earth-pro-engineering.md) and [Historical Imagery Timeline](../../references/historical-imagery-timeline.md). Keep imagery timeline controls docked/nonblocking; query scene availability per AOI; display actual acquisition/mosaic dates and provider licensing; cancel stale requests and never blank the globe on missing imagery. Compare mode shares camera/bounds, not two independently drifting map viewpoints. This is a design reference only, not a claim of live implementation.

## Earth View: globe-to-modal architecture

Review [Earth View](../../references/earth-view-architecture.md) for typed base/overlay imagery provider registries, WMS 1.3.0 EPSG:4326 BBOX axis order, temporal images, camera controls and regional zoom/view-state restoration. Avoid copying code without an upstream license; do not infer displayed date is the satellite acquisition date or assume optional AI controls are visible.

## OpenGeoS deeper integration candidates

- [COG/GeoTIFF client](https://github.com/opengeos/maplibre-gl-raster): inspect bands, NoData, overviews and source pixels; remote access requires CORS/range support.
- [GeoParquet](https://github.com/opengeos/maplibre-gl-geoparquet) and [DuckDB spatial](https://github.com/opengeos/maplibre-gl-duckdb): verify spatial extension, security of SQL input, CRS and memory usage.
- [3D Tiles](https://github.com/opengeos/maplibre-gl-3d-tiles), [historical Esri Wayback imagery releases](https://github.com/opengeos/maplibre-gl-esri-wayback), [layer controls](https://github.com/opengeos/maplibre-gl-layer-control): all need pinned compatible MapLibre versions, genuine live click tests, and upstream service rights. Wayback release date is not automatically acquisition date.
- [OpenGeoS advanced guide](../../references/opengeos-advanced-integration.md): MapLibre plugins are not drop-in CesiumJS adapters.

## Browser and WebView device permissions

For browser geolocation, notifications, file picking, camera/microphone, WebUSB/serial/BLE or embedded host access, consult [System Capabilities & Permissions](../system-capabilities-and-permissions/SKILL.md) and Security Guardian. Enforce HTTPS/secure contexts, origin and Permissions Policy, real user gestures and restricted WebView/Electron/Tauri bridges. Keep map scene/camera position distinct from user's physical GPS location via [GIS Device Context](../gis-device-context/SKILL.md), and apply [scientific GIS invariants](../../references/agent-reasoning/scientific-gis-reasoning.md) (XYZ vs TMS tile schema, view reprojection correctness, and honest `NOT RUN` browser boundaries).

## Visual assets (conditional)

When the reviewed project needs thumbnails, official logos, photographs, illustrations or screenshots, compose [Visual Asset Discovery & Integration](../visual-asset-discovery-integration/SKILL.md). It owns internet/source discovery, asset suitability, source credits and prepared local variants; keep layout, target resource binding, packaging and actual UI acceptance with this platform/UX owner. Do not silently replace requested images with generic icons or claim a source URL proves local integration.
