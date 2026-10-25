import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ReadmeLayoutTests(unittest.TestCase):
    def test_banner_and_six_real_navigation_cards(self):
        md = (ROOT / "README.md").read_text(encoding="utf-8")
        ar = (ROOT / "README.ar.md").read_text(encoding="utf-8")
        ET.parse(ROOT / "assets/brand/banner-dark.svg")
        self.assertIn("assets/brand/banner-dark.svg", md)
        self.assertIn("assets/brand/banner-dark.svg", ar)
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

    def test_header_banner_tight_word_spacing_and_no_white_edges(self):
        """Protect the new 1600x500 full-bleed vector banner and readable word gaps."""
        path = ROOT / "assets/brand/banner-dark.svg"
        root = ET.parse(path).getroot()
        self.assertEqual(root.attrib.get("viewBox"), "0 0 1600 500")
        self.assertEqual(root.attrib.get("width"), "1600")
        self.assertEqual(root.attrib.get("height"), "500")
        ns = "{http://www.w3.org/2000/svg}"

        # The banner's solid background covers every edge; the logo itself
        # has an independently reusable transparent master.
        backgrounds = [node for node in root.findall(ns + "rect")
                       if node.get("width") == "1600" and node.get("height") == "500"]
        self.assertEqual(len(backgrounds), 1)
        self.assertEqual(backgrounds[0].get("fill"), "#101B24")
        transparent_logo = (ROOT / "assets/brand/logo-dark.svg").read_text(encoding="utf-8")
        self.assertNotIn('<rect width="1400"', transparent_logo)

        # SVG lays out adjacent tspans by glyph advance, not hardcoded
        # absolute word start X values. This prevents overlaps in Inter
        # and system fallback fonts at every responsive display size.
        name = root.find(".//*[@id='brand-name']")
        tagline = root.find(".//*[@id='brand-tagline']")
        self.assertIsNotNone(name)
        self.assertIsNotNone(tagline)
        name_parts = name.findall(ns + "tspan")
        self.assertEqual(["Development", "Skills"], [p.text for p in name_parts])
        self.assertIsNone(name_parts[1].get("x"))
        self.assertGreaterEqual(float(name_parts[1].get("dx")), 16)
        self.assertLessEqual(float(name_parts[1].get("dx")), 30)
        tagline_parts = tagline.findall(ns + "tspan")
        self.assertEqual(["The", "Heart", "of", "Geospatial", "Innovation"],
                         [p.text for p in tagline_parts])
        for word in tagline_parts[1:]:
            self.assertIsNone(word.get("x"))
            self.assertGreaterEqual(float(word.get("dx")), 8)
        palette = {p.text: p.get("fill") for p in name_parts + tagline_parts}
        self.assertEqual(palette["Heart"], "#82D53E")
        self.assertEqual(palette["Skills"], "#82D53E")
        self.assertEqual(palette["Innovation"], "#1CC8E8")
        self.assertEqual(palette["Geospatial"], "#398CE3")
        banner = path.read_text(encoding="utf-8")
        self.assertNotIn("<image", banner)
        self.assertNotIn("data:image/", banner)
        self.assertIn('id="gis-i-dot"', banner)


if __name__ == "__main__":
    unittest.main()
