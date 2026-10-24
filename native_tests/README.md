# Native GIS Acceptance — Run Only In Installed GIS Environments

The generic GitHub Actions Python job **cannot run ArcGIS Pro/ArcMap/QGIS/PostGIS**. These smoke/acceptance scripts are deliberately excluded from generic CI. They test real output creation and re-reading in a temporary directory but do not guarantee universal deployment compatibility.

## ArcGIS Pro (installed arcpy)
From its activated Python prompt:
```powershell
python native_tests/arcgis_pro_acceptance.py
```
Creates a *temporary* file geodatabase and two WGS84 point features, copies outputs, re-reads/counts them, then removes its own temp directory. This is only a minimal real ArcPy vector I/O T3 assertion if the command **actually passes inside licensed ArcGIS Pro**, not a full project acceptance.

## QGIS (installed PyQGIS)
Launch from the installed QGIS Python environment configured with its required Qt and prefix paths:
```bash
python native_tests/qgis_acceptance.py
```
Creates two synthetic points in memory, writes a temporary GeoPackage, then opens it back to validate count, fields and EPSG:4326. This supports T3 for this limited operation only if it actually runs.

## PostGIS
[PostGIS SQL example](../examples/spatial-sql/postgis_network_index.sql) is intentionally review-only; connect to an authorized sandbox, record actual schema/index/query plans and logs, then fill the [GIS Acceptance Report](../templates/GIS_ACCEPTANCE_REPORT.md).

**ArcMap** requires its own legacy Python 2.7 host and cannot execute these Python 3 tests unchanged. QGIS and ArcGIS Pro scripts are not invoked from generic CI; no native pass is claimed until actual environment logs are provided.
