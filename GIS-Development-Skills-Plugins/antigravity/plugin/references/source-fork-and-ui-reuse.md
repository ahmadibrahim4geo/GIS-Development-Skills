# Open-Source Forking, QGIS Source Engineering & Component Reuse

> Companion manual (`REQ-EV2-008..011`, `042`, `043`) for [`qgis-engine-integration`](../skills/qgis-engine-integration/SKILL.md), [`geospatial-engine-selection`](../skills/geospatial-engine-selection/SKILL.md), and [`clean-room-reference-implementation`](../skills/clean-room-reference-implementation/SKILL.md).

---

## 1. Six-Level Open-Source Reuse Preference Hierarchy (`REQ-EV2-008`)

Always prefer the lightest reversible architecture that meets requirements cleanly:

1. **Profile / Host Configuration (`configure-host`)** — Hide/rearrange menus or toolbars cleanly inside QGIS Profiles / `Customization.ini` with zero upstream code fork.
2. **Official Plugin / Extension (`extend-host`)** — PyQGIS Plugin, Processing Provider, ArcGIS Pro SDK Add-in (only when licensed ArcGIS Pro is explicitly requested/authorized), without rebuilding core.
3. **Standalone Libraries (`GDAL` / `PROJ` / `GEOS` / `MapLibre`)** — For narrow CRS, format, or tiled viewer tools (`E08`), compose permissive libraries (`MIT`/`BSD`) rather than bundling a 1+ GB desktop GIS.
4. **Selective Component Reuse (`source-component-reuse`)** — Reuse well-isolated Apache/MIT/BSD modules after license compatibility and test verification.
5. **Controlled Source Fork (`source-fork`, `GPLv2+` Review Mandatory)** — Fork `qgis/QGIS` only when deep UI stripping or core modification cannot be solved via plugin/profiles, honoring reciprocal GPL source/notice duties (`E38`).
6. **Independent Multi-Engine / Custom App (`ADR` Required)** — Author original UI shell over tested engines (`reference-inspired-ui` / `multi-engine-composition`) when domain UX differs fundamentally from QGIS Desktop.

---

## 2. QGIS Source Engineering Handbook (`17` Official Sources, `REQ-EV2-043`)

Inspect exact commit/tag, Qt version (`Qt 5`/`Qt 6`), GDAL, PROJ, GEOS, and SIP/PyQt ABI **before** removing or compiling code. Canonical official references:
1. `qgis/QGIS` Core repo · 2. `src/core/` (`QgsProject`, `QgsVectorLayer`, `QgsCoordinateTransform`) · 3. `src/gui/` (`QgsMapCanvas`, dialogs) · 4. `src/app/` (`QgisApp`, `qgisapp.cpp`) · 5. `src/ui/qgisapp.ui` *(primary Qt Designer action manifest)* · 6. `src/analysis/` (`raster`, `network`, `interpolation`) · 7. `python/plugins/processing/` · 8. `src/providers/` (`ogr`, `gdal`, `postgres`, `wms`) · 9. `src/3d/` (`Qgs3DMapScene`) · 10. `src/server/` (`QgsServer`) · 11. `qgis/QGIS-Enhancement-Proposals` (`QEP` design RFCs) · 12. `qgis/QGIS-Documentation` · 13. `PyQGIS Developer Cookbook` · 14. `QGIS C++ API Docs` · 15. `QGIS Server Training/Config Docs` · 16. `INSTALL.md` (`vcpkg` / `OSGeo4W` / CMake Presets) · 17. `scripts/` & `tests/src/` *(upstream C++/Python test suite)*.

**Inspection Rule (`inventory_ui_actions.py`):** Always parse `.ui` XML read-only using bounded parsers (`5 MiB` cap, `<!DOCTYPE`/`<!ENTITY` forbidden, symlink traversal blocked). Static action extraction yields `handlers_verified=False` and `dynamic_actions_verified=False` until C++ `connect(...)` / runtime build confirms them.

---

## 3. Seven-Step Dependency Graph & `KEEP/HIDE/DISABLE/REMOVE/REPLACE/DEFER` (`REQ-EV2-009`, `010`)

