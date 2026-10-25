"""Offline tests for World Gazetteer sample, no web requests or GIS-native claims."""
import importlib.util
import sqlite3
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "examples/gazetteer/viewport_labels.py"
spec = importlib.util.spec_from_file_location("world_gazetteer", p)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


class WorldGazetteerTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        g.create_schema(self.db)
        self.db.executemany("INSERT INTO places VALUES (?,?,?,?,?,?,?,?,?)", [
            (1, "Egypt", 26, 30, "A", "PCLI", "EG", 0, 0),
            (2, "Cairo", 30.04, 31.24, "P", "PPLC", "EG", 10000000, 1),
            (3, "Aswan", 24.08, 32.9, "P", "PPLA", "EG", 350000, 2),
            (4, "Small village", 24.2, 32.8, "P", "PPL", "EG", 500, 5),
            (5, "East island", 0, 179.6, "T", "ISL", "FJ", 0, 5),
            (6, "West island", 0, -179.6, "T", "ISL", "FJ", 0, 5),
        ])
        self.db.commit()

    def tearDown(self):
        self.db.close()

    def test_layer_off_search_still_works(self):
        self.assertEqual([], g.viewport_labels(
            self.db, (20, 15, 40, 35), 100000, enabled=False))
        self.assertEqual("Cairo", g.search_places(self.db, "Cair")[0]["name"])

    def test_scale_filter(self):
        names = [p["name"] for p in g.viewport_labels(
            self.db, (20, 15, 40, 35), 60000000)]
        self.assertIn("Egypt", names)
        self.assertIn("Cairo", names)
        self.assertNotIn("Small village", names)
        detailed = [p["name"] for p in g.viewport_labels(
            self.db, (30, 23, 35, 26), 100000)]
        self.assertIn("Small village", detailed)

    def test_dateline(self):
        names = [p["name"] for p in g.viewport_labels(
            self.db, (179, -2, -179, 2), 100000, width_px=1000)]
        self.assertIn("East island", names)
        self.assertIn("West island", names)

    def test_invalid_bbox(self):
        with self.assertRaises(ValueError):
            g.viewport_labels(self.db, (-200, 0, 30, 10), 1000)
        with self.assertRaises(ValueError):
            g.viewport_labels(self.db, (20, 20, 30, 10), 1000)

    def test_import_arabic_tsv(self):
        with tempfile.TemporaryDirectory() as directory:
            cols = ["90", "سوهاج", "Sohag", "", "26.56", "31.69",
                    "P", "PPLA", "EG", "", "15", "", "", "", "250000",
                    "", "", "Africa/Cairo", "2026-10-01"]
            name = Path(directory) / "EG.txt"
            name.write_text("\t".join(cols) + "\n", encoding="utf-8")
            self.assertEqual(1, g.import_tsv(self.db, name, batch_size=1))
            self.assertEqual("سوهاج", g.search_places(self.db, "سوهاج")[0]["name"])
            visible = g.viewport_labels(self.db, (30, 25, 33, 28), 3000000)
            self.assertIn("سوهاج", [item["name"] for item in visible])
            self.assertEqual(2, len(visible))


if __name__ == "__main__":
    unittest.main()
