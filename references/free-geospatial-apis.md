# Free & public GIS APIs and web services — provider selection

**Reviewed 2026-10-24.** Machine-readable, filterable entries: [`free-geospatial-apis.json`](free-geospatial-apis.json). "Free" is not synonymous with commercial use, unlimited requests, full-resolution scientific data, offline caching, anonymous download, or permission to distribute imagery.

## Quick reference by domain

| Domain | Primary providers | Access caveat |
|---|---|---|
| Forecast and historical climate | [Open-Meteo](https://open-meteo.com/en/docs), [NASA POWER](https://power.larc.nasa.gov/docs/services/api/temporal/), [Copernicus CDS](https://cds.climate.copernicus.eu/how-to-api) | Open-Meteo free service is non-commercial with explicit quotas; NASA POWER enforces fair use; CDS needs account/token and dataset licence |
| Point elevation & DEM | [Open-Meteo Elevation](https://open-meteo.com/en/docs/elevation-api), [OpenTopography](https://opentopography.org/developers), [Open-Elevation](https://www.open-elevation.com/), [USGS EPQS](https://www.usgs.gov/the-national-map-data-delivery/gis-data-download) | Open-Meteo elevation GLO-90 ~90m; OpenTopography requires personal key; Open-Elevation tiny free quotas; USGS primarily US only |
| Satellite imagery catalog | [Earth Search](https://element84.com/earth-search), [Planetary Computer](https://planetarycomputer.microsoft.com/docs/), [Copernicus Data Space](https://dataspace.copernicus.eu/analyse/apis) | STAC metadata access differs from asset download/auth, COG CORS and redistribution terms |
| Satellite image tiles | [NASA GIBS](https://www.earthdata.nasa.gov/engage/open-data-services-software/earthdata-developer-portal/gibs-api) | WMS/WMTS visualize imagery; scientific raster analysis requires real source data |
| Basemaps | [OpenFreeMap](https://openfreemap.org/quick_start/), [OSMF tiles](https://operations.osmfoundation.org/policies/tiles/) | OpenFreeMap hosted maps no key; OSMF tiles are NOT an unlimited production/offline tile service |
| OSM POIs & geocoding | [Overpass](https://wiki.openstreetmap.org/wiki/Overpass_API), [Nominatim](https://operations.osmfoundation.org/policies/nominatim/) | Volunteer services; restricted usage. Never auto-generate generic Nominatim integration into apps |
| Soil | [ISRIC SoilGrids](https://isric.org/explore/soilgrids) | REST service **temporarily paused** in provider notice; prefer data download/WebDAV or WCS |
| Biodiversity | [GBIF API](https://techdocs.gbif.org/en/openapi/) | Search pagination limit; use dataset downloads for bulk, maintain provenance |

## Recommended API selection procedure for AI agents

1. Declare use case, output variables and units, spatial/temporal coverage, data resolution and required reproducibility.
2. Read the catalog entry's `access`, `authentication`, `limits`, `attribution`, and `caveat` fields; read provider live docs before integration.
3. Select **the dataset as well as the endpoint**: model reanalysis != ground station; imagery rendering != analysis-ready pixels; elevation raster != precise surveyed point.
4. Determine no-key/keyed, non-commercial/commercial, rate limits and cost; require explicit owner credentials. Store tokens outside Git and UI logs. Never hardcode a personal OpenTopography key in redistributable software.
5. Build adapters with per-provider version, retry only safe temporary errors (429/5xx with exponential backoff), cache where expressly permitted, request timeout, error telemetry, fallback, clear source attribution and license metadata.
6. Verify response shape, CRS, axis order, vertical datum, pixel scale, timezone, missing values, geographic and temporal coverage. Keep downloaded values labelled by exact dataset/source.
7. **Do not** bulk query public Nominatim, OSMF tiles, Overpass or soil services; use legitimate extracts, self-hosting or contracted providers when workloads are large.
8. Mark endpoints temporarily unavailable or unverified when evidence is insufficient. Never claim that a docs example has been live-tested unless it was.

## Worked examples (examples are documented, NOT live service tests)

Open-Meteo noncommercial forecast for Cairo (JSON):

```text
https://api.open-meteo.com/v1/forecast?latitude=30.0444&longitude=31.2357&hourly=temperature_2m,relative_humidity_2m
```

NASA POWER daily point meteorology (JSON):

```text
https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M&community=AG&longitude=31.2357&latitude=30.0444&start=20230101&end=20230103&format=JSON
```

OpenFreeMap MapLibre style (map display, **not** a GeoTIFF asset):

```text
https://tiles.openfreemap.org/styles/liberty
```

### Critical current provider warnings

- Open-Meteo [free terms](https://open-meteo.com/en/terms): <10,000 calls/day, <5,000/hour and <600/min; free noncommercial only; its data are CC BY 4.0, server code AGPLv3.
- OpenTopography [API developer terms](https://opentopography.org/developers): personal free keys, academic/nonacademic daily quotas; do **not** embed someone else's key in apps or proxy other users through it.
- OpenFreeMap [offline rules](https://openfreemap.org/quick_start/): offline download caps differ from public map views. OSM contributors' attribution applies.
- ISRIC [SoilGrids](https://isric.org/explore/soilgrids) currently reports its REST API temporarily paused, no restoration ETA.
- Nominatim [acceptable-use policy](https://operations.osmfoundation.org/policies/nominatim/) forbids autocomplete/systematic harvesting and generic embedding in code-generating tools; entries here are **documentation only**, not permission to programmatically generate an integration.

## Search and validation

```bash
python scripts/validate_api_catalog.py
python scripts/search_api_catalog.py --category terrain-elevation
python scripts/search_api_catalog.py --access free-noncommercial
python scripts/search_api_catalog.py --query sentinel
```

The catalog is an independently maintained curated reference, not an API aggregator, credential provider, service uptime guarantee, or proxy. All third-party services retain their own terms.