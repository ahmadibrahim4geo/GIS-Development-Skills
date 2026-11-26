# Native GIS Acceptance — Run Only In Installed GIS Environments

The generic GitHub Actions Python job **cannot run ArcGIS Pro/ArcMap/QGIS/PostGIS**. These smoke/acceptance scripts are deliberately excluded from generic CI. They test real output creation and re-reading in a temporary directory but do not guarantee universal deployment compatibility.

## ArcGIS Pro (installed arcpy)
From its activated Python prompt:
```powershell
python native_tests/arcgis_pro_acceptance.py
```
Creates a *temporary* file geodatabase and two WGS84 point features, copies the
output, and independently reads the exact coordinates, feature count and
EPSG:4326. A passing run supports this ArcPy vector I/O case in the named host.

## QGIS (installed PyQGIS)
Launch from the installed QGIS Python environment configured with its required Qt and prefix paths:
```bash
python native_tests/qgis_acceptance.py
```
Creates two synthetic points in memory, writes a temporary GeoPackage, then opens it back to validate count, fields and EPSG:4326. This supports T3 for this limited operation only if it actually runs.

For scientific raster and topology readback, pass an isolated copy of
fixtures/geojson/valid_invalid_polygons.geojson and an existing empty
test-run outputs directory:

    python native_tests/qgis_scientific_readback.py --polygons PATH --outputs PATH

The harness uses the installed GDAL and PyQGIS to write and reopen three small
GeoTIFFs. It records NoData, values, raster dimensions, CRS and grid-mismatch
checks and inspects the two synthetic polygon geometries. Compare the
qgis-science.json artifact with the [committed expected values](../fixtures/expected/p03-science.json).

## PostGIS
[PostGIS SQL example](../examples/spatial-sql/postgis_network_index.sql) is intentionally review-only; connect to an authorized sandbox, record actual schema/index/query plans and logs, then fill the [GIS Acceptance Report](../templates/GIS_ACCEPTANCE_REPORT.md).

**ArcMap** requires its own legacy Python 2.7 host and cannot execute these Python 3 tests unchanged. QGIS and ArcGIS Pro scripts are not invoked from generic CI; no native pass is claimed until actual environment logs are provided.

## Windows WPF toolchain acceptance

Provide the installed Windows .NET SDK executable, a new scratch directory,
and the raster receipt produced by qgis_scientific_readback.py:

    python native_tests/run_wpf_toolchain.py --dotnet "C:/Program Files/dotnet/dotnet.exe" --work "C:/scratch/wpf-check" --raster-readback "C:/scratch/qgis-science.json"

The harness instantiates an installed WPF template, restores against an empty
NuGet source list, and builds with that restore. The app creates a native
window, invokes a WPF button through its in-process AutomationPeer and returns
the shape, CRS and NoData-aware cell count read from the copied input. The
harness validates that receipt and the input hash. The scope is WPF build,
launch and in-process UI invocation. Add `--external-uia` to build a separate
Windows UI Automation client. It targets the process it starts and invokes the
`ReadRaster` button by AutomationId. The harness saves the client receipt and
the independent app receipt. The run uses an existing interactive Windows session.

[Installed .NET templates](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-new-sdk-templates) · [NuGet restore settings](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-restore) · [WPF automation peers](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/controls/ui-automation-of-a-wpf-custom-control)

## QGIS project persistence and browser point readback

In an empty isolated run directory generate the raster using the scientific
test above. Generate `roundtrip.gpkg` using the
[standalone QGIS example](../examples/qgis-engine/README.md). Run these commands
in the QGIS Python environment. The second process reopens the saved project
and independently verifies the exported longitude/latitude GeoJSON.

```powershell
python native_tests/qgis_project_roundtrip.py create --directory PATH
python native_tests/qgis_project_roundtrip.py reopen --directory PATH
```

Then run `native_tests/web_geojson_readback.py` with `--browser` pointing to
an installed Chromium binary, `--geojson PATH/qgis-web.geojson` and `--work`
pointing to a fresh directory. It uses an isolated browser profile and validates
the rendered point positions and layer visibility controls using DOM readback.
The browser fixture covers an offline planar point display. Native WebView2,
third-party basemap services and 3D scenes need their own acceptance tests.

## Playbooks for the remaining trial cases

| Path | Reproduce locally | Observe |
| --- | --- | --- |
| Sensor compatibility | `python -m unittest tests.test_remote_sensing_indices` | The declared Landsat collection drives scaling, QA band and mask. A scene from another product requires its own metadata and expected pixels. |
| Project migration | Copy the [coordinate-audit example](../examples/golden-qgis-coordinate-audit/README.md) into a scratch project and preview with `project_governance.py plan-move`. Run the native Processing example before and after authorized changes. | Compare the feature and coordinate summary outputs and restore the scratch copy to confirm rollback. |
| External skill review | `python -m unittest tests.test_skill_intake` and follow the [quarantine review procedure](../references/project-governance-workflow.md). | Read the expected manual-review and isolated-rejection receipts. Candidate activation and external scanners have separate permissions and evidence. |
