import json
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DiscoverabilityTests(unittest.TestCase):
    def test_homepage_has_canonical_social_and_structured_metadata(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        expected = (
            'name="description"',
            'rel="canonical" href="https://ahmadibrahim4geo.github.io/GIS-Development-Skills/"',
            'property="og:title"',
            'property="og:description"',
            'property="og:image"',
            'name="twitter:card" content="summary_large_image"',
            'type="application/ld+json"',
        )
        for token in expected:
            self.assertIn(token, html)
        raw = html.split('<script type="application/ld+json">', 1)[1].split("</script>", 1)[0]
        metadata = json.loads(raw)
        self.assertEqual("SoftwareSourceCode", metadata["@type"])
        self.assertEqual(
            "https://github.com/ahmadibrahim4geo/GIS-Development-Skills",
            metadata["codeRepository"],
        )
        self.assertEqual(["en", "ar"], metadata["inLanguage"])

    def test_sitemap_and_robots_use_project_subpath(self):
        sitemap = ROOT / "sitemap.xml"
        root = ET.parse(sitemap).getroot()
        namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        urls = [node.text for node in root.findall(f"{namespace}url/{namespace}loc")]
        self.assertGreaterEqual(len(urls), 3)
        for url in urls:
            self.assertTrue(url.startswith(
                "https://ahmadibrahim4geo.github.io/GIS-Development-Skills/"
            ))
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("/GIS-Development-Skills/sitemap.xml", robots)

    def test_community_entry_files_exist(self):
        self.assertTrue((ROOT / "CODE_OF_CONDUCT.md").is_file())
        template = (ROOT / ".github/PULL_REQUEST_TEMPLATE.md").read_text(encoding="utf-8")
        for token in ("CRS/units", "T0–T4", "NOT RUN", "security_audit.py"):
            self.assertIn(token, template)


if __name__ == "__main__":
    unittest.main()
