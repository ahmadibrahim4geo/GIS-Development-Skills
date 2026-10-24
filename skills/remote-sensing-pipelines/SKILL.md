---
name: remote-sensing-pipelines
description: Plan, implement and verify reproducible STAC, Cloud Optimized GeoTIFF, Google Earth Engine and satellite/climate raster pipelines with acquisition metadata, quality masks, correct scaling and aligned output grids.
license: MIT
---

# Remote Sensing Pipelines

Use for satellite scenes, Earth Engine, STAC/COG collections, cloud masking and climate rasters. Consult [data discovery](../geospatial-data-discovery/SKILL.md), [CRS engineering](../coordinate-reference-systems/SKILL.md), and [GIS development](../gis-development/SKILL.md).

## Required workflow
1. Confirm product/sensor/collection/processing level, acquisition dates, AOI, coverage, spatial resolution, data license, access and expected data semantics.
2. Verify reflectance scaling, offsets, band order, radiometric processing, sun angle, saturation, nodata and **per-pixel** cloud/shadow QA; scene `CLOUD_COVER` alone is insufficient.
3. Pin target CRS and pixel grid: transform, origin, resolution, extent, resampling algorithm and nodata handling.
4. Preserve STAC item IDs, source assets, timestamps, version, QA choices, license and the complete compositing/reprojection recipe.
5. Test COG range requests and real partial reads; distinguish preview tiles from numerical analysis products. Manage Earth Engine auth, server/client semantics, quotas and export.
6. Validate against known reference pixels and imagery footprints, including missing scenes, time-zone boundaries, antimeridian and uneven observation counts.
7. Report independent computational evidence and failures; do not assert native Earth Engine/GDAL correctness from documentation-only checks.

Read [STAC/COG workflow](../../examples/remote-sensing/STAC_COG_WORKFLOW.md), [production workflows](../../references/production-workflows.md) and [quality benchmark](../../docs/QUALITY_BENCHMARK.md).
