---
name: remote-sensing-pipelines
description: Plan, implement and verify reproducible STAC, Cloud Optimized GeoTIFF, Google Earth Engine and satellite/climate raster pipelines with acquisition metadata, quality masks, correct scaling, spectral index calculation, alias disambiguation and scientific interpretation.
license: MIT
---

# Remote Sensing Pipelines

**Free-first default:** Follow [no-cost GIS workflow and licensing policy](../../references/free-first-policy.md). Do not silently require paid GIS execution, LLM/API credits or expiring trials. Disclose vendor-license limits and offer a separately tested analogous free route where feasible.

Use for satellite scenes, Earth Engine, STAC/COG collections, cloud masking, spectral index calculation, biophysical interpretation and climate rasters. Consult [data discovery](../geospatial-data-discovery/SKILL.md), [data catalogs](../geospatial-data-catalogs/SKILL.md), [CRS engineering](../coordinate-reference-systems/SKILL.md), and [GIS development](../gis-development/SKILL.md).

## Spectral indices, sensor band mappings, and scientific interpretation

Scientific satellite workflows must separate algebra from interpretation. Consult the progressive references:
- [Remote Sensing Indices & Interpretation Guide](../../references/remote-sensing-indices.md): Formulations, domain guides, physical parameter caveats, and mathematical bounds.
- [Sensor Band Mappings & Product Scaling](../../references/remote-sensing-sensor-band-mappings.md): Band assignments across Landsat (TM/ETM+/OLI), Sentinel-2 MSI, MODIS, and HLS, with Level-2 surface reflectance scale factors ($DN \times 0.0000275 - 0.2$), SCL masks, and SAR linear power units.
- [Spectral Indices Catalog (`remote-sensing-indices.json`)](../../references/remote-sensing-indices.json): Machine-readable index formulas and domain metadata.
- [Contextual Threshold Profiles (`remote-sensing-threshold-profiles.json`)](../../references/remote-sensing-threshold-profiles.json): Conditional, non-universal classification cutoffs (e.g. dNBR fire severity, NDSI snow).
- [Scientific Source Registry (`remote-sensing-index-source-registry.json`)](../../references/remote-sensing-index-source-registry.json): Curated official agency documentation and peer-reviewed citations.

### Scientific rules of index interpretation
1. **Four distinct layers:** Distinguish (a) mathematical algebraic bounds, (b) typical observed landscape values, (c) local conditional classification thresholds, and (d) encoded storage integers (e.g. USGS index products scaled by `0.0001`).
2. **Values are not percentages:** NDVI = 0.65 does not equal 65% vegetation cover; NDWI = 0.40 does not mean 40% water depth; NDBI > 0 does not prove an urban surface.
3. **Disambiguate collisions:**
   - **NDWI:** McFeeters 1996 (Green - NIR) / (Green + NIR) maps open surface water; Gao 1996 (NIR - SWIR) / (NIR + SWIR) (NDMI) measures plant canopy moisture.
   - **NDSI:** Hall 1995 snow mapping requires NIR ≥ 0.11 to prevent water confusion. Distinct from salinity indices.
   - **RVI:** Radar Vegetation Index uses linear backscatter intensity power; distinct from Jordan 1969 optical Simple Ratio (NIR / Red).
4. **GEE and division protection:** Guard against zero denominators and NaNs. Note that `ee.Image.normalizedDifference()` silently masks pixels with negative inputs; use explicit expressions when analyzing dark water or shadows.

## Dynamic scientific source discovery workflow

