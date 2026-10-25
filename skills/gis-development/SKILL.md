---
name: gis-development
description: Route GIS tasks to ArcGIS, QGIS, raster, remote sensing, KML, desktop, web and API specialists with verifiable tests.
license: MIT
---

# GIS Development — Agent Router

**Free-first:** use [no-cost policy](../../references/free-first-policy.md). Disclose paid limits; prefer verified free alternatives.

**Examples:** [DEM](../../examples/terrain-slope/README.md), [STAC](../../examples/stac-offline/README.md).

**Intake:** [Global contract](../../references/repository-wide-skill-orchestration.md) → [Intent review](../prompt-intent-orchestrator/SKILL.md) → Router.

**Route:** [decision tree](../../references/agent-decision-tree.md); rendering ≠ analysis.

## Choose specialists

| Task | Read first |
| --- | --- |
| ArcMap 10.x | [ArcGIS Toolbox](../arcgis-toolbox-engineering/SKILL.md) · [legacy](../../references/arcmap-legacy.md) |
| ArcGIS Pro / ArcPy | [ArcGIS Toolbox](../arcgis-toolbox-engineering/SKILL.md) |
| Global Mapper | [Specialist](../global-mapper-development/SKILL.md) |
| QGIS plugin / Processing algorithm | [QGIS Plugin Development](../qgis-plugin-development/SKILL.md) |
| QGIS engine | [Integration](../qgis-engine-integration/SKILL.md) |
| PostGIS, SpatiaLite, schema/indexes | [Spatial Databases](../spatial-databases/SKILL.md) |
| Raster/vector, GDAL, GeoPandas, spatial batch | [Geospatial Data Processing](../geospatial-data-processing/SKILL.md) |
| Remote sensing | [Pipelines](../remote-sensing-pipelines/SKILL.md) |
| MapLibre, web 2D, CesiumJS globe/3D | [Geospatial Web Mapping](../geospatial-web-mapping/SKILL.md) |
| Independent GIS desktop application / installer | [GIS Desktop Development](../gis-desktop-application-development/SKILL.md) |
| Discover/download external data | [Geospatial Data Discovery](../geospatial-data-discovery/SKILL.md) |
| Find source directories, data repositories and STAC indexes | [Geospatial Data Catalogs](../geospatial-data-catalogs/SKILL.md) |
| GIS AI agents | [Agents](../geospatial-ai-agents/SKILL.md) |
| DEM, terrain, hydrology, LiDAR / point clouds | [Terrain / Hydrology / LiDAR](../terrain-hydrology-lidar/SKILL.md) |
| Untrusted GIS inputs, secrets and security | [GIS Security Guardian](../gis-security-guardian/SKILL.md) (cross-cutting) |
| Integrate GIS HTTP APIs safely | [Geospatial API Integration](../geospatial-api-integration/SKILL.md) |
| Geocoding | [API Integration](../geospatial-api-integration/SKILL.md) · [providers](../../references/geocoding-place-search.md) |
| Gazetteer search / scale-aware labels | [World Gazetteer](../../references/world-gazetteer-reference-layer.md) |
| WKID, projection, transformation, vertical datum | [Coordinate Reference Systems](../coordinate-reference-systems/SKILL.md) |
| Symbology / map layout | [Cartography](../gis-cartography-symbology/SKILL.md) |
| Device time/location/sunlight | [Device Context](../gis-device-context/SKILL.md) |
| KML/KMZ / Earth viewers | [KML](../kml-kmz-engineering/SKILL.md) · [Earth](../../references/google-earth-pro-engineering.md) · [Timeline](../../references/historical-imagery-timeline.md) |


**Wizard:** [planner](../../project-wizard.html). **Arabic:** [i18n](../gis-internationalization-arabic/SKILL.md). **QA:** [guide](../../docs/PERFORMANCE_RELIABILITY.md).

## Global rules (always apply)

1. **Protect sources:** use new outputs; approve destructive edits and back up.
2. **Geospatial correctness:** verify CRS/axis order, true transformations, area/distance units, Z/vertical datum, invalid geometries, NoData, raster alignment and output readback.
3. **Compatibility:** separate ArcMap/Pro; pin runtime, licenses and quotas.
4. **Security:** apply [GIS Security Guardian](../gis-security-guardian/SKILL.md) at preflight, runtime and release gates, plus [geospatial input rules](../../references/geospatial-security.md) for files, APIs, SQL and credentials. A policy document does not enforce runtime sandbox permissions.
5. **Performance:** [measure real inputs](../../references/geospatial-performance.md).
6. **Evidence:** complete [the acceptance report](../../templates/GIS_ACCEPTANCE_REPORT.md) and check it with [the evidence validator](../../scripts/validate_evidence.py). Record T0–T4 honestly; generic syntax checks or UI mockups are **not** native GIS execution.
7. **References:** [projects](../../references/project-catalog.json), [APIs](../../references/free-geospatial-apis.json), [data](../../references/geospatial-data-repositories.json) require source/license verification.

**More:** [full guide](../../references/gis-development-full-guidance.md) · [antipatterns](../../references/gis-antipatterns.md) · [examples](../../examples/README.md).
