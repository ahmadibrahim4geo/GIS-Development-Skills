---
name: geospatial-data-processing
description: Build robust standalone GIS vector and raster processing pipelines with GDAL, GeoPandas, Shapely, Rasterio, PROJ, topology and batch QA, portable paths, data provenance and deterministic tests.
license: MIT
---

# Geospatial Data Processing

Use for open-source independent processing. Complement, do **not replace**, [ArcGIS Toolbox Engineering](../arcgis-toolbox-engineering/SKILL.md), [QGIS development](../qgis-plugin-development/SKILL.md), and the [core router](../gis-development/SKILL.md).

## Required workflow
1. Identify Python, OS, GDAL/GEOS/PROJ and dependent package versions. Create project-scoped environments; avoid untested pip/Conda binary mixing.
2. Define input/output formats, known CRS/axis order, Z and vertical datum, field schema, encoding, nodata, raster cell alignment, resolution and precision.
3. Isolate deterministic calculations from UI and GIS-host adapters. Use `pathlib`, explicit options and testable modules; forbid machine-specific paths.
4. Check real datum transformations, not merely SRID label equality; never buffer in longitude/latitude degrees as if they were metres.
5. Check invalid/empty/multipart geometries, numeric stability, raster masks, nodata and resampling; use windowed/streaming reads for large datasets.
6. Preserve originals, verify outputs by re-reading, store source/version/license/provenance, test partial failures, and report limits.
7. Distinguish offline fixture tests from real GIS-engine or Desktop application acceptance.

Try the [read-only network topology sample](../../examples/network-topology/README.md). Its exact endpoint incidence check is not full noding/crossing detection. For automated ArcGIS map outputs read [batch PDF export](../../examples/batch-export/README.md). See [production workflows](../../references/production-workflows.md) and [quality benchmark](../../docs/QUALITY_BENCHMARK.md).
