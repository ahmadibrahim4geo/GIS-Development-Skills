# GIS Project Wizard — implementation plan

## Scope and architecture
- Bilingual Arabic/English guided project selection with accessible keyboard-operable controls.
- Paths: Desktop GIS, ArcGIS Pro toolbox, ArcMap toolbox, dual-host toolbox, QGIS plugin, Web GIS, Remote Sensing, Spatial Database and GeoAI.
- Select free/open-source first; disclose ArcGIS and third-party service licensing. Never promise that a proprietary host is free.
- Generate an editable Markdown plan and AI-agent instructions, with explicit skill paths, risks, implementation phases and acceptance checks.
- Recommend a compatible stack, not a universal stack. For dual ArcGIS hosts, keep a Python-2.7-compatible core where feasible and isolate Python 3/ArcGIS Pro adapters; verify real host APIs.
- Include a mandatory reliability plan: input sizes, memory budget, CPU and I/O measurements, cancellation, progress, logging, crash recovery, corrupt files, stress and regression testing.
- Include KML/KMZ whenever file interchange is selected. Clearly separate feature conversion from document-fidelity rendering.

## Delivery gates
1. Static UI and bilingual workflow, no server required.
2. Reference-driven recommendations and machine-readable manifest.
3. Real-world fixture suite: valid and malformed KML/KMZ, huge inputs, nested folders, altitude, overlays and extensions.
4. Unit tests and CI for validation; report exact test coverage and limitations.
5. Native host acceptance in ArcGIS Pro, ArcMap, QGIS, Cesium and desktop shells only when environments are available.
6. Browser accessibility and responsive/mobile smoke tests before release.

## Acceptance criteria
- A user can complete the wizard offline and export a meaningful plan.
- All suggested paths resolve to existing files or are explicitly marked planned.
- English and Arabic have equivalent meaning, without mixed UI labels.
- No performance or compatibility claim without measured evidence.
- KMZ processing never extracts untrusted archive members without path/size checks.

## Implementation status
- This document is a roadmap, not proof of implementation.
- Static wizard and linked engineering references are the first implementation increment.
- Native GIS runtime and load/stress acceptance remain outstanding.
