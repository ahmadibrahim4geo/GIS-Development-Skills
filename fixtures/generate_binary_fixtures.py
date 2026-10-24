#!/usr/bin/env python3
"""Create tiny synthetic Shapefile, multi-layer GPKG and two mismatched GeoTIFFs.

Requires user-provided tested Fiona, Rasterio and NumPy environment. Does not
download data. Creates outputs in a NEW caller-supplied directory.
"""
import argparse
from pathlib import Path


def generate(out):
    import fiona
    import numpy as np
    import rasterio
    from rasterio.transform import from_origin
    if out.exists() and any(out.iterdir()):
        raise FileExistsError("Output directory exists and is not empty; choose a fresh directory")
    out.mkdir(parents=True, exist_ok=True)
    shape_dir = out / "shapefile"
    shape_dir.mkdir()
    schema = {"geometry": "Point", "properties": {"very_long_identifier": "str:30", "VALUE_M": "float:12.2"}}
    with fiona.open(str(shape_dir / "attribute_limits.shp"), "w", driver="ESRI Shapefile",
                    crs="EPSG:4326", schema=schema, encoding="UTF-8") as dst:
        dst.write({"geometry": {"type": "Point", "coordinates": [31, 30]},
                   "properties": {"very_long_identifier": "synthetic", "VALUE_M": 25.5}})
    geopackage = out / "multilayer.gpkg"
    for layer, geometry, coords in [
        ("points", "Point", (31, 30)),
        ("lines", "LineString", [(31, 30), (31.1, 30.1)])
    ]:
        schema = {"geometry": geometry, "properties": {"label": "str:24"}}
        with fiona.open(str(geopackage), "w", driver="GPKG", layer=layer,
                        crs="EPSG:4326", schema=schema) as dst:
            dst.write({"geometry": {"type": geometry, "coordinates": coords},
                       "properties": {"label": layer}})
    values = np.array([[10, -9999], [30, 40]], dtype=np.int16)
    for filename, crs, resolution, left, top in [
        ("nodata_4326.tif", "EPSG:4326", 0.01, 30.0, 31.0),
        ("misaligned_3857.tif", "EPSG:3857", 100, 3330000, 3620000),
    ]:
        with rasterio.open(out / filename, "w", driver="GTiff", width=2, height=2,
                           count=1, dtype="int16", crs=crs, nodata=-9999,
                           transform=from_origin(left, top, resolution, resolution),
                           compress="deflate") as dst:
            dst.write(values, 1)
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    generate(args.output)
    print("Generated synthetic Shapefile, GPKG and GeoTIFF fixtures in " + str(args.output))


if __name__ == "__main__":
    main()
