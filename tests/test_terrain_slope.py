"""Deterministic offline tests for free ESRI ASCII Grid Horn slope example."""
import importlib.util
import json
import math
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "examples/terrain-slope/slope_ascii.py"
FIXTURE = ROOT / "examples/terrain-slope/fixtures/planar_slope.asc"
spec = importlib.util.spec_from_file_location("ascii_horn_slope", SRC)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TerrainSlopeTests(unittest.TestCase):
    def test_known_planar_rise_produces_45_degrees(self):
        head,x,y,a = mod.read_grid(FIXTURE)
        out=mod.horn_slope(a,head["nodata_value"],head["cellsize"])
        self.assertEqual(len(out),5)
        for r in range(5):
            for c in range(5):
                if r in (0,4) or c in (0,4):
                    self.assertEqual(out[r][c],mod.NODATA_OUTPUT)
                else:
                    self.assertAlmostEqual(out[r][c],45,places=10)

    def test_flat_grid_is_zero_not_nodata(self):
        grid=[[100.0]*5 for _ in range(5)]
        out=mod.horn_slope(grid,-9999,10)
        self.assertEqual(out[2][2],0.0)

    def test_nodata_propagates_only_to_kernel(self):
        grid=[[float(c) for c in range(5)] for _ in range(5)]
        grid[2][2]=-9999
        out=mod.horn_slope(grid,-9999,1)
        self.assertTrue(all(out[y][x]==mod.NODATA_OUTPUT for y in range(1,4) for x in range(1,4)))

    def test_feet_vertical_conversion(self):
        grid=[[float(c)*3.280839895 for c in range(5)] for _ in range(5)]
        out=mod.horn_slope(grid,-9999,1,horizontal_unit="m",vertical_unit="ft")
        self.assertAlmostEqual(out[2][2],45.0,places=6)

    def test_roundtrip_and_metadata_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            dst=Path(d)/"slope.asc"
            rc=mod.main(["--input",str(FIXTURE),"--output",str(dst),
                         "--horizontal-unit","m","--vertical-unit","m","--ack-projected"])
            self.assertEqual(rc,0)
            h,_,_,data=mod.read_grid(dst)
            self.assertAlmostEqual(data[2][2],45.0,places=6)
            self.assertEqual(h["nodata_value"],-9999)
            meta=json.loads((Path(d)/"slope.asc.provenance.json").read_text(encoding="utf-8"))
            self.assertEqual(meta["valid_slope_cells"],9)
            self.assertFalse(meta["crs_validated_by_tool"])
            with self.assertRaises(FileExistsError):
                mod.write_result(FIXTURE,dst,*mod.read_grid(FIXTURE)[:3],data,"m","m")

    def test_reject_malformed_or_unprojected(self):
        with tempfile.TemporaryDirectory() as d:
            bad=Path(d)/"bad.asc"
            bad.write_text("ncols 5\nnrows 5\nxllcorner 0\nyllcorner 0\ncellsize 1\nNODATA_value -9999\n5 4\n",encoding="utf-8")
            with self.assertRaises(ValueError):
                mod.read_grid(bad)
            with self.assertRaises(SystemExit):
                mod.main(["--input",str(FIXTURE),"--output",str(Path(d)/"slope.asc"),
                          "--horizontal-unit","m","--vertical-unit","m"])
