---
name: qgis-plugin-development
description: Design, implement, audit and package functional QGIS plugins and Processing algorithms with version-aware PyQGIS/Qt compatibility, dock panels, STAC integrations and end-to-end UI acceptance tests.
license: MIT
---

# QGIS Plugin Development

Choose this when building QGIS Processing providers or installable interface plugins.

## Procedure

1. Determine exact QGIS version (3.x versus 4.x), OS, Qt and Python interpreter. Do not assume ArcGIS-style ArcPy APIs.
2. Read `../../references/qgis.md` and `../../references/gishub-software.md`. Study https://github.com/opengeos/qgis-plugin-template for professional plugin structure.
3. Write behavior contracts for toolbar action, dialog/dock, layer I/O, settings, cancellation, reporting and user-visible errors.
4. Separate geoprocessing/CRS logic from PyQt interface. Add a testable Processing algorithm where appropriate.
5. For imagery use STAC or data-provider libraries only after verifying licensing, endpoints, date filters and authentication.
6. Package with valid `metadata.txt`, entry point and dependencies; test install/uninstall, QGIS version, UI clicks, output layer and project reload.
7. Audit secrets/auto-update mechanisms. Don't silently install dependencies or execute external scripts without consent.
8. Report static tests separately from testing inside a real QGIS installation.

## Checks

- [ ] Qt5/Qt6 and PyQGIS API compatibility tested for each claimed release
- [ ] CRS/axis order and correct area/distance units
- [ ] Undo/cancellation and handling of invalid geometries
- [ ] Functional toolbar, parameters, output layers and metadata
- [ ] No paid/authenticated data endpoints passed off as unlimited free
- [ ] No placeholder commands presented as implemented

## Related official sources

- https://github.com/qgis/QGIS
- https://github.com/opengeos/qgis-plugin-template
- https://github.com/opengeos/qgis-stac-plugin
- https://github.com/opengeos/qgis-nasa-opera-plugin
