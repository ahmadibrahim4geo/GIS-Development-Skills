"""GIS studio landing page regression: real onboarding and protected author section."""
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Elements(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=[]
        self.link_targets=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get("id"):
            self.ids.append(a["id"])
        if tag=="a" and a.get("href"):
            self.link_targets.append(a["href"])


class StudioHomepageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.site=(ROOT/"index.html").read_text(encoding="utf-8")
        cls.css=(ROOT/"assets/home-redesign.css").read_text(encoding="utf-8")
        cls.parser=Elements()
        cls.parser.feed(cls.site)

    def test_hero_brand_metric_and_design_system(self):
        self.assertIn('class="studio-hero"',self.site)
        self.assertIn('src="assets/brand/logo-dark.svg"',self.site)
        self.assertIn('href="assets/home-redesign.css"',self.site)
        for token in (".studio-hero", ".studio-metrics", ".studio-howto",
                      ".studio-how-grid", "@media(max-width:610px)",
                      ".author-panel.mirsad-author"):
            self.assertIn(token,self.css)
        expected=json.loads((ROOT/"references/repository-manifest.json").read_text(encoding="utf-8"))["skill_count"]
        self.assertEqual(int(re.search(r'id="skillsCount"[^>]*>(\d+)',self.site).group(1)),expected)

    def test_all_guidance_is_in_homepage(self):
        for i in ("how-to-use","howToHeading","studioPlatform","howToCommand",
                  "studioSpecialistCommand","howToExampleEn","howToExampleAr",
                  "studioChoiceEn","studioChoiceAr","cliText","copyCliBtn"):
            self.assertIn(i,self.parser.ids)
        for slug in ("gis-development","arcgis-toolbox-engineering","qgis-plugin-development",
                     "kml-kmz-engineering","gis-desktop-application-development",
                     "geospatial-web-mapping","remote-sensing-pipelines",
                     "geospatial-data-processing"):
            self.assertIn('value="'+slug+'"',self.site)
        for text in ("copyUsage('install',this)","copyUsage('specialist',this)",
                     "copyUsage('prompt',this)","function updateStudioTopic()",
                     "navigator.clipboard.writeText(value)",'href="#how-to-use"'):
            self.assertIn(text,self.site)
        self.assertIn("Node.js",self.site)
        self.assertIn("native GIS",self.site)
        self.assertIn("سجل",self.site)

    def test_author_markup_and_contacts_preserved(self):
        author=self.site.split('<section id="author"',1)[1].split("</section>",1)[0]
        for token in ('class="author-panel mirsad-author"',
                      "ahmad_ibrahim_original.png",
                      'أحمد إبراهيم','Ahmad Ibrahim',
                      'mailto:ahmadibrahim.geo@gmail.com',
                      'https://wa.me/201111915925',
                      'https://github.com/ahmadibrahim4geo',
                      'class="consultation"'):
            self.assertIn(token,author)
        self.assertEqual(self.site.count('id="author"'),1)

    def test_bilingual_pages_and_no_duplicate_ids(self):
        self.assertEqual(len(self.parser.ids),len(set(self.parser.ids)),
                         "No duplicate DOM ids allowed")
        self.assertIn('data-lang="en"',self.site)
        self.assertIn('data-lang="ar"',self.site)
        self.assertIn('onclick="toggleLanguage()"',self.site)
        self.assertIn('id="mobileMenu"',self.site)
        self.assertIn("renderPathways()",self.site)
        self.assertIn("function copyStudioText(value, button, focusTarget)",self.site)
        self.assertIn("studio-tab-active",self.site)
        self.assertIn('href="explorer.html#all-skills"',self.site)


if __name__=="__main__":
    unittest.main()
