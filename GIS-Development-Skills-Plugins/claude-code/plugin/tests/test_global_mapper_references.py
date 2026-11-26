"""Global Mapper / Blue Marble repository-intake regression tests (offline only)."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORG = "https://github.com/Blue-Marble-Geographics/"


class GlobalMapperReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project = json.loads((ROOT / "references/project-catalog.json").read_text(encoding="utf-8"))
        cls.entries = cls.project["projects"]
        cls.apis = json.loads((ROOT / "references/free-geospatial-apis.json").read_text(encoding="utf-8"))
        cls.html = (ROOT / "explorer.html").read_text(encoding="utf-8")

    def test_official_forks_and_nonofficial_community_separated(self):
        forks = [x for x in self.entries if x["url"].startswith(ORG)]
        self.assertEqual(7, len(forks))
        for item in forks:
            self.assertEqual("reference-only-fork-check-upstream-license", item["integration"])
            self.assertIn("origin_repository", item)
            self.assertFalse(item["license_verified"] or item["native_runtime_verified"])
        community = [x for x in self.entries if x["url"] == "https://github.com/PeterSanctus/GM-Scripting"]
        self.assertEqual(len(community), 1)
        self.assertIn("GPL-3.0", community[0]["license"])
        self.assertNotIn("Blue Marble fork", community[0]["name"])

    def test_commercial_sdk_not_open_web_api(self):
        ids = [x["id"] for x in self.apis["services"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(ids), 52)
        self.assertFalse(any("globalmapper" in x or "blue-marble" in x for x in ids))
        guide = (ROOT / "references/blue-marble-global-mapper.md").read_text(encoding="utf-8")
        self.assertIn("commercial", guide.lower())
        self.assertIn("DLL", guide)
        self.assertIn("MPL-2.0", guide)
        self.assertIn("AGPL-3.0", guide)

    def test_all_readmes_and_index_synced(self):
        self.assertIn('id="projectsCount">{}'.format(len(self.entries)), self.html)
        self.assertIn('data-i18n="gmTitle"', self.html)
        self.assertIn('gmTitle:"تطوير Global Mapper"', self.html)
        self.assertIn("blue-marble-global-mapper.md", self.html)
        self.assertIn("Blue Marble Geographics", (ROOT / "README.md").read_text(encoding="utf-8"))
        self.assertIn("blue-marble-global-mapper.md", (ROOT / "README.ar.md").read_text(encoding="utf-8"))

    def test_agent_and_specialists_linked(self):
        paths = ("skills/gis-development/SKILL.md",
                 "skills/global-mapper-development/SKILL.md",
                 "skills/terrain-hydrology-lidar/SKILL.md",
                 "skills/geospatial-web-mapping/SKILL.md",
                 "skills/gis-desktop-application-development/SKILL.md")
        self.assertTrue(all((ROOT / path).is_file() for path in paths))
        for path in paths:
            self.assertIn("global-mapper-development" if path.endswith("gis-development/SKILL.md")
                          else "blue-marble-global-mapper",
                          (ROOT / path).read_text(encoding="utf-8"))

    def test_manifest_counts(self):
        data = json.loads((ROOT / "references/repository-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(data["reference_count"], len(self.entries))
        self.assertEqual(data["skill_count"], len(list((ROOT / "skills").glob("*/SKILL.md"))))
