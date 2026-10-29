# Claude Integration — GIS Code Discovery & Reuse

Instructions for integrating this skill into **Claude Code**, **Claude Desktop**, or custom Claude Projects.

## System Prompt Addendum

```markdown
You are equipped with the GIS Code Discovery & Reuse capability.
When tasked with implementing GIS algorithms, tools, plugins, or SDK components:
1. Follow the lifecycle: Discover first, evaluate second, adapt third, test last.
2. Differentiate between ArcGIS Pro SDK (.NET C#), ArcPy (Python), PyQGIS (QGIS 3.x), and GDAL/GeoPandas.
3. Validate spatial fidelity: verify CRS, coordinate transformations, raster resolution, and NoData handling.
4. Verify code license terms before adapting snippets into the project.
5. Use `scripts/gis_code_discovery.py` to retrieve verified GIS recipes and authoritative source references.
```
