"""Offline tests for additive synthetic GIS examples."""
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(relative, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ProductionExamplesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.network = load("examples/network-topology/audit_network.py", "network_example")
        cls.weather = load("examples/api-ingestion/weather_to_geojson.py", "weather_example")

    def test_network_fixture(self):
        raw = json.loads((ROOT / "examples/network-topology/fixtures/network.geojson").read_text(encoding="utf-8"))
        result = self.network.audit(raw)
        self.assertEqual(result["unique_lines"], 3)
        self.assertEqual(result["duplicates"], [{"id": "reversed-duplicate", "same_as": "main-1"}])
        self.assertEqual(len(result["dangles"]), 4)

    def test_network_rejects_unsupported_geometries(self):
        with self.assertRaises(ValueError):
            self.network.audit({"type": "FeatureCollection", "features": [
                {"geometry": {"type": "Point", "coordinates": [31, 30]}}]})

    def test_weather_fixture(self):
        raw = json.loads((ROOT / "examples/api-ingestion/fixtures/open_meteo_hourly.json").read_text(encoding="utf-8"))
        result = self.weather.convert(raw, 30, 31)
        self.assertEqual(len(result["features"]), 2)
        one = result["features"][0]
        self.assertEqual(one["geometry"]["coordinates"], [31.0, 30.0])
        self.assertEqual(one["properties"]["temperature_c"], 15.2)
        self.assertEqual(one["properties"]["timestamp_utc"], "2026-01-01T00:00Z")

    def test_weather_bad_coordinates_or_units(self):
        raw = json.loads((ROOT / "examples/api-ingestion/fixtures/open_meteo_hourly.json").read_text(encoding="utf-8"))
        with self.assertRaises(ValueError):
            self.weather.convert(raw, 91, 31)
        raw["hourly_units"]["temperature_2m"] = "°F"
        with self.assertRaises(ValueError):
            self.weather.convert(raw, 30, 31)

    def test_navigation_paths_are_bilingual(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        for md in ("README.md", "README.ar.md"):
            text = (ROOT / md).read_text(encoding="utf-8")
            for target in ("examples/README.md", "docs/QUALITY_BENCHMARK.md",
                           "spatial-databases", "geospatial-data-processing",
                           "remote-sensing-pipelines"):
                self.assertIn(target, text)
                self.assertIn(target, html)
        self.assertIn('data-i18n="examplesTitle"', html)
        self.assertIn("examplesTitle:", html)


if __name__ == "__main__":
    unittest.main()