Before deleting any action/widget from a fork:
1. Map `UI Element (.ui QAction / Menu / Toolbar)` -> 2. `Shortcut / QAction objectName` -> 3. `C++ Slot / PyQGIS Handler` -> 4. `Service / QgsProject / Undo` -> 5. `Data Provider / GDAL / PROJ` -> 6. `Persistent State (.qgz / QSettings)` -> 7. `Upstream SHA + Binary Build Baseline`.

Follow **Safe Stripping Progression (`HIDE` before `REMOVE`)**: start with `HIDE` in UI customization, run roundtrip + shortcut QA (`E-25`, `E-26`), verify zero broken runtime signals, **only then** consider `DISABLE` or `REMOVE`. Never mark a backend-required module as `REMOVE` (`E25`).

### Sixteen Protected Background & Core Infrastructures (DO NOT Blindly Remove)
`1. PROJ CRS & datum grids` · `2. QUndoStack Undo/Redo` · `3. .qgz / Atomic Project Save & Load` · `4. OGR/GDAL/Memory Core Providers` · `5. GEOS Geometry Validity & Topology` · `6. QgsMessageLog Diagnostics` · `7. QgsApplication.initQgis() Profile Setup` · `8. Expression Engine Context` · `9. QgsCoordinateTransformContext` · `10. QgsLayerTreeRegistryBridge` · `11. Selection & Feature ID Registry` · `12. QgsTaskManager Async Cancel` · `13. QgsAuthManager Credential Store` · `14. QgsStyle / QML Symbology IO` · `15. UTF-8 / Arabic BiDi Codecs` · `16. Clean-Machine Runtime Env (qt.conf, PROJ_DATA, VC++/Qt libs)`.

---

## 4. Branding Isolation & Clean-Machine Packaging (`REQ-EV2-011`, `E29`, `E38`)

- Keep custom title/icons/splash in isolated overlay patches; keep upstream `COPYING`, `LICENSE`, `THIRD_PARTY_NOTICES`, and pinned QGIS release tag intact.
- Measure startup latency and binary bundle size *objectively* before/after cleanup.
- Validate on a clean OS VM without preinstalled OSGeo4W/QGIS (`E29`, `E30`); mark clean-machine verification strictly **`NOT_RUN`** if clean VM is unavailable.

---

## 5. Twenty-Seven Benchmark OSS Projects & `QGIS` vs `GeoLibre` vs `RustGIS` (`REQ-EV2-042`)

Canonical IDs live in [`project-catalog.json`](project-catalog.json) & [`engine-capability-profiles.json`](engine-capability-profiles.json):
`qgis-qgis`, `opengeos-geolibre`, `opengeos-rustgis`, `openjump-gis-openjump`, `gvsig-gvsig-desktop`, `locationtech-udig`, `saga-gis-saga-gis`, `osgeo-grass`, `jblindsay-whitebox-tools`, `osgeo-gdal`, `osgeo-proj`, `libgeos-geos`, `pdal-pdal`, `orfeotoolbox-otb`, `senbox-org-snap-desktop`, `kde-marble`, `openorienteering-mapper`, `maplibre-maplibre-native`, `maplibre-maplibre-gl-js`, `openlayers-openlayers`, `cesiumgs-cesium`, `mapsui-mapsui`, `opengisch-qfield`, `merginmaps-mobile`, `josm-josm`, `openstreetmap-id`, `opendronemap-odm`.

| Dimension | `QGIS` (`C++/Qt`) | `GeoLibre` | `RustGIS` (`Rust`) |
|---|---|---|---|
| **Maturity & Scope** | Production full desktop/server/PyQGIS ecosystem | Modern cloud-native viewer & web/desktop exploration | Rust native desktop/algorithm architecture under active evolution |
| **License** | `GPL-2.0-or-later` *(copyleft obligations on forks)* | Inspect upstream LICENSE per target module before linking | Inspect upstream permissive/copyleft license carefully |
| **GPKG / GeoTIFF / PROJ / RTL PoC Gate** | Native GDAL/OGR, PROJ 9+, Qt BiDi (`QgsVectorLayer`, `QgsRasterLayer`) | Verify exact native GeoTIFF/CRS/RTL capabilities locally — never equate viewer with GDAL workbench (`E14`) | Audit real implemented vector/raster readback vs planned Rust modules before production |
