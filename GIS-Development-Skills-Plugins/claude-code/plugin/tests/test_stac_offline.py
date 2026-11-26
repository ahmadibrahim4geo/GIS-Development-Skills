"""Offline STAC metadata fixture test; no provider network traffic."""
import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("stac_preview",ROOT/"examples/stac-offline/inspect_items.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
FIXTURE=json.loads((ROOT/"examples/stac-offline/fixtures/stac_items.json").read_text(encoding="utf-8"))


class STACOfflineTests(unittest.TestCase):
    def test_cloud_bbox_and_date_filter(self):
        result=mod.inspect(FIXTURE,search_bbox=mod.bbox_filter([30,25,32,27]),
                           since=mod.utc_time("2026-01-01T00:00:00Z"),max_cloud=10)
        self.assertEqual([x["id"] for x in result],["synthetic-clear-2026-01-01"])
        self.assertEqual(result[0]["asset_keys"],["B04"])

    def test_missing_timezone_rejected(self):
        with self.assertRaises(ValueError):
            mod.utc_time("2026-01-01T10:00:00")

    def test_antimeridian_not_silently_accepted(self):
        with self.assertRaises(ValueError):
            mod.bbox_filter([170,0,-170,10])

    def test_bad_cloud_metadata_rejected(self):
        d=json.loads(json.dumps(FIXTURE))
        d["features"][0]["properties"]["eo:cloud_cover"]=102
        with self.assertRaises(ValueError):
            mod.inspect(d)

    def test_duplicate_ids_rejected(self):
        d=json.loads(json.dumps(FIXTURE))
        d["features"][1]["id"]=d["features"][0]["id"]
        with self.assertRaises(ValueError):
            mod.inspect(d)
