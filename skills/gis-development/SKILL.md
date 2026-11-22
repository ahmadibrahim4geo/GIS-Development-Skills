---
name: gis-development
description: Route GIS tasks to ArcGIS, QGIS, raster, remote sensing, KML, desktop, web and API specialists with verifiable tests.
license: MIT
---

# GIS Development — Agent Router

**Free-first:** [policy](../../references/free-first-policy.md); disclose costs.

**Examples:** [DEM](../../examples/terrain-slope/README.md), [STAC](../../examples/stac-offline/README.md).

**Intake:** [Contract](../../references/repository-wide-skill-orchestration.md) → [Intent review](../prompt-intent-orchestrator/SKILL.md).

**Route:** [decision tree](../../references/agent-decision-tree.md); rendering ≠ analysis.

**Effort:** [guide](../../references/portable-execution-guidance.md).

**QGIS UI.js:** [contract](../../references/ui-engine-architecture-contract.md).

## Choose specialists

| Task | Read first |
| --- | --- |
| ArcMap 10.x | [ArcGIS Toolbox](../arcgis-toolbox-engineering/SKILL.md) · [legacy](../../references/arcmap-legacy.md) |
| ArcPy / Python toolbox | [ArcGIS Toolbox](../arcgis-toolbox-engineering/SKILL.md) |
| ArcGIS Pro SDK / C# add-in | [SDK workflow](../../references/arcgis-pro.md) · [code discovery](../gis-code-discovery/SKILL.md) |
| Global Mapper | [Specialist](../global-mapper-development/SKILL.md) |
| QGIS plugin / Processing algorithm | [QGIS Plugin Development](../qgis-plugin-development/SKILL.md) |
| QGIS engine | [Integration](../qgis-engine-integration/SKILL.md) |
| PostGIS, SpatiaLite, schema/indexes | [Spatial Databases](../spatial-databases/SKILL.md) |
| Raster/vector, GDAL, GeoPandas | [Geospatial Data Processing](../geospatial-data-processing/SKILL.md) |
| Remote sensing | [Pipelines](../remote-sensing-pipelines/SKILL.md) |
| MapLibre, web 2D, CesiumJS 3D | [Geospatial Web Mapping](../geospatial-web-mapping/SKILL.md) |
| HTML and browser UI | [Modern Web Guidance](../modern-web-guidance/SKILL.md) + UI/UX Pro Max |
| Standalone CAD/GIS | [Desktop](../gis-desktop-application-development/SKILL.md) |
| Clean-room parity | [Reference Implementation](../clean-room-reference-implementation/SKILL.md) |
| Android/iOS, GNSS, offline | [Mobile](../gis-mobile-application-development/SKILL.md) |
| UI commands and handlers | [Command Audit](../gis-ui-command-audit/SKILL.md) |
| Windows, WebView2, installers | [Desktop E2E](../gis-desktop-e2e-testing/SKILL.md) |
| Lineage and missing layers | [Data Flow Diagnostics](../gis-data-flow-diagnostics/SKILL.md) |
| Images, thumbnails, logos | [Visual Assets](../visual-asset-discovery-integration/SKILL.md) |
| GIS snippets and SDK examples | [Code Discovery](../gis-code-discovery/SKILL.md) |
| UI/UX, keyboard, accessibility | [UI/UX Design & Testing](../gis-ui-ux-design-testing/SKILL.md) |
| Discover/download external data | [Geospatial Data Discovery](../geospatial-data-discovery/SKILL.md) |
| Source directories, repositories and STAC indexes | [Geospatial Data Catalogs](../geospatial-data-catalogs/SKILL.md) |
| GIS AI agents | [Agents](../geospatial-ai-agents/SKILL.md) |
| Architecture diagrams and changes | [Visualization](../gis-architecture-visualization/SKILL.md) (conditional) |
| MCP/native tools and fallback | [MCP Tool Orchestration](../mcp-integration-and-tool-orchestration/SKILL.md) |
| DEM, terrain, hydrology, LiDAR | [Terrain / Hydrology / LiDAR](../terrain-hydrology-lidar/SKILL.md) |
| Untrusted GIS inputs, secrets and security | [GIS Security Guardian](../gis-security-guardian/SKILL.md) (cross-cutting) |
| Integrate GIS HTTP APIs safely | [Geospatial API Integration](../geospatial-api-integration/SKILL.md) |
| Geocoding | [API Integration](../geospatial-api-integration/SKILL.md) · [providers](../../references/geocoding-place-search.md) |
| Gazetteer search / scale-aware labels | [World Gazetteer](../../references/world-gazetteer-reference-layer.md) |
| WKID, projection, transformation, vertical datum | [Coordinate Reference Systems](../coordinate-reference-systems/SKILL.md) |
| Symbology / map layout | [Cartography](../gis-cartography-symbology/SKILL.md) |
| OS/device permissions and sensors | [System Capabilities & Permissions](../system-capabilities-and-permissions/SKILL.md) |
| Device time/location/sunlight | [Device Context](../gis-device-context/SKILL.md) |
| KML/KMZ / Earth viewers | [KML](../kml-kmz-engineering/SKILL.md) · [Earth](../../references/google-earth-pro-engineering.md) · [Timeline](../../references/historical-imagery-timeline.md) |


[Planner](../../project-wizard.html) · [Arabic i18n](../gis-internationalization-arabic/SKILL.md) · [QA](../../docs/PERFORMANCE_RELIABILITY.md).

## Rules (always apply)

[MCP routing](../../references/mcp-integration-workflow.md) follows preflight. Apply [execution](../../references/repository-wide-skill-orchestration.md), [GIS](../../references/gis-development-full-guidance.md) and [security](../gis-security-guardian/SKILL.md) rules for sources, CRS, units, NoData, licenses, permissions and readback. Verify with [DoneProof](../completion-evidence/SKILL.md), the [T0–T4 report](../../templates/GIS_ACCEPTANCE_REPORT.md) and [validator](../../scripts/validate_evidence.py).

**Shared checks:** [security](../../references/geospatial-security.md) · [performance](../../references/geospatial-performance.md).

**More:** [software sources](../../references/gis-software-source-registry.md) · [antipatterns](../../references/gis-antipatterns.md) · [project preflight](../../references/project-governance-workflow.md).
