import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SecurityPerformanceTests(unittest.TestCase):
    def test_docs_linked_from_router(self):
        router = (ROOT / "skills/gis-development/SKILL.md").read_text(encoding="utf-8")
        for item in ("geospatial-security.md", "geospatial-performance.md", "gis-antipatterns.md"):
            self.assertIn(item, router)
            self.assertTrue((ROOT / "references" / item).is_file())

    def test_benchmark_verifies_result_not_just_speed(self):
        spec = importlib.util.spec_from_file_location("benchmark", ROOT / "scripts/benchmark_gis_examples.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        actual = mod.measure(2)
        self.assertEqual(actual["tier"], "T1")
        self.assertEqual(actual["expected_result"], "3 unique, 1 duplicate, 4 dangles")
        self.assertFalse(actual["native_gis_verified"])
