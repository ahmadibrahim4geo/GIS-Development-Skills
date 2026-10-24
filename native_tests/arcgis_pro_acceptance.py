#!/usr/bin/env python3
"""Native ArcGIS Pro I/O smoke test. Run ONLY with installed ArcGIS Pro arcpy."""
import tempfile
from pathlib import Path


def run():
    import arcpy
    with tempfile.TemporaryDirectory(prefix="gis_agent_pro_") as directory:
        root = Path(directory)
        gdb = str(root / "audit.gdb")
        arcpy.management.CreateFileGDB(str(root), "audit.gdb")
        sr = arcpy.SpatialReference(4326)
        arcpy.management.CreateFeatureclass(gdb, "points", "POINT", spatial_reference=sr)
        source = str(root / "audit.gdb" / "points")
        with arcpy.da.InsertCursor(source, ["SHAPE@XY"]) as cursor:
            cursor.insertRow([(31, 30)])
            cursor.insertRow([(31.1, 30.1)])
        out = str(root / "audit.gdb" / "copied")
        arcpy.management.CopyFeatures(source, out)
        result = int(arcpy.management.GetCount(out).getOutput(0))
        if result != 2:
            raise AssertionError("Expected two copied points, got {}".format(result))
        with arcpy.da.SearchCursor(out, ["SHAPE@XY"]) as cursor:
            coords = list(cursor)
        if len(coords) != 2:
            raise AssertionError("Copied output readback failed")
        print("Native ArcGIS Pro temporary GDB readback PASS; count=2")
        # Temp gdb belongs to this test and may be cleaned after ArcPy exits.


if __name__ == "__main__":
    run()
