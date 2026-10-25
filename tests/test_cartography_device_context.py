"""Offline tests for independently authored GIS symbology and device-time fixtures."""
import json
import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples" / "device-context"))
from device_context import build_context  # noqa: E402


class DeviceContextTests(unittest.TestCase):
    def test_simulated_cairo_summer_offset(self):
        ctx = build_context(30.0444, 31.2357, "Africa/Cairo", "2026-07-01T12:00:00+03:00")
        self.assertEqual(ctx["time_utc"], "2026-07-01T09:00:00+00:00")
        self.assertEqual(ctx["location_source"], "manual")
        self.assertEqual(ctx["permission_status"], "not_requested")
        self.assertEqual(ctx["time_mode"], "simulated")

    def test_rejects_naive_time(self):
        with self.assertRaises(ValueError):
            build_context(10, 20, "UTC", "2026-07-01T12:00:00")

    def test_rejects_wrong_dst_offset(self):
        with self.assertRaises(ValueError):
            build_context(30, 31, "Africa/Cairo", "2026-07-01T12:00:00+02:00")

    def test_rejects_bad_coordinates(self):
        for lat, lon in [(91, 0), (0, 181), (math.nan, 0), (0, math.inf)]:
            with self.subTest(lat=lat, lon=lon), self.assertRaises(ValueError):
                build_context(lat, lon, "UTC", "2026-01-01T00:00:00Z")

    def test_live_clock_is_aware(self):
        ctx = build_context(-90, 180, "UTC")
        self.assertEqual(ctx["time_mode"], "live")
        self.assertTrue(ctx["time_utc"].endswith("+00:00"))


class CartographyFixtureTests(unittest.TestCase):
    def test_vector_style_is_consistent(self):
        spec = json.loads((ROOT / "examples/cartography/maplibre-demo-style.json").read_text(encoding="utf-8"))
        self.assertEqual(spec["version"], 8)
        self.assertEqual({l["type"] for l in spec["layers"]}, {"fill", "line", "circle"})
        self.assertEqual(len({l["id"] for l in spec["layers"]}), len(spec["layers"]))
        self.assertEqual(len(spec["sources"]["synthetic"]["data"]["features"]), 3)

    def test_catalog_sources_unique_with_licensing(self):
        data = json.loads((ROOT / "references/cartographic-style-sources.json").read_text(encoding="utf-8"))
        sources = data["sources"]
        self.assertGreaterEqual(len(sources), 8)
        self.assertEqual(len({x["id"] for x in sources}), len(sources))
        for item in sources:
            self.assertTrue(item["url"].startswith("https://"))
            self.assertTrue(item["license_status"])
            self.assertTrue(item["redistribution"])


if __name__ == "__main__":
    unittest.main()
