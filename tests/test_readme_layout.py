import struct
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ReadmeLayoutTests(unittest.TestCase):
    def test_banner_and_six_real_navigation_cards(self):
        md = (ROOT / "README.md").read_text(encoding="utf-8")
        ar = (ROOT / "README.ar.md").read_text(encoding="utf-8")
        ET.parse(ROOT / "assets/brand/banner-dark.svg")
        self.assertIn("assets/brand/banner.png", md)
        self.assertIn("assets/brand/banner.png", ar)
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

    def test_supplied_banner_has_native_six_to_one_ratio(self):
        brand = ROOT / "assets" / "brand"
        for filename in ("banner-dark.svg", "banner-light.svg"):
            svg = ET.parse(brand / filename).getroot()
            self.assertEqual(svg.get("viewBox"), "0 0 2400 400")
        png_header = (brand / "banner.png").read_bytes()[:24]
        self.assertEqual(png_header[:8], bytes.fromhex("89 50 4E 47 0D 0A 1A 0A"))
        self.assertEqual(struct.unpack(">II", png_header[16:24]), (2400, 400))


if __name__ == "__main__":
    unittest.main()
