# GIS Performance, Reliability and Crash Prevention

Apply to desktop applications, ArcGIS toolboxes, QGIS plugins, web GIS and geoprocessing services.

## Design controls
- Use bounded-memory streaming, spatial indexing, tiling and batch processing for large data.
- Keep UI work responsive: move expensive tasks to worker processes/threads appropriate to the host.
- Provide cancellation, progress reporting, checkpoints and atomic output writes.
- Validate user inputs and corrupted geospatial data before processing.
- Capture structured error logs and actionable diagnostics without leaking personal data.
- Restore recoverable application state; never silently overwrite a valid project after failure.

## Test matrix
| Test | Evidence |
| --- | --- |
| Baseline | Dataset size, runtime, peak RAM, CPU, disk I/O |
| Scale | Multiple feature/raster sizes and scaling curves |
| Stress | Load beyond expected operating range and graceful refusal |
| Soak | Repeated open/process/close cycles and memory trend |
| Failure | Corrupt KML/KMZ, bad CRS, missing layers, interrupted writes |
| Recovery | Cancel, restart, reopen last committed project |
| Regression | Compare to baseline with documented tolerance |
| Compatibility | Native ArcGIS Pro, ArcMap, QGIS, Windows and browser tests where applicable |

Define thresholds per project and hardware; no universal maximum file size or feature count exists. Unit and mock tests are not proof of native runtime behavior.

## 10-Domain Measured Budget Matrix (`Web_Mobile_r3` §16.1, `REQ-WM-032`)

Never cite invented FPS or RAM limits (`"guaranteed 60 FPS"`). Instead, measure and gate across all 10 operational domains under your documented dataset, device class, and GPU/WebGL fallback state:

1. **First Launch & Cold Boot:** Shell parse time, worker initialization, offline cache hydration (`WEB-QA-06`).
2. **Large Vector Rendering:** Peak heap/VRAM and pan/zoom frame responsiveness across `1k` / `10k+` features (`GIS-011`) with clustering/MVT/PMTiles streaming.
3. **Raster & COG Streaming:** HTTP `Range` request counts, overview pyramid selection, and canvas decode latency without full-image OOM.
4. **3D Globe & Tiles:** Screen-Space Error (`SSE`) budget, mobile Safari WebGL context teardown (`webglcontextlost`), and terrain fallback (`WEB-QA-09`).
5. **Search, Filter & Spatial Editing:** Index build latency (`RBush`/`Flatbush`), topology validation time, and non-blocking worker execution.
6. **Offline Storage Quotas & Persistence:** `navigator.storage.estimate()`, `storage.persist()` fallback handling, and manual JSON/GeoPackage backup export (`REQ-WM-047`).
7. **API Quotas & Cost Circuit Breakers:** Hard budget stops plus `401/403/429` secret-free fallback behavior (`WEB-QA-08`).
8. **Network Throttling & Disconnection:** Slow-3G / intermittent drops, stalled fetch timeouts, and `WebSocket`/`SSE` cursor deduplication (`WEB-QA-14`).
9. **Crash Recovery & Corrupted Input Rejection:** Atomic storage commits before optimistic UI confirmation, bad-CRS/self-intersection refusal (`GIS-006`, `GIS-008`).
10. **Accessibility & Subpath Parity:** Keyboard tab order/focus restore (`WEB-QA-03`), screen-reader tabular feature view (`WEB-QA-15`), `dir="rtl"` Web layout (`WEB-QA-04`), and relative subpath URLs (`WEB-QA-11`).