When resolving unfamiliar indices, novel sensors, regional thresholds or calibration disputes, follow this non-exclusive discovery protocol:
1. **Intent detection:** Classify user goal (index calculation, physical interpretation, sensor selection, error diagnostics, temporal change).
2. **Known registry first:** Query `remote-sensing-indices.json` and `remote-sensing-index-source-registry.json` before initiating web search.
3. **Dynamic discovery:** Search official space agencies (USGS, NASA, ESA), peer-reviewed databases (Crossref, OpenAlex, NASA ADS), and academic publications. Do not restrict search to predetermined lists.
4. **Search expansion:** Use bilingual targeted queries combining index acronym, author, DOI, sensor, Level-2 product, processing baseline, and validation region.
5. **Rank by authority:** (a) Primary peer-reviewed paper / official product guide → (b) Regional empirical validation → (c) Official training (ARSET, STEP) → (d) Open-source code examples.
6. **Verification & two-source cross-check:** Verify formulas against the original publication; if two reputable sources diverge (e.g. different SWIR band definitions), record both with explicit reasons.
7. **Failure handling:** If network search is unavailable or unauthenticated, fall back to the curated local registry with clear confidence disclosure; never invent a DOI or threshold.

## Offline STAC discovery fixture

The [free STAC ItemCollection metadata test](../../examples/stac-offline/README.md) filters synthetic items by UTC acquisition date, approximate bbox and cloud fraction, without contacting or downloading assets. A bbox intersection is not a polygon intersection and sample fixture URLs are deliberately invalid. Real satellite imagery requires an authenticated/authorized source STAC API, pagination and asset-level verification.

## Esri raster AI references

[Esri raster deep learning](https://github.com/Esri/raster-deep-learning) demonstrates Python raster inference functions. Sample source code does not include rights to Image Analyst, model weights, satellite data or GPU runtimes. Verify band scales, masks, CRS and outputs, and use independently licensed inference engines when the target is standalone.

## Required workflow
1. Confirm product/sensor/collection/processing level, acquisition dates, AOI, coverage, spatial resolution, data license, access and expected data semantics.
2. Verify reflectance scaling, offsets, band order, radiometric processing, sun angle, saturation, nodata and **per-pixel** cloud/shadow QA; scene `CLOUD_COVER` alone is insufficient.
3. Pin target CRS and pixel grid: transform, origin, resolution, extent, resampling algorithm and nodata handling.
4. Preserve STAC item IDs, source assets, timestamps, version, QA choices, license and the complete compositing/reprojection recipe.
5. Test COG range requests and real partial reads; distinguish preview tiles from numerical analysis products. Manage Earth Engine auth, server/client semantics, quotas and export.
6. Validate against known reference pixels and imagery footprints, including missing scenes, time-zone boundaries, antimeridian and uneven observation counts.
7. Report independent computational evidence and failures; do not assert native Earth Engine/GDAL correctness from documentation-only checks.

Read [STAC/COG workflow](../../examples/remote-sensing/STAC_COG_WORKFLOW.md), [production workflows](../../references/production-workflows.md), [scientific GIS invariants](../../references/agent-reasoning/scientific-gis-reasoning.md) (including per-pixel QA masking, Landsat C2 L2 reflectance unpacking before division, zero-denominator guards, and McFeeters water NDWI vs Gao canopy NDWI disambiguation), and [quality benchmark](../../docs/QUALITY_BENCHMARK.md).

## NASA GIBS and Copernicus globe reference

[Earth View architecture](../../references/earth-view-architecture.md) separates public NASA GIBS image **visualizations** from authenticated Sentinel Process/Catalog products, dated layer previews and time-lapse mosaics. Preserve real acquisition dates and scientific band/cloud QA instead of treating screen pixels as calibrated source data.

## Agent-assisted source search, not invented Earth observations

Use [agentic-stac](https://github.com/opengeos/agentic-stac), [gee-agents](https://github.com/opengeos/gee-agents) and [geoai-skills](https://github.com/opengeos/geoai-skills) as independent implementation candidates only after host/auth/license checks. Query the [data catalog specialist](../geospatial-data-catalogs/SKILL.md) to find verified sources; ask [Geospatial AI Agents](../geospatial-ai-agents/SKILL.md) for schema validation, cost confirmations and reproducible provenance. Do not trust an LLM generated STAC asset URL without independently reading real item metadata.
