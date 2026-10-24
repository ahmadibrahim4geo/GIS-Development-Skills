import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ReadmeLayoutTests(unittest.TestCase):
    def test_banner_and_six_real_navigation_cards(self):
        md = (ROOT / "README.md").read_text(encoding="utf-8")
        ar = (ROOT / "README.ar.md").read_text(encoding="utf-8")
        ET.parse(ROOT / "assets/readme-banner.svg")
        self.assertIn("assets/readme-banner.svg", md)
        self.assertIn("assets/readme-banner.svg", ar)
        self.assertEqual(md.count("<td align=\"center\" valign=\"top\""), 6)
        self.assertNotIn("<strong>The Heart of Geospatial Innovation</strong>", md)
        self.assertIn("Build GIS tools, plugins and geospatial applications with a verifiable development workflow.", md)
        links = [
           "skills/arcgis-toolbox-engineering/SKILL.md",
           "references/free-geospatial-apis.md",
           "skills/gis-development/SKILL.md",
           "skills/geospatial-web-mapping/SKILL.md",
           "skills/gis-desktop-application-development/SKILL.md",
           "references",
        ]
        for link in links:
            self.assertIn('href="' + link + '"', md)
            self.assertTrue((ROOT / link).exists(), link)
        for name in ("tools", "apis", "development", "maps", "desktop", "guides"):
            ET.parse(ROOT / "assets" / ("readme-" + name + ".svg"))
        self.assertNotIn("v1.0.0", md.split("## What makes this different")[0])

if __name__ == "__main__":
    unittest.main()
