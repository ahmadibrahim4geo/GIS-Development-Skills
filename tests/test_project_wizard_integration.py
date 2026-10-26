"""Bilingual GIS Project Wizard integration and JavaScript smoke checks."""
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


class WizardIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.wizard=(ROOT/"project-wizard.html").read_text(encoding="utf-8")
        cls.home=(ROOT/"index.html").read_text(encoding="utf-8")
        cls.explorer=(ROOT/"explorer.html").read_text(encoding="utf-8")
        cls.manifest=json.loads((ROOT/"references/repository-manifest.json").read_text(encoding="utf-8"))

    def test_wizard_exists_and_is_linked_from_home(self):
        self.assertIn('href="project-wizard.html"',self.home)
        self.assertIn('id="generate"',self.wizard)
        self.assertIn('id="download"',self.wizard)
        self.assertIn("URL.createObjectURL",self.wizard)
        self.assertIn("textContent=output",self.wizard)
        for name in ('docs/PROJECT_WIZARD_PLAN.md','docs/PERFORMANCE_RELIABILITY.md',
                     'skills/kml-kmz-engineering/SKILL.md'):
            self.assertIn(name,self.wizard)
            self.assertTrue((ROOT/name).is_file(),name)

    def test_manifest_and_licensing_include_multilingual_skill(self):
        slug="gis-internationalization-arabic"
        self.assertIn(slug,self.manifest["skill_ids"])
        self.assertEqual(self.manifest["skill_count"],len(list((ROOT/"skills").glob("*/SKILL.md"))))
        self.assertIn(slug,(ROOT/"references/free-first-policy.md").read_text(encoding="utf-8"))
        self.assertIn(slug,self.home)
        self.assertIn(slug,self.explorer)
        self.assertIn(slug,(ROOT/"skills/gis-development/SKILL.md").read_text(encoding="utf-8"))

    def test_bilingual_ui_and_download_claims(self):
        for field in ('id="type"','id="locale"','id="files"','id="license"',
                      'id="details"','id="result"'):
            self.assertIn(field,self.wizard)
        for label in ('العربية','English','document.documentElement.dir',
                      'Arabic + English','Download Markdown'):
            self.assertIn(label,self.wizard)
        self.assertNotIn("};\\nconst stacks",self.wizard)
        self.assertNotIn("</select>\\n<label",self.wizard)

    def test_inline_javascript_syntax(self):
        node=shutil.which("node")
        if not node:
            self.skipTest("Node unavailable: static checks only")
        scripts=re.findall(r"<script>(.*?)</script>",self.wizard,re.S)
        self.assertEqual(len(scripts),1)
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/"wizard.js"
            p.write_text(scripts[0],encoding="utf-8")
            result=subprocess.run([node,"--check",str(p)],capture_output=True,text=True,timeout=15)
            self.assertEqual(result.returncode,0,result.stderr)


if __name__=="__main__":
    unittest.main()
