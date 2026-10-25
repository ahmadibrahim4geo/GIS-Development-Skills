---
name: gis-development
description: Route GIS tasks to ArcGIS, QGIS, raster, remote sensing, KML, desktop, web and API specialists with verifiable tests.
license: MIT
---

# GIS Development — Agent Router

**Free-first:** use [no-cost policy](../../references/free-first-policy.md). Disclose commercial host/API limits and offer verified free alternatives; never silently require payment.

**Offline examples:** [DEM slope](../../examples/terrain-slope/README.md), [STAC](../../examples/stac-offline/README.md). [License audit](../../references/upstream-license-audit.md) is not native proof.

**Intake:** [Plan and approve free-form requests](../prompt-intent-orchestrator/SKILL.md) before GIS routing.

**Load selectively:** use the [decision tree](../../references/agent-decision-tree.md) to select specialists; rendering is not spatial analysis.

## Choose specialists

| Task | Read first |
| --- | --- |
| ArcMap 10.x, Python 2.7, older `arcpy.mapping` | [ArcGIS Toolbox Engineering](../arcgis-toolbox-engineering/SKILL.md) and [legacy reference](../../references/arcmap-legacy.md) |
| ArcGIS Pro, ArcPy, `.pyt`, geoprocessing | [ArcGIS Toolbox Engineering](../arcgis-toolbox-engineering/SKILL.md) |
| Global Mapper / Blue Marble GMS, Python and licensed SDK | [Global Mapper Development](../global-mapper-development/SKILL.md) |
| QGIS plugin / Processing algorithm | [QGIS Plugin Development](../qgis-plugin-development/SKILL.md) |
| Independent QGIS libraries, PyQGIS workers, Server | [QGIS Engine Integration](../qgis-engine-integration/SKILL.md) |
| PostGIS, SpatiaLite, schema/indexes | [Spatial Databases](../spatial-databases/SKILL.md) |
| Raster/vector, GDAL, GeoPandas, spatial batch | [Geospatial Data Processing](../geospatial-data-processing/SKILL.md) |
| Landsat, Sentinel, Earth Engine, STAC, COG | [Remote Sensing Pipelines](../remote-sensing-pipelines/SKILL.md) |
| MapLibre, web 2D, CesiumJS globe/3D | [Geospatial Web Mapping](../geospatial-web-mapping/SKILL.md) |
| Independent GIS desktop application / installer | [GIS Desktop Development](../gis-desktop-application-development/SKILL.md) |
| Discover/download external data | [Geospatial Data Discovery](../geospatial-data-discovery/SKILL.md) |
| Find source directories, data repositories and STAC indexes | [Geospatial Data Catalogs](../geospatial-data-catalogs/SKILL.md) |
| Automate PyQGIS / STAC / GeoAI / Earth Engine with an agent | [Geospatial AI Agents](../geospatial-ai-agents/SKILL.md) |
| DEM, terrain, hydrology, LiDAR / point clouds | [Terrain / Hydrology / LiDAR](../terrain-hydrology-lidar/SKILL.md) |
| Untrusted GIS inputs, secrets and security | [GIS Security Guardian](../gis-security-guardian/SKILL.md) (cross-cutting) |
| Integrate GIS HTTP APIs safely | [Geospatial API Integration](../geospatial-api-integration/SKILL.md) |
| Search place names / geocode addresses / autocomplete | [Geospatial API Integration](../geospatial-api-integration/SKILL.md) + [provider selection guide](../../references/geocoding-place-search.md) |
| Gazetteer search / scale-aware labels | [World Gazetteer](../../references/world-gazetteer-reference-layer.md) |
| WKID, projection, transformation, vertical datum | [Coordinate Reference Systems](../coordinate-reference-systems/SKILL.md) |
| Point/line/polygon/raster symbols, color ramps, map layout | [GIS Cartography & Symbology](../gis-cartography-symbology/SKILL.md) |
| Device time/date/timezone, permission-controlled location, Sunlight simulation | [GIS Device Context](../gis-device-context/SKILL.md) |
| KML/KMZ, Earth-like viewers and timeline | [KML](../kml-kmz-engineering/SKILL.md) · [Earth Pro](../../references/google-earth-pro-engineering.md) · [Historical imagery](../../references/historical-imagery-timeline.md) |


**Wizard:** [planner](../../project-wizard.html). **Arabic:** [i18n](../gis-internationalization-arabic/SKILL.md). **QA:** [guide](../../docs/PERFORMANCE_RELIABILITY.md).

## Global rules (always apply)

1. **Do not silently modify sources:** default to new output files, explicit user approval for destructive editing and backups.
2. **Geospatial correctness:** verify CRS/axis order, true transformations, area/distance units, Z/vertical datum, invalid geometries, NoData, raster alignment and output readback.
3. **Compatibility:** never mix ArcMap Python 2 with Pro APIs; pin host/runtime and validate third-party licensing/authentication/quotas.
4. **Security:** apply [GIS Security Guardian](../gis-security-guardian/SKILL.md) at preflight, runtime and release gates, plus [geospatial input rules](../../references/geospatial-security.md) for files, APIs, SQL and credentials. A policy document does not enforce runtime sandbox permissions.
5. **Performance:** measure real inputs using [performance guidance](../../references/geospatial-performance.md).
6. **Evidence:** complete [the acceptance report](../../templates/GIS_ACCEPTANCE_REPORT.md) and check it with [the evidence validator](../../scripts/validate_evidence.py). Record T0–T4 honestly; generic syntax checks or UI mockups are **not** native GIS execution.
7. **References:** [projects](../../references/project-catalog.json), [APIs](../../references/free-geospatial-apis.json), [data](../../references/geospatial-data-repositories.json) require source/license verification.

**More:** [full guide](../../references/gis-development-full-guidance.md) · [antipatterns](../../references/gis-antipatterns.md) · [examples](../../examples/README.md).

## Required cross-skill orchestration

Read the [repository-wide prompt, data and command flow contract](../../references/repository-wide-skill-orchestration.md). This router is invoked after the Intent Orchestrator has normalized and reviewed consequential requests. Route by delivery target, assign one owner per output, load only necessary specialists plus Security Guardian, check dependencies and conflicts, and return verified outcomes to the Development Journal. Do not allow a specialist to execute directly from an unreviewed user prompt; read-only questions need no unnecessary approval ceremony.
