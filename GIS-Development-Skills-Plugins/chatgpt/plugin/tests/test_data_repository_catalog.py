"""Offline GIS data repository catalog and search regression checks."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RepositoryDirectoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load("validate_data_repositories", "scripts/validate_data_repositories.py")
        cls.searcher = load("search_sources", "examples/data-catalogs/search_sources.py")
        cls.document = json.loads((ROOT / "references/geospatial-data-repositories.json").read_text(encoding="utf-8"))
        cls.entries = cls.document["repositories"]

    def test_schema_and_distinct_urls(self):
        self.assertEqual([], self.validator.validate())
        self.assertGreaterEqual(len(self.entries), 20)
        self.assertEqual(len({x["url"].casefold().rstrip("/") for x in self.entries}), len(self.entries))

    def test_our_large_source_index_is_linked_not_copied(self):
        refs = [x for x in self.entries if x["id"] == "ahmad-gis-data-repositories"]
        self.assertEqual(1, len(refs))
        self.assertIn("gis-data-repositories-professional-2026", refs[0]["url"])
        self.assertLess(len(self.entries), 100)

    def test_search_is_bounded_and_case_insensitive(self):
        matches = self.searcher.search(self.entries, query="stac", limit=4)
        self.assertGreaterEqual(len(matches), 2)
        self.assertLessEqual(len(matches), 4)
        self.assertTrue(any(x["type"] == "catalog-index" for x in matches))
        self.assertEqual([], self.searcher.search(self.entries, query="STAC", limit=0))
        with self.assertRaises(ValueError):
            self.searcher.search(self.entries, limit=-1)

    def test_exact_catalog_type_and_category(self):
        matches = self.searcher.search(self.entries, kind="catalog-index")
        self.assertTrue(matches)
        self.assertTrue(all(x["type"] == "catalog-index" for x in matches))
        self.assertTrue(self.searcher.search(self.entries, category="bathymetry-dem"))

    def test_failing_duplicate_and_non_https(self):
        entries = [dict(x) for x in self.entries]
        entries.append(dict(entries[0]))
        entries[-1]["url"] = "http://untrusted.example"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sources.json"
            path.write_text(json.dumps({"schema_version": "1.0", "repositories": entries}), encoding="utf-8")
            failures = self.validator.validate(path)
        self.assertTrue(any("duplicate id" in x for x in failures))
        self.assertTrue(any("HTTPS url" in x for x in failures))

    def test_website_separate_bilingual_repository_tab(self):
        html = (ROOT / "explorer.html").read_text(encoding="utf-8")
        self.assertIn('id="repositoriesTab"', html)
        self.assertIn('id="dataCount">{}'.format(len(self.entries)), html)
        self.assertIn('loadCatalog("repositories","references/geospatial-data-repositories.json"', html)
        self.assertIn('repositoriesTab:"مستودعات البيانات"', html)

    def test_manifest_lists_repository_count(self):
        manifest = json.loads((ROOT / "references/repository-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(len(self.entries), manifest["data_repository_count"])
