# 3D Web GIS, Digital Twins, LiDAR, WebXR & Resilience Checks

> Authoritative 3D Web / Globe / Point Cloud guide (`REQ-WM-014`). Separates ellipsoidal Earth globes from local planar CAD scenes and documents all 13 mandatory 3D failure/accuracy checks.

---

## 1. Seventeen Web 3D, Digital Twin, LiDAR & Spatial Visualization Sources (`§5.6`)

| Engine / Spec | Core Purpose | Coordinate & Scale Model | License / Billing Caveats |
|---|---|---|---|
| `CesiumJS` + `Sandcastle` | Global WGS84 3D globe, quantized terrain, `3D Tiles`, CZML time | Geocentric ECEF (`EPSG:4978`/`4326`), global logarithmic depth buffer | `Apache-2.0` core; `Cesium ion` assets/terrain require key & quota (`commercial/free-tier`) |
| `Three.js` + `3d-tiles-renderer-js` (`NASA-AMMOS`) | Custom WebGL/WebGPU 3D architectural scenes, CAD/BIM, local `3D Tiles` | Local Cartesian ENU scene origin required to avoid float32 jitter | `MIT`; add custom `Proj4`/`ECEF->ENU` bridge for geo-referencing |
| `deck.gl` + `loaders.gl` + `luma.gl` (`vis.gl`) | High-density GPU instancing, hexagon grids, point clouds, `MapLibre` overlay | Mercator/globe synchronized camera matrices | `MIT`; GPU driver/VRAM bounded (`WEB-QA-12`) |
| `kepler.gl` | Ready-made exploratory spatio-temporal analytics React workbench | Built over `deck.gl` | `MIT`; heavy bundle — keep for `W05` dashboards, not `W01` |
| `GeoLibre` | Multi-engine browser/desktop reference patterns over OSS libs | Synchronized 2D/3D layer state model | Verify individual component versions & upstream terms |
| `Potree` | Progressive octree point-cloud (`LAS`/`LAZ`/`Entwine`) WebGL renderer | Spatial octree hierarchy, local bounding box offset | `BSD-2-Clause`; convert raw LAZ to `COPC` or `Potree` octree offline first |
| `iTowns` / `Giro3D` | Open-source Three.js-based 3D geospatial/elevation/IFC browser frameworks | Arbitrary projected CRS (`EPSG` local frames) | `MIT` / `CeCILL-B` — check per-repo upstream notice |
| `ol-cesium` | Synchronizes `OpenLayers` 2D view state with `CesiumJS` 3D globe | Shared camera/projection bridge | `BSD-3-Clause`; avoid running dual full WebGL contexts on weak mobile GPUs |
| `OGC 3D Tiles 1.0/1.1` + `glTF 2.0` (`Draco` / `KTX2`) + `CityJSON` + `3D Gaussian Splatting` + `MapillaryJS` / `WebXR` | Interoperable hierarchical LOD meshes, compressed textures, semantic city models, street-level imagery & AR/VR views | Verify `glTF` Y-up vs GIS Z-up transform matrices explicitly | Street imagery & WebXR sensors require explicit CORS, API attribution & user consent |

---

## 2. Thirteen Mandatory 3D Web QA & Precision Checks (`WEB-QA-09`, `GIS-014`)

1. **Global Geodesy & Camera Framing (`GIS-014`):** Handle antimeridian (`±180°`) and high-latitude/polar boundaries without inverted triangles or trapped gimbal lock.
2. **Double-to-Float32 Jitter Prevention:** Subtract camera-relative local `ENU` anchor in 64-bit `Float64` before uploading vertex arrays to GPU `Float32` shaders (`Three.js` / `deck.gl`).
3. **Z-Up vs Y-Up Axis Alignment:** Validate `glTF` (`Y-up`) and `CityJSON` (`Z-up`) bounding transforms so extruded buildings do not rotate 90° or float underground.
4. **Terrain Height Clamping & Vertical Datum:** Distinguish ellipsoidal heights (`WGS84` / Cesium quantized mesh) from orthometric (`EGM96`/`EGM2008` MSL) when placing ground markers (`clampToGround`).
5. **LOD / Screen-Space Error (SSE) Budget:** Tune `maximumScreenSpaceError` so 3D Tiles stay responsive without exhausting mobile Safari / WebView VRAM.
6. **Z-Fighting Prevention:** Avoid near-coplanar depth bias on polygons/footprints draped onto sloped terrain; verify near/far frustum clipping ratios.
7. **Solar Lighting & Cast Shadow Accuracy:** Drive sun position via validated timestamp + timezone (`gis-device-context`) and match `Cesium` / `Three.js` shadow frustum to site scale.
8. **Feature Picking & Highlight Parity:** Ensure 3D `BatchId` / `EXT_mesh_features` picking maps cleanly back to the same canonical `feature_id` shown in 2D map & attribute tables.
9. **Non-Blocking Terrain Failure Recovery (`WEB-QA-09`):** If a quantized-mesh terrain endpoint returns `404`/`503`/CORS error, drop back gracefully to smooth ellipsoid terrain (`EllipsoidTerrainProvider`) with a visible non-blocking warning instead of crashing camera navigation.
10. **WebGL Context Loss & Memory Teardown:** Listen to `webglcontextlost` / `webglcontextrestored` and explicitly destroy inactive WebGL canvases when toggling `2D <-> 3D` modes.
11. **Point-Cloud Progressive Budget:** Cap active point budget (`pointBudget`) and verify intensity/classification/RGB ramp legends render identically.
12. **2D ↔ 3D Camera & Layer Synchronization:** Switching between `OpenLayers`/`MapLibre` (`2D`) and `CesiumJS` (`3D`) synchronizes center, scale/altitude, and active layer visibility deterministically.
13. **Asset, Terrain & Ion Attribution:** Render non-removable data/imagery/terrain credit overlays required by OpenTopography, Cesium ion, OSM, or local LiDAR licenses.
