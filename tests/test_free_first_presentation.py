"""Offline free-first catalog, skill and website invariants."""
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


class FreeFirstSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html=(ROOT/"index.html").read_text(encoding="utf-8")
        cls.api=json.loads((ROOT/"references/free-geospatial-apis.json").read_text(encoding="utf-8"))
        cls.manifest=json.loads((ROOT/"references/repository-manifest.json").read_text(encoding="utf-8"))
        cls.policy=(ROOT/"references/free-first-policy.md").read_text(encoding="utf-8")

    def test_all_skills_link_policy_and_manifest(self):
        skills=sorted(p.parent.name for p in (ROOT/"skills").glob("*/SKILL.md"))
        self.assertGreaterEqual(len(skills),15)
        self.assertEqual(skills,self.manifest["skill_ids"])
        for slug in skills:
            with self.subTest(slug=slug):
                self.assertIn("free-first-policy.md",(ROOT/"skills"/slug/"SKILL.md").read_text(encoding="utf-8"))
                self.assertIn(slug,self.policy)

    def test_api_cost_metadata_and_default_subset(self):
        rows=self.api["services"]
        self.assertEqual(self.manifest["api_count"],len(rows))
        self.assertEqual(sum(s["access"] in {"free-noncommercial","public-fair-use","free-registration","free-key-required","free-limited","public-with-asset-restrictions","self-hosted-open-source"} for s in rows),sum(s["cost_tier"] in {"free-conditional","free-self-hosted"} for s in rows))
        self.assertEqual(sum(s["access"]=="commercial-metered" for s in rows),sum(s["cost_tier"]=="commercial" for s in rows))
        for x in rows:
            self.assertIn(x["cost_tier"],self.api["cost_tiers"])

    def test_all_skills_paging_and_bilingual_cost_ui(self):
        for token in ('id="all-skills"','id="skillDirectory"','id="costFilter"',
                      'id="loadMoreBtn"','state.visibleLimit+=24',
                      'filtered.slice(0,state.visibleLimit)',
                      'installedSkills=m.skill_ids',
                      'state.cost==="free-only"',
                      'showMore:"عرض المزيد"',
                      'costLabel:"التكلفة والإتاحة"'):
            self.assertIn(token,self.html)
        self.assertNotIn("filtered.slice(0,60)",self.html)

    def test_terrain_skill_heading_repaired(self):
        text=(ROOT/"skills/terrain-hydrology-lidar/SKILL.md").read_text(encoding="utf-8")
        self.assertEqual(1,text.count("# Terrain, Hydrology & LiDAR"))
        self.assertNotIn("tiles.#",text)

    def test_embedded_site_js_parses_if_node_installed(self):
        node=shutil.which("node")
        if not node:
            self.skipTest("Node not installed; CI has a required Node syntax gate")
        scripts=re.findall(r"<script>(.*?)</script>",self.html,re.S)
        self.assertEqual(1,len(scripts))
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/"site.js"
            p.write_text(scripts[0],encoding="utf-8")
            result=subprocess.run([node,"--check",str(p)],capture_output=True,text=True,timeout=20)
        self.assertEqual(result.returncode,0,result.stderr)
