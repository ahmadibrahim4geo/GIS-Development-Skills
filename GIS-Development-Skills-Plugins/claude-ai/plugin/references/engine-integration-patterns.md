# Multi-Engine Integration Patterns, Data Contracts & Composite Architecture

> Core architectural contract specification (`REQ-EV2-028`, `053`, `054`, `058`, `064`) for [`geospatial-engine-selection`](../skills/geospatial-engine-selection/SKILL.md), [`scripts/recommend_stack.py`](../scripts/recommend_stack.py), and [`engine-comparison-guide.md`](engine-comparison-guide.md).

---

## 1. Eight Canonical Provider Interfaces (`REQ-EV2-028`)

Keep every engine replaceable behind minimal typed interfaces instead of coupling UI event handlers directly to library internals:

1. **`IDataProvider`** — `probe(ref)`, `read_features(query)`, `read_raster_window(bbox, bands)`, `write_atomic(target)`
2. **`ICrsTransformer`** — `transform_point/geom(src_crs, dst_crs, epoch, vertical_grid)`, axis-order awareness (`E08`, `E27`)
3. **`IRenderer2D`** — `set_view_state(center, zoom, crs, rotation)`, `set_layers()`, `pick(screen_xy)`
4. **`IRenderer3D`** — `set_camera_ecef()`, `set_terrain_provider()`, `add_3d_tileset()`, `on_context_lost()` (`REQ-EV2-053`)
5. **`IGeoprocessingWorker`** — `submit(job_spec)`, `progress_stream()`, `cancel(job_id)`, `cleanup_temp()` (`E32`, `E33`)
6. **`ILayerStyleAdapter`** — translate across `MapLibre Style JSON` / `QML` / `SLD` / `CIM-spec` + emit mandatory **`style_loss_report`** & HarfBuzz/FriBidi Arabic text checks (`REQ-EV2-054`)
7. **`ITerrainElevProvider`** — sample DEM / quantized mesh w/ explicit vertical datum (`ellipsoidal` vs `orthometric`) & `NoData` refusal (`E-12`)
8. **`ISimulationProvider`** — explicit steady/dynamic physics solver (`NOAA solar`, `SWMM` vs `D8` distinction, `SUMO` directed turns, `REQ-EV2-057`)

---

## 2. Five Immutable Data & Execution Contracts (`REQ-EV2-058`)

- **`DatasetRef`:** `{ dataset_id (opaque token), driver, crs_auth_code, bbox, readonly, provenance }` — **NEVER** trust raw client filesystem strings across IPC/WebView boundaries without root validation.
- **`FeatureIdentity`:** `{ layer_id, feature_uuid, driver_fid, server_revision }` — preserved losslessly when switching renderers (`E14`) or round-tripping formats.
- **`RasterRef`:** `{ asset_id, uri, crs, affine_gt_6, width, height, band_count, dtype, nodata_value, scale_offset, acquisition_utc }` (`REQ-EV2-056`).
- **`Renderer` Canonical State:** `{ mode ("2d"|"3d"), view_crs, center_epsg4326, zoom_or_alt_m, heading, pitch, visible_layer_ids, selected_ids, time_iso }` (`E14`).
- **`Processing` Execution Envelope:** `{ job_id, tool_id, input_refs, params, timeout_s, cancel_token, atomic_output_dir, exit_code, provenance }` (`E32`, `E33`).

---

## 3. Eight Cross-Language Integration Modes & `Multi-Engine` Safety

| Integration Mode | Best Fit | Critical Safety & ABI Guard |
|---|---|---|
| **1. Static / Shared Native C++ Lib** | Single-process C++/Qt (`QGIS Core`, `GDAL`, `MapLibre Native`) | Exact MSVC/GCC ABI + CMake/vcpkg dependency alignment |
| **2. `C ABI` Boundary** | Calling Rust (`RustGIS` / `geo`) or C++ (`PROJ`/`GEOS`) safely | Explicit UTF-8 string ownership & status error structs (`E34`) |
| **3. Python Extension (`pybind11` / `PyQGIS`)** | Scientific workflows (`GeoPandas`, `Rasterio`, `PySTAC`) | Isolate matching conda/OSGeo4W interpreter & DLL search path |
| **4. `.NET` P/Invoke / Interop** | WPF / WinUI / Avalonia desktop (`GDAL.NET`, `NetTopologySuite`, `Mapsui`) | Verify x64 native `.dll` lookup & `PROJ_DATA` initialization (`E29`) |
| **5. Java JNI / JVM Bridge** | Android Kotlin <-> MapLibre Native / Spatialite | Handle ABI splits (`arm64-v8a` / `x86_64`) & lifecycle cleanup |
| **6. JS / WebView2 Host Bridge** | Desktop C#/Qt shell + CesiumJS / MapLibre web view (`E05`, `Z EARTH`) | Typed JSON schemas, strict CORS/origin allowlist, no `eval()` |
| **7. WebAssembly (`WASM`)** | Client-side `DuckDB-Wasm`, `SQLite-Wasm`, `GDAL3.js` | Enforce heap ceilings & `COOP/COEP` single-thread fallback |
| **8. Local IPC / CLI Subprocess Worker** | **WPF / Desktop Shell + isolated QGIS / GDAL / SNAP Worker (`E05`)** | Process crash recovery (`E33`), bounded timeout, atomic output writes |

**Non-Negotiable Composite Engine Guardrails (`REQ-EV2-028`, `064`):**
- Never assume Qt GUI widgets (`QgsMapCanvas`) embed cleanly inside unrelated WPF/Web frameworks — use isolated IPC worker processes or native host canvases (`E05`).
- Enforce explicit **`ICrsTransformer`** across boundaries (e.g., metric GEOS buffer in UTM -> `EPSG:4326`/`3857` MapLibre display) — block silent CRS swaps (`E27`, `E38`).
- Separate **Developer Build SDKs** (`CMake`, `vcpkg`, `Conan`, `PyInstaller`, `Inno Setup`) from **End-User Runtime Bundles** (`REQ-EV2-064`) without claiming authorship over upstream OSS libraries.
