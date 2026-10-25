"""Ensure integrated source has synced catalog, skills, index and safe licensing."""
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

class EarthViewIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project = json.loads((ROOT / "references/project-catalog.json").read_text(encoding="utf-8"))
        cls.apis = json.loads((ROOT / "references/free-geospatial-apis.json").read_text(encoding="utf-8"))
        cls.page = (ROOT / "index.html").read_text(encoding="utf-8")

    def test_single_reference_no_unlicensed_code_copy(self):
        rows = [x for x in self.project["projects"] if x["url"] == "https://github.com/colincode0/earth-view"]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["integration"], "architecture-reference-only-no-code-copy")
        self.assertIn("no-license-file-observed", rows[0]["license"])
        self.assertFalse(rows[0]["license_verified"])
        self.assertFalse(rows[0]["native_runtime_verified"])

    def test_existing_api_entries_are_reused(self):
        ids = [x["id"] for x in self.apis["services"]]
        self.assertEqual(ids.count("nasa-gibs"), 1)
        self.assertEqual(ids.count("copernicus-dataspace"), 1)

    def test_all_synchronized_surfaces_reference_guide(self):
        for path in ("index.html", "README.md", "README.ar.md",
                     "references/desktop-and-web.md",
                     "skills/geospatial-web-mapping/SKILL.md",
                     "skills/gis-desktop-application-development/SKILL.md",
                     "skills/remote-sensing-pipelines/SKILL.md",
                     "skills/geospatial-api-integration/SKILL.md"):
            self.assertIn("earth-view-architecture.md", (ROOT / path).read_text(encoding="utf-8"))
        self.assertIn('id="projectsCount">130<', self.page)
        self.assertIn("lang-ar", self.page)
        self.assertIn("lang-en", self.page)

    def test_future_source_intake_and_qa(self):
        self.assertIn("source-intake-workflow.md", (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8"))
        self.assertIn("python scripts/build_manifest.py --check",
                      (ROOT / "references/source-intake-workflow.md").read_text(encoding="utf-8"))
        review = (ROOT / "references/earth-view-architecture.md").read_text(encoding="utf-8")
        self.assertIn("WMS 1.3.0", review)
        self.assertIn("ASK_VIEW_VISIBLE = false", review)
