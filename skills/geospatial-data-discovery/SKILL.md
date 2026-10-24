---
name: geospatial-data-discovery
description: Find appropriate, legally usable GIS datasets and working geospatial APIs using verified public metadata catalogs, STAC, NASA, Earth Engine, elevation, weather and basemap providers. Choose by location, time, resolution and license; distinguish a metadata index from an actual API.
license: MIT
---

# Geospatial Data Discovery

Use for DEM, climate, satellite images, environmental rasters, OSM/POIs and geospatial downloads.

## Procedure

1. Ask for or infer domain, area, period, resolution, coordinate system, output type and intended commercial/noncommercial use.
2. Read `../../references/free-geospatial-apis.md` and its JSON catalog. For supplementary discovery, read `../../references/gishub-software.md` and `../../references/project-catalog.json`.
3. Browse catalogs like `opengeos/geospatial-data-catalogs`, `opengeos/stac-index-catalogs`, `opengeos/NASA-CMR-STAC` as **indexes**, never assume an indexed API is available.
4. Verify the *underlying* provider's official page for current access, key requirements, geographic/time coverage, quotas, TOS, attribution and CORS.
5. Try a small legally accessible sample if tools/environment permit. Confirm CRS, pixel size, date, DEM vertical datum, NoData and geolocation.
6. Provide a reproducible download workflow, metadata/provenance fields, failure/retry handling, and license caveats.
7. Don't fabricate endpoints, keys, imagery dates or missing measurements. Never embed users' API tokens in source.
8. Disclose untested endpoints and mark current live access as unverified if it was not checked.

## Prefer

- Climate/time series: verified Open-Meteo and NASA POWER provider documentation.
- Elevation/terrain: authoritative DEM source with verified grid, datum and coverage; access quota may need a key.
- Satellite: STAC-compatible sources or provider catalogs with independently validated scenes/assets.
- Basemaps: verify per-provider commercial terms, caching permissions and attribution.
- ArcGIS Pro/ArcMap/QGIS downstream: convert to supported formats and honor each application's runtime.

## Acceptance criteria

- [ ] True provider/source URL, not only a GitHub metadata catalog
- [ ] Authentication, rate limits, license and attribution documented
- [ ] Tested—or clearly not tested—availability/extent/epoch/resolution
- [ ] GIS-safe CRS, NoData, units and output formats
- [ ] Reproducible processing and failure handling
