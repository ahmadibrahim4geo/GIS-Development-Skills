# ArcGIS Pro tool development

Official reference: https://pro.arcgis.com/en/pro-app/latest/arcpy/geoprocessing_and_python/defining-a-tool-in-a-python-toolbox.htm

- Target **Python 3 supplied with the exact ArcGIS Pro release**, unless the user provides a validated clone environment. Do not install random GDAL/PyQt wheels into the managed ArcGIS Pro environment without checking binary compatibility.
- Python toolboxes use `Toolbox`, tool classes, `getParameterInfo`, `updateParameters`, `updateMessages` and `execute`; keep top-level code side-effect-free. See the official `.pyt` creator docs at https://pro.arcgis.com/en/pro-app/3.6/arcpy/geoprocessing_and_python/creating-a-new-python-toolbox.htm .
- `arcpy.Parameter` definitions must match expected path/datatype, direction, required/optional type, supported output types and filters.
- Validate parameter `altered` / `hasBeenValidated` behavior when implementing dynamic menus.
- Respect geoprocessing `arcpy.env` and license requirements, messages, cancellation patterns and workspace locks.
- Use `arcpy.mp` for ArcGIS Pro map and layout automation; never mechanically rename an `arcpy.mapping` operation.
- Unit/integration test outside ArcGIS Pro where possible, then run the actual `.pyt` in ArcGIS Pro before reporting it works.

**Safe starter:** `templates/arcgis-pro-toolbox.pyt` copies feature geometries/attributes to a new destination without mutating the source.

**Official resources:** https://github.com/Esri/arcpy ; https://github.com/Esri/arcgis-python-api