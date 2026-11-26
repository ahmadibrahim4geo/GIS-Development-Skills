import json
import math
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def crosses(a, b, c, d):
    def orient(p, q, r):
        return (q[0]-p[0]) * (r[1]-p[1]) - (q[1]-p[1]) * (r[0]-p[0])
    return orient(a, b, c) * orient(a, b, d) < 0 and orient(c, d, a) * orient(c, d, b) < 0


class FixtureTests(unittest.TestCase):
    def test_valid_and_invalid_polygon(self):
        rows = load("fixtures/geojson/valid_invalid_polygons.geojson")["features"]
        expected = load("fixtures/expected/expected-results.json")["polygons"]
        self.assertEqual(len(rows), expected["total"])
        rings = [f["geometry"]["coordinates"][0] for f in rows]
        self.assertFalse(crosses(rings[0][0], rings[0][1], rings[0][2], rings[0][3]))
        self.assertTrue(crosses(rings[1][0], rings[1][1], rings[1][2], rings[1][3]))

    def test_one_degree_is_not_one_metre(self):
        values = load("fixtures/geojson/points_lines.geojson")["features"]
        a, b = values[0]["geometry"]["coordinates"], values[1]["geometry"]["coordinates"]
        radius = 6371000.0
        lat1, lat2 = math.radians(a[1]), math.radians(b[1])
        dlat, dlon = lat2 - lat1, math.radians(b[0] - a[0])
        hav = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
        distance = 2 * radius * math.asin(math.sqrt(hav))
        expect = load("fixtures/expected/expected-results.json")["distances"]
        self.assertLess(abs(distance - expect["great_circle_spherical_approx_m"]), expect["tolerance_m"])

    def test_binary_fixture_generation_recipe_is_available(self):
        text = (ROOT / "fixtures/generate_binary_fixtures.py").read_text(encoding="utf-8")
        for signature in ("ESRI Shapefile", "multilayer.gpkg", "nodata_4326.tif", "misaligned_3857.tif"):
            self.assertIn(signature, text)
