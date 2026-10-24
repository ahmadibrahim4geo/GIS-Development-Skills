import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("inventory", ROOT / "scripts/build_manifest.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class InventoryMetadataTests(unittest.TestCase):
    def test_single_source_counts(self):
        data = mod.derived()
        self.assertEqual((data["skill_count"], data["reference_count"], data["api_count"]), (11, 104, 39))
        saved = json.loads((ROOT / "references/repository-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(data, saved)

    def test_all_metadata_explicitly_unverified(self):
        for filename, key in [("project-catalog.json", "projects"), ("free-geospatial-apis.json", "services")]:
            data = json.loads((ROOT / "references" / filename).read_text(encoding="utf-8"))
            for item in data[key]:
                self.assertIn(item["status"], ("active", "archived", "unknown"))
                self.assertFalse(item["tested_by_repository"] or item["native_runtime_verified"])
                self.assertTrue(item["last_checked"] is None or isinstance(item["last_checked"], str))

    def test_readme_current_counters(self):
        self.assertEqual(mod.synchronize_text(ROOT, mod.derived(), write=False), [])
