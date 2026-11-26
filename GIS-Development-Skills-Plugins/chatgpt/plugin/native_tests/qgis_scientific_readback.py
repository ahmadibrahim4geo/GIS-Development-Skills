#!/usr/bin/env python3
"""Write and re-open small raster fixtures in QGIS/GDAL; read trusted test geometry."""

import argparse
import json
from pathlib import Path
import struct

from osgeo import gdal, osr
from qgis.core import QgsApplication, QgsRasterLayer, QgsVectorLayer


NODATA = -9999


def write_grid(path, epsg, affine):
    if path.exists():
        raise FileExistsError(path)
    dataset = gdal.GetDriverByName("GTiff").Create(str(path), 2, 2, 1, gdal.GDT_Int16)
    reference = osr.SpatialReference()
    reference.ImportFromEPSG(epsg)
    dataset.SetSpatialRef(reference)
    dataset.SetGeoTransform(affine)
    band = dataset.GetRasterBand(1)
    band.SetNoDataValue(NODATA)
    band.WriteRaster(0, 0, 2, 2, struct.pack("=4h", 10, NODATA, 30, 40), buf_type=gdal.GDT_Int16)
    band = None
    dataset = None


def grid_signature(path):
    dataset = gdal.Open(str(path), gdal.GA_ReadOnly)
    reference = dataset.GetSpatialRef()
    return (reference.GetAuthorityCode(None), dataset.GetGeoTransform(),
            dataset.RasterXSize, dataset.RasterYSize)


def require_matching_grid(left, right):
    if left[0] != right[0]:
        raise ValueError("CRS_MISMATCH")
    if left[1:] != right[1:]:
        raise ValueError("GRID_MISMATCH")


def mismatch(left, right):
    try:
        require_matching_grid(left, right)
    except ValueError as error:
        return str(error)
    return "ACCEPTED"


def raster_observation(outputs):
    geographic = outputs / "wgs84.tif"
    shifted = outputs / "shifted.tif"
    projected = outputs / "projected.tif"
    affine = (0, 1, 0, 2, 0, -1)
    write_grid(geographic, 4326, affine)
    write_grid(shifted, 4326, (0.5, 1, 0, 2, 0, -1))
    write_grid(projected, 3857, affine)
    reference = grid_signature(geographic)
    layer = QgsRasterLayer(str(geographic), "verification", "gdal")
    if not layer.isValid():
        raise RuntimeError("PyQGIS raster readback failed")
    provider = layer.dataProvider()
    block = provider.block(1, layer.extent(), 2, 2)
    if not block.isValid():
        raise RuntimeError("PyQGIS could not read the raster block")
    values = [[None if block.isNoData(row, column) else int(block.value(row, column))
               for column in range(2)] for row in range(2)]
    return {"crs": layer.crs().authid(), "shape": [layer.height(), layer.width()],
            "nodata": int(provider.sourceNoDataValue(1)), "values": values,
            "same_grid": mismatch(reference, grid_signature(geographic)),
            "different_crs": mismatch(reference, grid_signature(projected)),
            "shifted_grid": mismatch(reference, grid_signature(shifted))}


def polygon_observation(source):
    original = QgsVectorLayer(str(source), "verification", "ogr")
    if not original.isValid():
        raise RuntimeError("Fixture polygons could not be opened")
    geometries = [feature.geometry().isGeosValid() for feature in original.getFeatures()]
    return {"crs": original.crs().authid(), "valid": geometries.count(True),
            "invalid": geometries.count(False)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--polygons", type=Path, required=True)
    parser.add_argument("--outputs", type=Path, required=True)
    args = parser.parse_args()
    report = args.outputs / "qgis-science.json"
    if report.exists():
        raise FileExistsError(report)
    gdal.UseExceptions()
    app = QgsApplication([], False)
    app.initQgis()
    try:
        result = {"raster": raster_observation(args.outputs),
                  "polygons": polygon_observation(args.polygons)}
        with report.open("x", encoding="utf-8") as handle:
            json.dump(result, handle, indent=2)
        print(json.dumps(result))
    finally:
        app.exitQgis()


if __name__ == "__main__":
    main()
