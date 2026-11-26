# Web GIS Engineering Guide (`W01–W12`, `WEB-01..WEB-18`) / دليل تطوير خرائط وتطبيقات الويب

> Companion guide to [`skills/geospatial-web-mapping/SKILL.md`](../skills/geospatial-web-mapping/SKILL.md) and [`examples/web-gis/README.md`](../examples/web-gis/README.md).

## 1. Quick Architecture Selection (`W01–W12`)

- **Static Viewer / Landing Page (`W01`–`W02`):** Use `MapLibre GL JS` or `Leaflet`, relative subpath paths (`./`), accessible keyboard feature list (`WEB-QA-15`), and RTL-ready labels (`WEB-QA-04`).
- **Editing & Custom Projections (`W03`):** Use `OpenLayers` + `Proj4js` (`W03`/`WEB-03`) when arbitrary projections (`EPSG:32636`, polar), OGC WFS-T, or topological snapping/undo are primary; keep geometry core cleanly in `examples/web-gis/shared/spatial-core.mjs`.
- **EO / 3D / Portal / Realtime (`W05`–`W12`):** Select `CesiumJS` for ellipsoidal 3D terrain with graceful failure fallback (`WEB-QA-09`), `COG` + `STAC` for satellite timelines with honest acquisition metadata (`GIS-013`), and `PostGIS + pygeoapi / QGIS Server` for multiuser portals or desktop-parity publishing (`WEB-10`, `WEB-15`).
- **Offline PWA (`W08` / `WEB-12`):** Bundle self-hosted `PMTiles` or local GeoJSON slices + `Service Worker` subpath cache + 15-field `WebOfflineOutbox` (`WEB-06`, `WEB-12`). Never scrape `tile.openstreetmap.org`. Document `COOP`/`COEP` needs for multi-thread `SQLite-Wasm` OPFS and provide manual JSON export backup (`REQ-WM-047`).

## 2. Offline Verification Commands (`Node.js + Python`)

```bash
node --check examples/web-gis/shared/spatial-core.mjs
node --check examples/web-gis/shared/pwa-sync.mjs
node --test tests/web-gis/web_gis_contract.test.mjs
python -B -m unittest tests.test_web_gis_expansion -v
```

> **Verification Boundary:** Node.js + Python tests provide `T0/T1` deterministic contract & cross-runtime GeoJSON readback verification. Live multi-browser visual rendering & Playwright E2E (`WEB-QA-01..03`, `WEB-QA-12` GPU metrics) remain **`NOT RUN`** unless Playwright and target browser binaries are installed on the machine.
