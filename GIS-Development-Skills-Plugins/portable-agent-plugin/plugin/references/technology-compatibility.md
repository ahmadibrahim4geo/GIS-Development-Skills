# Geospatial Engine & Library Compatibility Matrix (`technology-compatibility.md`)

> Consult this reference alongside [`engine-capability-profiles.json`](engine-capability-profiles.json), [`build-vs-reuse-policy.md`](build-vs-reuse-policy.md), and [`free-first-policy.md`](free-first-policy.md).

## 1. Software License Compatibility Rules (Redistribution & Linking)

| License Family | Examples | Permissive App Static/Dynamic Link | Copyleft Propagation Boundary | Commercial / Closed Binary Rule |
|---|---|---|---|---|
| **Permissive (`MIT`, `BSD-2/3`, `ISC`, `BSL-1.0`, `Apache-2.0`)** | `GDAL` (MIT-style core), `PROJ`, `Clipper2`, `earcut.hpp`, `MapLibre GL JS/Native`, `CesiumJS/Native`, `DuckDB Spatial`, `Fluent.Ribbon`, `GeoPandas` | Allowed statically or dynamically | Keep copyright & LICENSE notice (and Apache `NOTICE` if present) | Compatible with commercial & OSS products; check GDAL optional third-party drivers independently |
| **Weak Copyleft (`LGPL-2.1`, `LGPL-3.0`, `MPL-2.0`, `EPL-2.0`)** | `GEOS` (LGPL-2.1), `Qt` (LGPL-3.0), `SARibbon`, `Qt-ADS`, `IfcOpenShell`, `OSRD`, `Mapnik`, `Eigen` (MPL-2.0) | Allowed dynamically (`.dll`/`.so`/`.dylib`) or file-level (MPL) | Modifications to the LGPL library itself must be shared; app can stay independent if dynamically replaceable | For LGPL in closed apps: compile as shared library (`.dll`/`.so`), preserve relinking rights & ship source/offer; for static linking check license rules |
| **Strong Copyleft (`GPL-2.0`, `GPL-3.0`)** | `QGIS` (GPL-2.0+), `GRASS` (GPL-2.0+), `SAGA` (GPL/LGPL), `QField` (GPL-2.0+), `CloudCompare` (GPL-2.0+), `pgRouting` | Direct linking makes the whole combined binary GPL | Any plugin or binary linking Qt/QGIS/GRASS libraries in-process inherits GPL obligations | NEVER statically or dynamically link GPL libraries into a non-GPL proprietary executable; isolate via separate CLI/IPC/microservice process when integrating cleanly (`worker-service`) |
| **Network Copyleft (`AGPL-3.0`)** | `OpenDroneMap`, `openMVS` | Triggered even over network SaaS delivery | Network users must be offered full corresponding server source | Review SaaS/deployment scope explicitly before bundling into web backend services |
| **Noncommercial / Source-Available / Dev-Only** | `token-optimizer` (`PolyForm-Noncommercial-1.0`), `Redis` (`RSALv2/SSPLv1` -> prefer BSD `Valkey`) | Blocked in commercial or end-user distributions | Quarantine strictly as dev workflow or evaluate free alternative (`Valkey`, OSS engines) | Cannot clear `free_only=True` hard gate for end-user distribution |
| **Commercial / Host-Dependent** | `Esri ArcGIS Pro SDK`, `ArcPy`, `PyPRT / CityEngine SDK`, `Global Mapper SDK`, `Google Maps Platform`, `Mapbox SDK` | Host-owned proprietary runtime; Apache/MIT sample wrappers do NOT open the SDK | Sample code licenses are separate from SDK runtime licenses & API billing | Keep optional & explicit (`extend-host` only); pair with Free/OSS alternatives |

---

## 2. Native ABI, Threading, and Runtime Boundaries (Windows / Linux / macOS / Web)

1. **Duplicate Native GDAL / PROJ Prevention (`E17` / C++ & Python):**
   - Never mix `OSGeo4W` `gdal*.dll`, `conda-forge` `gdal`, and PyPI binary wheels (`rasterio` / `pyogrio` bundled DLLs) inside the same process address space on Windows — symbol collisions on `PROJ_DATA`, `sqlite3`, and CRT heaps (`msvcrt` vs `ucrt`) cause silent crashes or wrong datum shifts.
   - Pin one authoritative GDAL/PROJ installation + `PROJ_DATA` / `GDAL_DATA` environment isolation per process or worker!
2. **Qt Widgets vs WPF / WinUI / WebView2:**
   - Do **not** assume C++ `QgsMapCanvas` (`Qt`) embeds trivially inside `.NET WPF` (`HwndHost`) without OpenGL context contention, DPI scaling drift, and GPL contamination risks.
   - Standard safe boundary: run QGIS / PyQGIS / Python EO computation inside an isolated **`worker-service`** process over typed JSON-RPC / CLI / memory-mapped or GeoPackage/Arrow IPC (`DatasetRef`, `RasterRef`), while rendering native `.NET` (`Mapsui`) or `WebView2` (`MapLibre` / `CesiumJS`) in the WPF shell.
3. **ARM64 vs x86_64 Windows/macOS Native Add-ons:**
   - Several C++/Fortran GIS engines (`TauDEM`, legacy COM ArcObjects `32-bit x86`, `MODFLOW`, `SARibbon`) target specific bitness (`x86` vs `x64` vs `ARM64`). Record ABI match before recommending direct binary linking.
4. **Browser WASM & WebGL2 / WebGPU Limits (`Web & Mobile`):**
   - Multi-threaded WASM engines (`DuckDB-Wasm` multi-thread / `GDAL-Wasm` pthreads) require `Cross-Origin-Opener-Policy: same-origin` (`COOP`) and `Cross-Origin-Embedder-Policy: require-corp` (`COEP`) headers (`SharedArrayBuffer`). Always document single-thread WASM fallback when hosted on static CDNs like GitHub Pages.
   - WebGL context loss on mobile Safari / Android WebView limits simultaneous heavy vector/3D layers; avoid binding dual active 3D WebGL contexts simultaneously without teardown/pause (`multi-engine` `2D <-> 3D` view-state switch).
   - Never prefetch bulk tiles from public `tile.openstreetmap.org` servers for offline mobile/PWA storage (explicitly banned by OSM Tile Usage Policy); require self-hosted PMTiles/MBTiles or licensed tile sources.
