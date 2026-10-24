"""Offline acceptance tests for the Esri factory-table inspector."""
import contextlib
import csv
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("crs_catalog", ROOT / "scripts" / "crs_catalog.py")
crs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(crs)


class CoordinateReferenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        cols = ["wkid", "latestWkid", "name", "authority", "description",
                "areaname", "slat", "nlat", "llon", "rlon", "deprecated", "wkt2"]
        with (self.root / "pe_list_projcs.csv").open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=cols)
            writer.writeheader()
            writer.writerow(dict(wkid=102100, latestWkid=3857, name="WGS_1984_Web_Mercator_Auxiliary_Sphere",
                                 authority="EPSG", description="Web Mercator", areaname="World", slat=-85,
                                 nlat=85, llon=-180, rlon=180, deprecated="no", wkt2="PROJCRS[...]"))
            writer.writerow(dict(wkid=32636, latestWkid=32636, name="WGS_1984_UTM_Zone_36N",
                                 authority="EPSG", description="UTM", areaname="Egypt", slat=0,
                                 nlat=84, llon=30, rlon=36, deprecated="no", wkt2="PROJCRS[...]"))
        (self.root / "pe_list_geogcs.json").write_text(
            json.dumps({"GeographicCoordinateSystems": [
                dict(wkid=4326, latestWkid=4326, name="GCS_WGS_1984", authority="EPSG",
                     areaname="World", slat=-90, nlat=90, llon=-180, rlon=180)
            ]}), encoding="utf-8")

    def test_read_two_formats_and_actual_object_families(self):
        records = crs.read_catalog(self.root)
        self.assertEqual(3, len(records))
        self.assertEqual({"geogcs", "projcs"}, {r["object_type"] for r in records})

    def test_alias_retained_not_silently_rewritten(self):
        row = next(crs.filter_rows(crs.read_catalog(self.root), query="102100"))
        self.assertEqual("102100", row["wkid"])
        self.assertEqual("3857", row["latestWkid"])

    def test_search_area_and_geographic_extent(self):
        rows = list(crs.filter_rows(crs.read_catalog(self.root), kind="projcs",
                                    query="Egypt", bbox=[32, 24, 35, 30]))
        self.assertEqual(["32636"], [str(x["wkid"]) for x in rows])
        self.assertEqual([], list(crs.filter_rows(crs.read_catalog(self.root),
                       kind="projcs", query="Egypt", bbox=[-100, 20, -80, 30])))

    def test_dateline_overlap(self):
        row = {"slat": -15, "nlat": 15, "llon": 170, "rlon": -170}
        self.assertTrue(crs.intersects(row, [175, -5, -175, 5]))
        self.assertFalse(crs.intersects(row, [-100, -5, -80, 5]))

    def test_favorites_persist_without_esri_settings(self):
        path = self.root / "settings" / "favorites.json"
        self.assertEqual(["EPSG:4326"], crs.change_favorite(path, "epsg:4326", "add"))
        self.assertEqual(["EPSG:4326"], crs.change_favorite(path, "EPSG:4326", "add"))
        self.assertEqual([], crs.change_favorite(path, "EPSG:4326", "remove"))

    def test_top_level_esri_folder_terms(self):
        tree = crs.tree_summary(crs.read_catalog(self.root), [], [])
        self.assertIn("Favorites", tree["Horizontal systems"])
        self.assertIn("Layers", tree["Horizontal systems"])
        self.assertEqual(2, tree["Horizontal systems"]["Projected Coordinate Systems"])
        self.assertEqual(1, tree["Vertical systems"]["Vertical Coordinate Systems"] if False else 0)
        self.assertIn("hierarchy_provenance", tree)

    def test_cli_json_and_no_download(self):
        with contextlib.redirect_stdout(io.StringIO()) as capture:
            self.assertEqual(0, crs.main(["--source", str(self.root), "--kind", "projcs",
                                          "--query", "WGS_1984_UTM", "--format", "json"]))
        result = json.loads(capture.getvalue())
        self.assertEqual(1, result["matched"])
        self.assertEqual(32636, int(result["results"][0]["wkid"]))


if __name__ == "__main__":
    unittest.main()
