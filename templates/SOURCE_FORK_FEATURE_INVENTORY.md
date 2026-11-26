# Open-Source Fork Feature & Action Inventory (`KEEP / HIDE / DISABLE / REMOVE / REPLACE / DEFER`)

> Mandatory inventory prior to trimming or forking an open-source desktop application (such as `QGIS` or `FreeCAD`) to preserve core architecture, CRS, Undo/Redo, providers, and project save integrity.

- **Upstream Repository & Pinned Tag/SHA:**
- **License & Redistribution Obligations:**
- **Protected Backend Invariants (16 Critical Areas):** CRS/Datum/Ellipsoid transforms, `QUndoStack`/Edit transactions, Project Save/Load/Recovery, Vector & Raster Data Providers, Layer Registry & Selection model, Geometry Validity & Snapping, Expression Engine, Processing Framework, Task Manager/Threading, Symbology/Renderer pipeline, Layout/Export serialization, Arabic/UTF-8 BiDi text encoding, Plugin boundary, Error logging, Security path checks, Preferences/Profile paths.

## UI Action & Subsystem Disposition Matrix

| Item / `QAction` (`objectName`) | Source Location (`.ui` / module) | Subsystem Role | Disposition (`KEEP` / `HIDE` / `DISABLE` / `REMOVE` / `REPLACE` / `DEFER`) | Dependency / Backend Guardrail | Replacement / Adapter Target | Static Inventory Ref (`inventory_ui_actions.py`) |
|---|---|---|---|---|---|---|
| | | | | | | |

## Safe Cleanup Sequence
1. Run read-only static `.ui` inventory (`python scripts/inventory_ui_actions.py --root <ui_dir>`) — note `handlers_verified: false`.
2. Classify all actions and isolate visibility changes (`HIDE` / `DISABLE` / profile settings) before attempting source deletion.
3. Verify dependency map across signals/slots, Processing algorithms, and project schemas before marking `REMOVE`.
4. Confirm build on clean machine + project load/edit/save/readback (`T2–T4`) before release.
