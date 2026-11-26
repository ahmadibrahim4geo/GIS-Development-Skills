# Reference-Inspired UI Mapping & Clean-Room Architecture (`ArcGIS Pro`, `Google Earth Pro`, `Global Mapper`, `ENVI`, `CityEngine`)

> Companion specification (`REQ-EV2-012`, `024`, `054`) for [`clean-room-reference-implementation`](../skills/clean-room-reference-implementation/SKILL.md), [`geospatial-engine-selection`](../skills/geospatial-engine-selection/SKILL.md), and [`gis-ui-command-audit`](../skills/gis-ui-command-audit/SKILL.md).

---

## 1. Strict Intellectual Property & Clean-Room Boundary (`E02`, `E40`, `E45`)

- **Allowed:** Studying *observable workflows, user mental models, panel layouts, ribbon grouping concepts, and interoperable public formats* (`GeoPackage`, `GeoTIFF`, `KML`, `COG`, `CIM`-documented concepts) to design an **original application** powered by free/OSS engines (`recommend_stack.py` mode `reference-inspired-ui`).
- **Strictly Forbidden:** Copying proprietary icons, splash logos, `.daml` Ribbon manifests, commercial DLLs/assemblies (`ArcGIS.Desktop.*`), private endpoints, or pretending a proprietary host runtime (`ArcGIS Pro SDK`) is a free standalone library (`E44`). Always pair with permissive icon packs (`Lucide`, `Fluent System Icons`) and original branding (`Z EARTH` pattern).

---

## 2. Seven-Step Clean-Room Behavioral Transformation Workflow

1. **Reference Inventory (`TEMPLATE`):** Record observable workflows & commands in [`REFERENCE_UI_COMMAND_MAPPING.md`](../templates/REFERENCE_UI_COMMAND_MAPPING.md).
2. **Behavioral Feature Map:** Translate proprietary menu terms into generic GIS domain intents (`Map Viewport`, `Selection`, `Coordinate Conversion`, `Spatial Analysis`, `Export & Readback`).
3. **Select Independent UI Framework from 20 Curated Frameworks (`V2 §24.3`, `E34`):**
   - **Desktop C++ / Python:** `Qt Widgets`, `Qt QML`, `PySide6`, `PyQt6`, `wxWidgets` + `Qt-Advanced-Docking-System` / `SARibbon`.
   - **Windows / Cross-.NET:** `WPF` (`Fluent.Ribbon`, `AvalonDock`, `MaterialDesignInXAML`), `WinUI 3` (`Windows Community Toolkit`), `Avalonia UI` (`Dock`), `.NET MAUI`.
   - **Web-Hybrid / Cross-Platform UI:** `Tauri`, `Electron`, `WebView2`, `Flutter`, plus SPA frameworks `React`, `Vue`, `Svelte`, `Angular` with `GoldenLayout` / `Gridstack` and `Lucide` / `Fluent Icons`.
   - *Gate (`E34`):* Verify Arabic RTL mirroring, High-DPI scaling, keyboard focus, and UI Automation / screen-reader accessibility before locking the UI framework.
4. **Original Design System:** Create project-owned colors, typography, SVG icons (`Fluent Icons`/`Lucide`), and localized AR/EN command labels.
5. **Unified Command Registry (`ui.ribbon.command-registry`):** Bind every Ribbon button, menu item, context menu, and keyboard shortcut to one tested handler (`E28`); any unimplemented button stays explicitly disabled/unavailable (`E26`).
6. **Decouple Free OSS Compute & Render Engines:** Never embed proprietary runtime dependencies; use tested adapters from [`engine-integration-patterns.md`](engine-integration-patterns.md).
7. **Vertical Slice & Independent Verification (`T0–T4`):** Prove import -> view/edit -> export -> independent readback on target OS (`NOT_RUN` when Windows UIA/QGIS host absent).

---

## 3. Ten `ArcGIS Pro`-Inspired Workspace Sections Mapped to Free Engines (`E02`)

| Inspired UI Workspace Section | Original OSS Equivalent Components (Free-First) | Style / Format Fidelity Notes |
|---|---|---|
| **1. Project Backstage / Templates** | `.zearth` / `.qgz` project manager + ZIP backup recovery | Never clone `.aprx` internals silently |
| **2. Ribbon Tabs (Map, Analysis, Edit, Share)** | Original `Fluent.Ribbon` / `SARibbon` + unified command registry | Disable unsupported tabs cleanly (`E26`) |
| **3. Map Scene Canvas (`2D` / `3D` Linked)** | `MapLibre Native` / `OpenLayers` / `QgsMapCanvas` + `CesiumJS` | Sync Extent/CRS across 2D & 3D (`E14`) |
| **4. Contents / Layer TOC** | Hierarchical tree view + visibility/opacity/CRS metadata | Retain explicit layer CRS & Z provenance |
| **5. Catalog / Data Browser** | `STAC` + Local FS/GeoPackage/`PostGIS` tree browser | Safe read-only probing (`DatasetRef`) |
| **6. Geoprocessing Pane / Searchable Tools** | `GDAL`/`OGR`, `WhiteboxTools`, `GRASS`, `PyQGIS Processing` | Async worker + cancel + atomic temp writes (`E32`) |
| **7. Attribute Table & Selection** | Virtualized grid w/ UTF-8 Arabic search & bidirectional selection | Sync row IDs cleanly via `FeatureIdentity` |
| **8. Symbology & Label Inspector** | `MapLibre Style JSON`, `QGIS QML`, `SLD` | Document exact CIM/QML/MapLibre loss report (`REQ-EV2-054`) |
| **9. Print Layout & Map Series** | `QGIS Print Layout` (`A4–A0`), `WeasyPrint` / vector SVG->PDF | Include scalebar, north arrow, attribution |
| **10. Scripting Console & Task History** | Sandboxed `Python`/`CLI` runner + `.agent-development-log` ledger | Require explicit user consent for side effects |

*(For `Google Earth Pro` -> `CesiumJS` + `KML/KMZ` + `Esri Wayback` parity; `CityEngine` -> procedural JSON rules + `OCCT`/`Clipper2` + `CityJSON`; `Global Mapper`/`ENVI` -> `PDAL` + `GDAL`/`Rasterio` + `Orfeo`/`PySTAC`.)*
