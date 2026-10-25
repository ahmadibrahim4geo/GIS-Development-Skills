# KML/KMZ open-source engineering references

Review candidates; inclusion here does not imply that all features were run or verified in this repository.

| Repository | Relevant capabilities | Cautions |
| --- | --- | --- |
| [google/libkml](https://github.com/google/libkml) | KML object model, serialization, KMZ, Google's historical implementation | Inspect maintenance state, platform builds and license before embedding |
| [OSGeo/gdal](https://github.com/OSGeo/gdal) | OGR KML and LIBKML drivers, feature conversion | Driver availability varies by build; not full Google Earth scene fidelity |
| [cleder/fastkml](https://github.com/cleder/fastkml) | Python KML read/write and object model | Validate extensions, styles and nested semantics per release |
| [tylere/pykml](https://github.com/tylere/pykml) | XML/KML authoring and validation | Review dependency support and maintenance |
| [CesiumGS/cesium](https://github.com/CesiumGS/cesium) | Browser-based KML visualization and 3D globe integration | Coverage of Google gx extensions and models must be tested |
| [mapbox/togeojson](https://github.com/mapbox/togeojson) | KML to GeoJSON feature conversion | GeoJSON cannot represent all KML scene/style/time semantics |
| [qgis/QGIS](https://github.com/qgis/QGIS) | Desktop layer loading, editing and interoperability | Compare imported layers with original document for style/folder losses |

## Research-to-implementation rules
1. Confirm license and current maintenance/release state from the upstream repository before vendoring or copying code.
2. Prefer a small adapter per runtime; never force a single library to promise universal compatibility.
3. Record feature-level support: Placemark, folders, ExtendedData, StyleMap, GroundOverlay, NetworkLink, altitude, time, gx:Track, gx:Tour and COLLADA.
4. Add synthetic test fixtures with expected output and a conversion-loss report.
5. Test ZIP bombs, traversal, XML entity attacks, network links, malformed XML and missing assets.
6. Verify Google Earth and GIS-host interoperability through actual round-trip tests, not by documentation alone.

See [KML/KMZ engineering skill](../skills/kml-kmz-engineering/SKILL.md).
