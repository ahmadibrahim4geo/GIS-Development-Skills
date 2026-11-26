# Browser Geospatial JS Runtime, File Formats & Earth Observation Guide

> Authoritative client-side JS geoprocessing, cloud-native I/O, lossless roundtrip, and EO/STAC guide (`REQ-WM-011`, `REQ-WM-012`, `REQ-WM-013`, `REQ-WM-043`). Keep renderer visualization separate from CRS/topology math.

---

## 1. Browser Draw, Edit & Spatial Analysis (`19 Libraries + 22 Functions`, `§5.3`)

- **Draw / Interactive Editing (`6`):** `Terra Draw` (cross-renderer uniform draw state over MapLibre/Leaflet/OpenLayers), `ol/interaction/Draw + Modify + Snap`, `Leaflet.draw`, `Leaflet-Geoman`, `Mapbox GL Draw` (compatible fork modes), `OpenGeoS maplibre-gl-geo-editor`.
- **Geoprocessing, Indexing & CRS (`13`):** `@turf/turf` (prefer tree-shaken modular packages like `@turf/buffer`, `@turf/area`), `Proj4js` (EPSG definitions + datum grids caveats), `JSTS` (JavaScript port of `JTS` for exact planar OGC Simple Features predicates/valid/buffer), `polygon-clipping`, `martinez-polygon-clipping`, `rbush` (R-tree spatial index), `Supercluster` (fast point aggregation), `earcut` (polygon triangulation with holes), `geodesy` (ellipsoidal/Vincenty formulas), `h3-js` (hexagonal DGGS), `s2-geometry`, `ol-ext`, `wkx` / `wellknown` (WKB/WKT codecs).
- **22 Required Browser Spatial Capabilities:** Draw/edit Point, MultiPoint, LineString, Polygon with interior holes; Vertex/Edge Snapping (`vector.snap`); Split/Cut polygon; Union; Difference; Intersection; Planar Buffer (explicitly projected CRS) vs Geodesic Buffer; Geodesic Area & Distance (`GIS-002`); Douglas-Peucker simplification; Self-intersection bowtie & ring-orientation validation (`GIS-008`); Projected reprojection (`Proj4js`); Spatial BBOX indexing (`rbush`); Clustering (`Supercluster`); Voronoi / Delaunay; Centroids & Convex Hulls; Point-in-Polygon containment; Topology snap tolerance check; Non-destructive Command `Undo`/`Redo` stack (`GIS-005`).

> **CRS & Topology Rule (`GIS-006`, `GIS-008`):** Reject unsupported CRS codes with a clear user error instead of silently projecting into `EPSG:4326`/`3857`. Never run planar metric buffers directly on `EPSG:4326` degrees — transform to appropriate projected `UTM` or use true geodesic buffering.

---

## 2. Web File Formats & Cloud-Native I/O (`29 Sources + 10-Point Roundtrip`, `§5.4`)

| Category | Formats & Client Libraries | Driver Limitations & Browser Memory Notes |
|---|---|---|
| **Core Vector** | `GeoJSON` (RFC 7946 right-hand rule UTF-8), `KML` / `KMZ` (`JSZip` + `@tmcw/togeojson` + `tokml`), `Shapefile` (`shpjs` / `shp-write`), `GPX`, `CSV + WKT` | Check DBF 10-char field truncation & mixed CP1252/UTF-8 Arabic mojibake on Shapefile (`GIS-007`); KML color hex `#aabbggrr` != CSS `#rrggbbaa`; `WEB-QA-13` unsupported feature error |
| **Compact & Analytical Vector** | `GeoPackage` (`@ngageoint/geopackage-js`), `FlatGeobuf`, `GeoParquet`, `GeoArrow`, `DuckDB-Wasm`, `GeoBuf`, `MVT`, `PMTiles`, `MBTiles` | `FlatGeobuf`/`PMTiles` support HTTP `Range` streaming; `DuckDB-Wasm` multi-thread requires `COOP`/`COEP` headers |
| **Raster, Grids & Volumetric** | `GeoTIFF` / `COG` (`GeoTIFF.js`, `ol/source/GeoTIFF`, `georaster`, `geoblaze`, `loaders.gl`), `Zarr` (`zarr.js`), `NetCDF` (`netcdfjs`), `COPC`/`LAZ` (`copc.js`/`laz-perf`), `OGC 3D Tiles`/`glTF` | Enforce windowed/overview reads rather than decoding multi-GB TIFFs into JS TypedArrays (`GIS-011`) |
| **Catalog & Exchange** | `STAC Item/Collection`, `GeoPDF` (generation caveat: prefer QGIS Server/GDAL print for true georeferenced GeoPDF) | Always carry `CORS` + HTTP `Range` checks on external object storage |

**Mandatory 10-Point Format Roundtrip Gate (`REQ-WM-043` / `GIS-001, 007, 012`):** Every import -> edit -> export pipeline must pass independent server/desktop readback (`GDAL/OGR`, `GeoPandas`, or `QGIS`) verifying: `(1)` feature count, `(2)` geometry validity/type, `(3)` exact CRS `EPSG`/axis order, `(4)` persistent `feature_id`, `(5)` numeric/date field types, `(6)` Arabic UTF-8 names & values (zero mojibake), `(7)` explicit `null` preservation vs `""`/`0`, `(8)` `Z`/`M` dimensions or explicit loss notice, `(9)` UTC timestamps/attachments, and `(10)` transparent loss warning when target format drops schema semantics.

---

## 3. Earth Observation, Raster & Time-Series Web GIS (`17 Sources + 15 Tasks`, `§5.5`)

- **17 Indexed Tools & Catalogs:** `TiTiler`, `rio-tiler`, `COG` spec, `STAC Browser`, `stac-fastapi`, `pgSTAC`, `Element 84 Earth Search`, `Microsoft Planetary Computer` (SAS token signing), `NASA CMR / GIBS`, `USGS M2M / Landsat`, `Copernicus Data Space Ecosystem`, `Google Earth Engine JS` (account/quota gate), `ArcGIS ImageServer` (commercial license check), `opengeos/maplibre-gl-raster`, `plotty`, `GDAL-Wasm`.
- **15 EO Web Workflows:** STAC spatio-temporal AOI search, cloud-cover filter, real sensor/acquisition metadata badge, COG overview pyramid selection, custom RGB band combination (`B4/B3/B2`, false-color `B8/B4/B3`), spectral index expressions (`NDVI`, `NDWI`, `NBR`) honoring scale factors & offsets, histogram percentile stretch (`2%–98%`), strict `NoData` alpha transparency mask (`GIS-009`), client pixel-value probe on hover/click, before/after swipe compare sharing camera bounds, time-slider animation with stale HTTP request cancellation, AOI GeoTIFF clip download, vector-raster zonal summary, attribution & license display (`CC-BY`/open data), and fallback error state on missing date/granule.
- **Anti-Fabrication Rule (`GIS-013`):** NEVER display an Esri Wayback mosaic publication date, STAC catalog index timestamp, or OSM edit timestamp as a satellite image's actual sensor acquisition date. Show `Unknown / Mosaic release YYYY-MM-DD` whenever per-pixel scene metadata is absent.
