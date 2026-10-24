# GIS Fixture Pack — Deterministic Test Data

All data are synthetic, not real geographic networks, weather stations or elevations. The fixture pack **supplements** earlier `examples/*/fixtures` files without moving or deleting them.

## Shipped (standard-library CI)
- [valid_invalid_polygons.geojson](geojson/valid_invalid_polygons.geojson): one valid OGC ring and one self-intersecting bowtie polygon.
- [points_lines.geojson](geojson/points_lines.geojson): longitude/latitude point pair and line spanning 1° latitude; use proper geodesic/spherical calculation, never degrees as metres.
- [expected-results.json](expected/expected-results.json): deterministic expected geometry flags, Haversine tolerance, vector attribute limitations and raster metadata.

## Generated binary fixtures (optional GIS environment)
Install a compatible Fiona/Rasterio/NumPy stack (prefer a tested single conda-forge environment), then run:

```bash
python fixtures/generate_binary_fixtures.py --output ./generated-gis-fixtures
```

Creates `shapefile/attribute_limits.shp` plus sidecars (long DBF field gets truncated to `very_long_`); a multi-layer `multilayer.gpkg` (points + lines); `nodata_4326.tif` and `misaligned_3857.tif` (2x2, nodata=-9999, intentionally incompatible CRSs and transforms). Generated files go in a **new** folder, not checked-in provider content. Binary GIS correctness must be checked with a compatible GDAL/QGIS/ArcGIS installation.

The test harness [test_gis_fixtures.py](../tests/test_gis_fixtures.py) checks GeoJSON/expected values in stdlib CI. Native targets are separated in [native_tests](../native_tests/README.md). Follow [evidence tiers](../docs/QUALITY_BENCHMARK.md) for actual test claims.
