# Web GIS Examples & Templates (`W01–W12`, `WEB-01..WEB-18`)

Complete implementation blueprints and executable vertical slices aligned with [Web GIS Products Map](../../references/web-gis-products-map.md), [geospatial-web-mapping](../../skills/geospatial-web-mapping/SKILL.md), and [WEB_GIS_GUIDE.md](../../docs/WEB_GIS_GUIDE.md).

## 1. Shared Executable Core & Offline Vertical Slices

- [`shared/spatial-core.mjs`](shared/spatial-core.mjs): GeoJSON `EPSG:4326` validation, unsupported-CRS rejection (`GIS-006`), WGS84↔UTM Zone `36N` math & Haversine geodesic distance (`GIS-002`), bowtie self-intersection detection (`GIS-008`), `SpatialEditorStore` Undo/Redo + GeoJSON export (`GIS-004`, `GIS-005`), popup XSS sanitization (`WEB-QA-10`), BiDi coordinate formatting (`WEB-QA-04`), subpath URL resolution (`WEB-QA-11`), imagery acquisition date guard (`GIS-013`), and antimeridian bbox wrap (`GIS-014`).
- [`shared/pwa-sync.mjs`](shared/pwa-sync.mjs): Public OSM bulk tile scraping ban (`WEB-QA-07`), `401/403/429` secret-redacting fallback (`WEB-QA-08`), realtime cursor stream backoff & deduplication (`WEB-QA-14`), and 15-field offline sync queue without blind LWW (`WEB-QA-06`).
- **Interactive Browser Vertical Slices (tested in Node.js T1; headless Chromium E2E: `NOT RUN`):**
  - [`WEB-01`](templates/WEB-01/docs/README.md) (`templates/WEB-01/index.html`) — Static Map Explorer + Accessible Feature Table (`WEB-QA-15`).
  - [`WEB-03`](templates/WEB-03/docs/README.md) (`templates/WEB-03/index.html`) — Spatial Editing Studio with Undo/Redo, topology validation, XSS-safe popup inspector, and GeoJSON export.
  - [`WEB-12`](templates/WEB-12/docs/README.md) (`templates/WEB-12/index.html`, `manifest.webmanifest`, `sw.js`) — Offline-First PWA with Service Worker subpath cache and manual JSON backup export.

## 2. All 18 Web GIS Template Packages (`templates/WEB-01` .. `WEB-18`)

Every template directory enforces the mandatory **6-subfolder contract** (`fixtures/`, `spec/`, `tests/`, `evidence/`, `docs/`, `safety/`). See each template's `spec/template-spec.json` and `evidence/ACCEPTANCE.md` for honest `T0/T1` vs `NOT RUN` status.
