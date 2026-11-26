#!/usr/bin/env python3
"""Save/reopen a QGIS project and export a local web fixture with independent readback."""
import argparse
import json
from pathlib import Path

from qgis.core import (Qgis, QgsApplication, QgsCoordinateReferenceSystem, QgsMarkerSymbol,
                       QgsProject, QgsRasterLayer, QgsVectorFileWriter, QgsVectorLayer)


def create(project, directory):
    output = directory / "readback.qgs"
    if output.exists():
        raise FileExistsError(output)
    points = QgsVectorLayer(str(directory / "roundtrip.gpkg"), "Control points", "ogr")
    raster = QgsRasterLayer(str(directory / "wgs84.tif"), "Grid")
    if not points.isValid() or not raster.isValid():
        raise RuntimeError("Generate the QGIS vector and raster fixtures first.")
    points.renderer().setSymbol(QgsMarkerSymbol.createSimple({"name": "square", "color": "#167b72"}))
    project.setCrs(QgsCoordinateReferenceSystem("EPSG:3857"))
    project.setFilePathStorage(Qgis.FilePathType.Relative)
    project.addMapLayers([raster, points])
    project.layerTreeRoot().findLayer(raster.id()).setItemVisibilityChecked(False)
    project.viewSettings().setDefaultViewExtent(project.viewSettings().fullExtent())
    if not project.write(str(output)):
        raise RuntimeError("QGIS project save failed.")


def reopen(project, directory):
    export = directory / "qgis-web.geojson"
    if export.exists():
        raise FileExistsError(export)
    if not project.read(str(directory / "readback.qgs")):
        raise RuntimeError("QGIS could not reopen the saved project.")
    points, = project.mapLayersByName("Control points")
    raster, = project.mapLayersByName("Grid")
    provider = raster.dataProvider()
    block = provider.block(1, raster.extent(), 2, 2)
    observed = {
        "project_crs": project.crs().authid(),
        "extent_restored": not project.viewSettings().defaultViewExtent().isEmpty(),
        "relative_paths": project.filePathStorage() == Qgis.FilePathType.Relative,
        "vector_crs": points.crs().authid(),
        "features": points.featureCount(),
        "marker_color": points.renderer().symbol().color().name(),
        "grid_crs": raster.crs().authid(),
        "grid_nodata": int(provider.sourceNoDataValue(1)),
        "missing_cells": sum(block.isNoData(row, col) for row in range(2) for col in range(2)),
        "grid_hidden": not project.layerTreeRoot().findLayer(raster.id()).itemVisibilityChecked(),
    }
    expected = {
        "project_crs": "EPSG:3857", "extent_restored": True, "relative_paths": True,
        "vector_crs": "EPSG:4326", "features": 2, "marker_color": "#167b72",
        "grid_crs": "EPSG:4326", "grid_nodata": -9999, "missing_cells": 1, "grid_hidden": True,
    }
    if observed != expected:
        raise RuntimeError(f"QGIS project readback mismatch: {observed}")
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GeoJSON"
    options.layerOptions = ["RFC7946=YES"]
    code, *_ = QgsVectorFileWriter.writeAsVectorFormatV3(points, str(export), project.transformContext(), options)
    if code != QgsVectorFileWriter.NoError:
        raise RuntimeError(f"GeoJSON export failed: {code}")
    document = json.loads(export.read_text(encoding="utf-8"))
    expected_points = {"Cairo": [31.2357, 30.0444], "Alexandria": [29.9187, 31.2001]}
    coordinates = {
        item["properties"]["place"]: item["geometry"]["coordinates"]
        for item in document["features"]
    }
    if document["type"] != "FeatureCollection" or coordinates != expected_points:
        raise RuntimeError("GeoJSON geographic coordinates failed independent JSON readback.")
    print(json.dumps({"status": "PASS", "host": Qgis.QGIS_VERSION, "project_readback": observed,
                      "export": export.name, "geojson_points": coordinates}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("create", "reopen"))
    parser.add_argument("--directory", type=Path, required=True)
    args = parser.parse_args()
    directory = args.directory.resolve(strict=True)
    app = QgsApplication([], False)
    app.initQgis()
    project = QgsProject.instance()
    try:
        if args.action == "create":
            create(project, directory)
        else:
            reopen(project, directory)
    finally:
        project.clear()
        app.exitQgis()


if __name__ == "__main__":
    main()
