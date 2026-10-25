---
name: gis-cartography-symbology
description: Design, automate, apply and verify GIS symbols, vector renderers, raster color ramps, labels and accessible layouts in ArcMap, ArcGIS Pro, QGIS, MapLibre, Cesium and desktop GIS, with license-aware reusable style sources.
license: MIT
---

# GIS Cartography, Symbology & Styling

**Free-first default:** Follow [no-cost GIS and upstream licensing policy](../../references/free-first-policy.md); proprietary ArcGIS hosts are optional, while individual styles/fonts retain their own rights.

Use for point, line, polygon, raster, labels, legends, scientific color maps, map layouts and reusable cartographic style libraries. Load only this skill and the target host's specialist; do not load every GIS skill.

## Read first
- [Curated, license-aware catalog](../../references/cartographic-style-sources.json) and [selection guide](../../references/cartographic-style-guide.md).
- [Own ArcMap Style Collection](https://github.com/ahmadibrahim4geo/ArcMap-Style-Collection) is the primary external discovery source. It contains third-party assets with *independent* licenses. Reference assets by URL and exact path, not by copying or automatically installing.
- [Cartography example](../../examples/cartography/README.md) is a testable MapLibre vector fixture, **not** proof of ArcGIS/QGIS renderer parity.
- [Map marker/icon library (8 sources + Cesium PinBuilder)](../../references/map-marker-icon-library.md) lists SVG, PNG and icon fonts, exact code-vs-asset licenses and KML/KMZ compatibility; [preservation-first KML/KMZ contract](../../references/kml-kmz-symbol-preservation.md) is mandatory for imported content.

## Action contract
1. Inspect actual geometry (Point/MultiPoint, LineString/MultiLineString, Polygon/MultiPolygon, raster bands/pixel type), coordinate system, scale, field semantics, nulls and category/numeric distribution; verify raster NoData, statistics and band definitions. Distinguish geographic units from graphic symbol units.
2. Ask for, or infer from known evidence, purpose, target map type, expected audience, background/basemap, print vs screen, software + version, language and accessibility requirements. Never mistake category labels for a continuous numerical scale.
3. Choose renderer **before** choosing a palette:
   - qualitative categories -> unique values and distinct colors/patterns;
   - ordered numeric -> sequential scale;
   - departures around meaningful neutral -> diverging with explicitly defined center;
   - exact thresholds -> classified renderer with documented cutoffs;
   - magnitude on points -> sizes or proportional symbols (check area vs radius);
   - concentration -> heatmap only with meaningful aggregation/kernel and units.
4. Design **Point** symbols: shape/SVG/marker/font, fill/stroke, size, rotation, anchor, opacity, labels, clustering only when appropriate. For **Line**: width, color, dashes, casing, arrows/flow direction, pattern and scale-aware behavior. For **Polygon**: fill, outline, hatches, pattern, transparency, multipart/hole handling. For **Raster**: single-band grayscale, stretch, min/max, percentile, classified/pseudocolor, RGB composites, scientifically suitable ramps, hillshade and NoData/alpha treatment.
5. Use compatible formats per host: ArcMap legacy `.style` and `.lyr` + `arcpy.mapping` where supported; ArcGIS Pro `.stylx`, `.lyrx`, `arcpy.mp`/CIM (version-pinned); QGIS XML/QML/QGZ + PyQGIS renderers; MapLibre Style Spec paint/layout expressions; Cesium entity/material primitives (not drop-in MapLibre styles). Do not silently equate these file formats.
6. Generate a **preview** with a legend, representative features, min/max, null/NoData, RGB and alpha channels; check collision/overlap, hierarchy, grayscales/CVD accessibility, Arabic/English text shaping, projected vs geographic display, low/high zoom and export scale.
7. Apply on a copy or reversible in-memory layer where feasible. Save explicitly in host-native format; reload and compare renderer type, fields, stops, colors, opacity, labels and artwork references. Do not modify source geometry, raster pixel values or overwrite project files without user approval.
8. Capture evidence: source license, name/version, target GIS runtime, renderer, attribute/classification method, color stops, symbology JSON/native layer file, screenshot/export if available, readback and failures. Test in the actual licensed target before claiming native success.

## Icon and KMZ-specific branch — preserve before styling

1. For **new points**, browse [source catalog](../../references/cartographic-style-sources.json) by `kind=map-marker-icon-library`, intended platform, selected icon's source, version, license, and required attribution. Prefer CC0 Pinhead, Maki and Temaki when appropriate; also include Map Icons Collection, Map Icons (mixed rights), Material Symbols, Leaflet ExtraMarkers/AwesomeMarkers and Cesium PinBuilder as *distinct* renderer/library options.
2. For *new* KML/KMZ placemarks, render a licensed SVG or canvas pin to a transparent PNG for broad KML viewer compatibility; include it as a safe local file and `IconStyle/Icon/href` relative reference. Keep `scale`, `hotSpot`, heading, alpha and label properties intentional. Record any mandatory credits. Do not promise native KML support for SVG, Leaflet icon fonts or CSS.
3. **Existing imported KML/KMZ is exempt from all palette/marker defaults.** Its embedded point/line/polygon symbols, `StyleMap` normal/highlight, `styleUrl`, `IconStyle`, `LabelStyle`, `LineStyle`, `PolyStyle`, colors and packed image bytes have precedence. Never run a restyling pass during import, save or opening a project. Read [mandatory fidelity guide](../../references/kml-kmz-symbol-preservation.md) and [KMZ Engineering](../kml-kmz-engineering/SKILL.md).
4. Fallback if an imported icon fails to display is **temporary visual-only**: preserve source href/bytes and warn; never export a temporary blue-pin fallback as if it were the original. Replacing an imported style needs explicit user action with Reset to original and preferably Save As. The source document and user-authored edits must be stored separately.
5. Validate imported file → rendered scene → exported copy → re-import **without any style drift**. Use the [offline style/resource checker](../../examples/kml-style-preservation/README.md) for narrow structural regression and native engine screenshots separately. If renderer cannot reproduce something, report it rather than silently substituting a preset.

## Source and permission policy
- **Free-first:** prefer independently licensed QGIS, MapLibre, OS GeoDataViz, CARTOColor and scientific palettes where use terms permit; rank cost and host dependency distinctly.
- Repository MIT licenses do **not** automatically relicense included Esri/USGS/BGS files, fonts or converted styles; verify per-file rights, attribution and embedding/redistribution rules before shipping.
- Do not download/run untrusted bundled scripts, font installers, SVG scripts or external QML expressions automatically. Sanitize URLs and validate imports.

## Cross-skill routing
- ArcGIS Pro / ArcMap -> [ArcGIS Toolbox Engineering](../arcgis-toolbox-engineering/SKILL.md); QGIS -> [QGIS Plugin Development](../qgis-plugin-development/SKILL.md).
- 2D/3D web -> [Geospatial Web Mapping](../geospatial-web-mapping/SKILL.md); independent GIS UI -> [Desktop GIS](../gis-desktop-application-development/SKILL.md).
- Spatial processing / raster stats -> [Geospatial Data Processing](../geospatial-data-processing/SKILL.md); CRS -> [Coordinate Reference Systems](../coordinate-reference-systems/SKILL.md).
- Sun position, time/location, device environment -> [Device Context](../gis-device-context/SKILL.md).

## Acceptance
- [ ] Correct variable semantics and renderer choice, legend/units/NoData, CVD check
- [ ] Tested native format and target version; original geometry/pixels unchanged
- [ ] External assets' exact license/attribution verified; fallback available if not
- [ ] Preview, apply, save/reopen and real appearance verified (or limitations explicitly recorded)
- [ ] Imported KML/KMZ original symbology/assets remain unchanged unless user explicitly opts to restyle
