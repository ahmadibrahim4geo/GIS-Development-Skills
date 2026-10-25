"""Offline regression for the bilingual How to Use onboarding."""
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


class OnboardingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=set()
        self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag=="a" and a.get("href"):
            self.links.append(a["href"])


class HowToUseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home=(ROOT/"index.html").read_text(encoding="utf-8")
        cls.explorer=(ROOT/"explorer.html").read_text(encoding="utf-8")
        cls.links=OnboardingParser()
        cls.links.feed(cls.home)

    def test_home_stepper_language_and_copy(self):
        for element in ("how-to-use","howToHeading","howToCommand",
                        "howToExampleEn","howToExampleAr"):
            self.assertIn(element,self.links.ids)
        self.assertIn("#how-to-use",self.links.links)
        for key in ("copyUsage('install',this)","copyUsage('prompt',this)",
                    "navigator.clipboard.writeText(value)",
                    "document.documentElement.lang==='ar'",
                    "id=\"author\"","id=\"capabilities\""):
            self.assertIn(key,self.home)
        self.assertIn("npx skills add ahmadibrahim4geo/GIS-Development-Skills --skill gis-development",self.home)
        self.assertIn("The CLI installs skill instructions",self.home)

    def test_explorer_quick_start_preserved_and_enhanced(self):
        for key in ('id="get-started"','id="command"','id="copyBtn"',
                    'class="usage-four"','guideStep1:', 'guideManualTitle:',
                    'navStart:"طريقة الاستخدام"','navStart:"How to Use"',
                    'data-i18n="guideCaveat"','references/repository-manifest.json'):
            self.assertIn(key,self.explorer)

    def test_guides_exist_and_are_linked(self):
        for name in ("HOW_TO_USE.md","HOW_TO_USE.ar.md"):
            doc=ROOT/"docs"/name
            self.assertTrue(doc.is_file(),str(doc))
            body=doc.read_text(encoding="utf-8")
            for token in ("npx skills add", "KML/KMZ", "GIS"):
                self.assertIn(token,body)
            for page in (self.home,self.explorer):
                self.assertIn('href="docs/'+name+'"',page)
        self.assertIn("التراجع",(ROOT/"docs/HOW_TO_USE.ar.md").read_text(encoding="utf-8"))

    def test_no_native_execution_claims(self):
        for value in ("site is a guide and catalog","does not run ai agents"):
            combined=(self.home+" "+self.explorer+" "+
                      (ROOT/"docs/HOW_TO_USE.md").read_text(encoding="utf-8")).lower()
            self.assertIn(value,combined)


if __name__=="__main__":
    unittest.main()
