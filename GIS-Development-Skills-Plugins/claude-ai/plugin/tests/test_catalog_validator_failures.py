"""Negative fixtures: validators should report errors, never crash."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


class DefensiveCatalogValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.projects = module("projects_validator", "validate_catalog.py")
        cls.apis = module("apis_validator", "validate_api_catalog.py")
        cls.original_projects = json.loads(
            (ROOT / "references" / "project-catalog.json").read_text(encoding="utf-8")
        )
        cls.original_apis = json.loads(
            (ROOT / "references" / "free-geospatial-apis.json").read_text(encoding="utf-8")
        )

    def fixture(self, data):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        p = Path(tmp.name) / "catalog.json"
        p.write_text(json.dumps(data), encoding="utf-8")
        return p

    def test_url_duplicates_even_with_trailing_slash(self):
        src = self.original_projects
        record = dict(src["projects"][0])
        extra = dict(record, url=record["url"].rstrip("/") + "/")
        fixture = self.fixture(dict(schema_version="1.0", projects=[record, extra]))
        self.assertTrue(any("duplicate URL" in e for e in self.projects.validate_catalog(fixture)))

    def test_bad_project_catalog_root(self):
        self.assertTrue(any("root" in e for e in self.projects.validate_catalog(self.fixture([]))))

    def test_api_identifier_is_list_not_hashable(self):
        record = dict(self.original_apis["services"][0], id=["bad"])
        fixture = self.fixture(dict(schema_version="1.0", services=[record]))
        self.assertTrue(any("invalid id" in e for e in self.apis.validate_catalog(fixture)))

    def test_api_broken_https_url(self):
        record = dict(self.original_apis["services"][0], documentation_url="https://")
        fixture = self.fixture(dict(schema_version="1.0", services=[record]))
        self.assertTrue(any("HTTPS URL" in e for e in self.apis.validate_catalog(fixture)))

    def test_api_access_wrong_type_is_reported(self):
        for access in ([], {}, None, 42):
            with self.subTest(access=access):
                record = dict(self.original_apis["services"][0], access=access)
                fixture = self.fixture(dict(schema_version="1.0", services=[record]))
                errors = self.apis.validate_catalog(fixture)
                self.assertTrue(any("invalid access" in e for e in errors))
                self.assertTrue(any("unknown access type" in e for e in errors))

    def test_api_malformed_urls_are_reported(self):
        for field in ("documentation_url", "service_url", "example_url"):
            for url in ("https://[broken", "https://[not-an-ip]"):
                with self.subTest(field=field, url=url):
                    record = dict(self.original_apis["services"][0], **{field: url})
                    fixture = self.fixture(dict(schema_version="1.0", services=[record]))
                    errors = self.apis.validate_catalog(fixture)
                    self.assertTrue(any(field + " must be a valid HTTPS URL" in e for e in errors))

    def test_api_url_whitespace_is_reported(self):
        for field in ("documentation_url", "service_url", "example_url"):
            for url in ("https://example.com/\n", "https://example.com/\t"):
                with self.subTest(field=field, url=url):
                    record = dict(self.original_apis["services"][0], **{field: url})
                    fixture = self.fixture(dict(schema_version="1.0", services=[record]))
                    errors = self.apis.validate_catalog(fixture)
                    self.assertTrue(any(field + " must be a valid HTTPS URL" in e for e in errors))

    def test_bad_api_catalog_root(self):
        self.assertTrue(any("root" in e for e in self.apis.validate_catalog(self.fixture([]))))

    def test_broken_json_is_reported_not_raised(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text("{bad-json", encoding="utf-8")
            self.assertTrue(self.projects.validate_catalog(path))
            self.assertTrue(self.apis.validate_catalog(path))


if __name__ == "__main__":
    unittest.main()
