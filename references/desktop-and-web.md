# Standalone GIS, mapping and globe applications

A GIS application needs more than a map view: data loading, CRS handling, layer state, style, selection, query, analysis, export, error recovery, tests, packaging and licensing.

## Stack options

| Need | Relevant project | Important boundary |
|---|---|---|
| Cross-platform desktop shell with Rust backend | Tauri + Rust Geo ecosystem, using GeoLibre as reference | Rendering, backend analysis and offline files are separate layers |
| Full-featured existing GIS core | QGIS / PyQGIS | QGIS bindings and redistribution carry license/deployment obligations |
| 2D browser map canvas | MapLibre GL JS | Requires verified style/tiles provider or offline data |
| 3D global viewer | CesiumJS | Imagery/terrain service may have separate terms/keys |
| Browser/desktop multi-engine inspiration | GeoLibre | Do not claim feature parity without testing the referenced release |

Official sources: https://github.com/opengeos/GeoLibre ; https://github.com/maplibre/maplibre-gl-js ; https://github.com/CesiumGS/cesium

## Workflow for a desktop app

1. Document explicit functional acceptance criteria: open GeoPackage/GeoTIFF/Shapefile/KML; CRS; lat/lon status; zoom/pan/rotate; project save/open; large layers.
2. Separate **renderer** from **data services**, **analysis engine**, **UI command bus**, and **project persistence**.
3. For each ribbon command, name handler, input data, output change, observable success, failure behavior and test case.
4. Verify real basemap terms and offline access (availability and caching are provider-specific). No automatically assumed access to proprietary satellite imagery.
5. Instrument file imports and timing; never show dead commands that simply log or display a placeholder success message.
6. Test export, project roundtrips, coordinate display, layer order, cache cleanup and recovery from corrupt project files.

## Provider caveat

A rendering SDK's open-source license does **not** make its imagery, style, tile server, terrain tiles or geocoding endpoint free or redistributable. Verify each upstream service independently.

## Windows .NET GIS and the EarthMapper examples

Read [`dotnet-gis.md`](dotnet-gis.md) and [`earthmapper-case-studies.md`](earthmapper-case-studies.md). **AliAlkazraji/EarthMapper** is a README-only Windows GIS product overview, not a reusable code repository in the inspected state. **HIT-SIRS/EarthMapper** is separate satellite/map generation research.

## GeoLibre R / RustGIS and real API service requirements

Read [`rustgis-and-geolibre-r.md`](rustgis-and-geolibre-r.md) for inspectable RustGIS and R GeoLibre integration examples. For climate data, DEM, imagery, tiles and geocoding use [`free-geospatial-apis.md`](free-geospatial-apis.md). Never assume a free/open renderer guarantees rights to a hosted map tile or imagery service.