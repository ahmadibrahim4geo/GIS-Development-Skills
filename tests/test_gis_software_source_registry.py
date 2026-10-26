"""Offline checks for the shared GIS software source-code registry.

Tests validate source catalog wiring and provenance claims. No upstream binary,
service or GIS host is executed or declared compatible by these tests.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "references" / "project-catalog.json"
GUIDE = ROOT / "references" / "gis-software-source-registry.md"
ADDED_ON = "2026-10-26"


class SoftwareRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads(CATALOG.read_text(encoding="utf-8"))
        cls.entries = cls.doc["projects"]
        cls.new = [x for x in cls.entries if x.get("repository_access_checked_on") == ADDED_ON]

    def test_single_catalog_and_unique_urls(self):
        self.assertGreaterEqual(len(self.entries), 188)
        normalized = [x["url"].rstrip("/").casefold() for x in self.entries]
        self.assertEqual(len(normalized), len(set(normalized)))
        self.assertIn("project-catalog.json", GUIDE.read_text(encoding="utf-8"))
        self.assertFalse((ROOT / "references" / "gis-software-source-registry.json").exists())

    def test_added_repositories_are_real_source_references_not_install_claims(self):
        self.assertEqual(len(self.new), 40)
        for entry in self.new:
            with self.subTest(project=entry["name"]):
                self.assertTrue(entry["url"].startswith("https://github.com/"))
                self.assertIn(entry["role"], {"application", "engine", "framework", "library", "server"})
                self.assertEqual(entry["integration"], "reference-only")
                self.assertEqual(entry["status"], "unknown")
                self.assertIsNone(entry["last_checked"])
                self.assertFalse(entry["license_verified"])
                self.assertFalse(entry["tested_by_repository"])
                self.assertFalse(entry["native_runtime_verified"])
                self.assertEqual(entry["license"], "verify-upstream")
                self.assertTrue(entry["license_metadata_unverified"])
                self.assertTrue((ROOT / "skills" / entry["primary_skill"] / "SKILL.md").is_file())
                self.assertEqual(entry["source_availability"], "public-repository;build-not-verified")

    def test_all_software_families_represented(self):
        names = {x["url"].split("/")[-1].casefold() for x in self.entries}
        for slug in (
            "qgis", "geolibre", "rustgis", "openjump", "qfield", "mobile",
            "mapstore2", "geonode", "terriajs", "terriamap", "kepler.gl",
            "maplibre-native", "openlayers", "leaflet", "gdal", "postgis",
            "pdal", "mapsui", "geoda", "snap-desktop", "snap-engine",
            "geoserver", "stac-browser", "eo-learn",
        ):
            with self.subTest(repo=slug):
                self.assertIn(slug, names)

    def test_skill_entrypoints_and_bilingual_site(self):
        for file in (
            "skills/gis-development/SKILL.md",
            "skills/gis-desktop-application-development/SKILL.md",
            "skills/geospatial-web-mapping/SKILL.md",
            "README.md",
            "README.ar.md",
            "index.html",
            "explorer.html",
        ):
            with self.subTest(file=file):
                self.assertIn("gis-software-source-registry.md",
                              (ROOT / file).read_text(encoding="utf-8"))
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="software-registry"', home)
        self.assertIn('data-lang="en">GIS SOFTWARE', home)
        self.assertIn('data-lang="ar">دليل البرامج', home)
        self.assertIn('id="author"', home)
        self.assertIn("ahmad_ibrahim_original.png", home)

    def test_explorer_exposes_usable_skill_handoff(self):
        page = (ROOT / "explorer.html").read_text(encoding="utf-8")
        self.assertIn('entry.primary_skill', page)
        self.assertIn('entry.role', page)
        self.assertIn('entry.platforms', page)
        self.assertIn('repository_access_checked_on', page)
        self.assertIn('skills/"+entry.primary_skill+"/SKILL.md', page)
        self.assertIn("Repository available; builds and reuse rights still unverified.", page)
        self.assertIn('x.primary_skill,x.programming_language', page)

    def test_manifest_counters_match_source(self):
        manifest = json.loads((ROOT / "references" / "repository-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(len(self.entries), manifest["reference_count"])
        for file in ("index.html", "explorer.html"):
            with self.subTest(file=file):
                text = (ROOT / file).read_text(encoding="utf-8")
                self.assertIn('id="projectsCount"', text)
                self.assertIn(">" + str(len(self.entries)) + "</strong>", text)


if __name__ == "__main__":
    unittest.main()
