---
name: gis-development
description: Route GIS tasks to ArcGIS, QGIS, raster, remote sensing, KML, desktop, web and API specialists with verifiable tests.
license: MIT
---

# GIS Development — Agent Router

**Free-first:** [policy](../../references/free-first-policy.md); disclose costs.

**Examples:** [DEM](../../examples/terrain-slope/README.md), [STAC](../../examples/stac-offline/README.md).

**Intake:** [Global contract](../../references/repository-wide-skill-orchestration.md) → [Intent review](../prompt-intent-orchestrator/SKILL.md) → Router.

**Route:** [decision tree](../../references/agent-decision-tree.md); rendering ≠ analysis.

**Effort:** [guide](../../references/portable-execution-guidance.md).

**QGIS ribbon/UI.js:** [contract](../../references/ui-engine-architecture-contract.md); verify names before host/shell/renderer/engine choice.

## Choose specialists

| Task | Read first |
| --- | --- |
| ArcMap 10.x | [ArcGIS Toolbox](../arcgis-toolbox-engineering/SKILL.md) · [legacy](../../references/arcmap-legacy.md) |
| ArcGIS Pro / ArcPy | [ArcGIS Toolbox](../arcgis-toolbox-engineering/SKILL.md) |
| Global Mapper | [Specialist](../global-mapper-development/SKILL.md) |
| QGIS plugin / Processing algorithm | [QGIS Plugin Development](../qgis-plugin-development/SKILL.md) |
| QGIS engine | [Integration](../qgis-engine-integration/SKILL.md) |
| PostGIS, SpatiaLite, schema/indexes | [Spatial Databases](../spatial-databases/SKILL.md) |
| Raster/vector, GDAL, GeoPandas | [Geospatial Data Processing](../geospatial-data-processing/SKILL.md) |
| Remote sensing | [Pipelines](../remote-sensing-pipelines/SKILL.md) |
| MapLibre, web 2D, CesiumJS 3D | [Geospatial Web Mapping](../geospatial-web-mapping/SKILL.md) |
| Standalone CAD/GIS desktop / studio | [GIS Desktop Development](../gis-desktop-application-development/SKILL.md) |
| Clean-room reference parity | [Reference Implementation](../clean-room-reference-implementation/SKILL.md) |
| Android/iOS, GNSS, offline | [GIS Mobile Application Development](../gis-mobile-application-development/SKILL.md) |
| Command inventory, handlers, dead controls | [UI Command Audit](../gis-ui-command-audit/SKILL.md) |
| Windows UI, WebView2 and installer tests | [Desktop E2E Testing](../gis-desktop-e2e-testing/SKILL.md) |
| Data flow provenance, missing layers | [GIS Data Flow Diagnostics](../gis-data-flow-diagnostics/SKILL.md) |
| Images, thumbnails, logos | [Visual Assets](../visual-asset-discovery-integration/SKILL.md) |
| GIS code snippets, SDK examples, recipes | [GIS Code Discovery](../gis-code-discovery/SKILL.md) |
| UI/UX, keyboard, accessibility | [UI/UX Design & Testing](../gis-ui-ux-design-testing/SKILL.md) |
| Discover/download external data | [Geospatial Data Discovery](../geospatial-data-discovery/SKILL.md) |
| Source directories, repositories and STAC indexes | [Geospatial Data Catalogs](../geospatial-data-catalogs/SKILL.md) |
| GIS AI agents | [Agents](../geospatial-ai-agents/SKILL.md) |
| Architecture diagrams, structural changes | [Visualization](../gis-architecture-visualization/SKILL.md) (conditional) |
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


**Wizard:** [planner](../../project-wizard.html). **Arabic:** [i18n](../gis-internationalization-arabic/SKILL.md). **QA:** [guide](../../docs/PERFORMANCE_RELIABILITY.md).

## Rules (always apply)

[MCP/native routing](../../references/mcp-integration-workflow.md) follows domain preflight. Apply the [execution contract](../../references/repository-wide-skill-orchestration.md), [full guidance](../../references/gis-development-full-guidance.md) and [Security Guardian](../gis-security-guardian/SKILL.md): preserve sources, CRS/units/NoData, licenses, permissions and readback. Use [DoneProof](../completion-evidence/SKILL.md), [T0–T4 report](../../templates/GIS_ACCEPTANCE_REPORT.md) and [validator](../../scripts/validate_evidence.py). Static checks ≠ native proof.

**Shared checks:** [security](../../references/geospatial-security.md) · [performance](../../references/geospatial-performance.md).

**More:** [GIS software registry](../../references/gis-software-source-registry.md) · [antipatterns](../../references/gis-antipatterns.md) · [examples](../../examples/README.md).


## Project-level bootstrap and engineering governance

For a multi-step **software project** route the root project inspection,
structure inventory, required user-owned testing data/ and separate testing
results/, numbered plans and project-local AGENTS.md through the existing
[project governance contract](../../references/project-governance-workflow.md)
and [project helper](../../scripts/project_governance.py).
Read-only audit precedes authorized initialization. Register new persistent
folders with a purpose and preserve the host project's native build layout.

The Workflow Orchestrator is a *logical* engineering organization: Intent
defines goals, the architecture/toolchain roles assess the current project,
GIS specialists execute, Security Guardian checks untrusted dependencies,
QA verifies concrete outcomes and the existing Journal/DoneProof records
handoffs. Do not claim an actual multi-agent runtime unless host-native tools
and roles demonstrably execute.

For uncovered specialist needs, examine existing skills, source registries
and libraries first. Search outside only for a real gap; stage source-only
external candidates in target-project New Skill/ with no automatic activation.
Retain Remote Sensing, NVIDIA/Anthropic/Qt upstream references and the
[Token Optimization Triad](../../references/token-optimization-triad.md).
