#!/usr/bin/env python3
"""P08 Repo-Wide Integration tests (routing, bilingual web UIs, roles, Archify, 0006 archive)."""

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class P08RepoIntegrationTests(unittest.TestCase):
    """Validates P08 wiring across router, web hubs, role registry, and archived 0006 plan."""

    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("intent_router", ROOT / "scripts" / "intent_router.py")
        cls.router = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.router)

    def test_colloquial_arabic_english_engine_routing_and_e31_lightweight_guard(self):
        heavy_prompts = (
            "عايز واجهة زي ArcGIS Pro وبرنامج مستقل",
            "خد QGIS ونضفه وسيب تحرير الطبقات",
            "صمملي برنامج خفيف لتحويل إحداثيات فقط",
            "engine replacement using existing program source",
        )
        for p in heavy_prompts:
            hints = self.router.route_hints(p)
            self.assertIn("geospatial-engine-selection", hints["suggested_skills"], p)

        # E31: isolated style/label edit stays lightweight
        light = self.router.route_hints("Change button label color to blue")
        self.assertFalse(light["architecture_review"]["required"])
        self.assertNotIn("geospatial-engine-selection", light["suggested_skills"])

    def test_v2_roles_and_archify_validation_contract_linked(self):
        reg = json.loads((ROOT / "references" / "engineering-role-registry.json").read_text(encoding="utf-8"))
        role_ids = {r["id"] for r in reg["roles"]}
        for rid in ("engine-selector", "clean-room-reviewer", "license-auditor"):
            self.assertIn(rid, role_ids)
        self.assertIn("V2_ARCHITECTURE", reg["profiles"])

        wf = (ROOT / "references" / "engineering-role-workflow.md").read_text(encoding="utf-8")
        self.assertIn("SEQUENTIAL_ROLE_SIMULATION", wf)

        arch = (ROOT / "skills" / "gis-architecture-visualization" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("validate_architecture_flow.py", arch)

    def test_explorer_wizard_and_homepage_expose_p08_integration(self):
        explorer = (ROOT / "explorer.html").read_text(encoding="utf-8")
        wizard = (ROOT / "project-wizard.html").read_text(encoding="utf-8")
        home = (ROOT / "index.html").read_text(encoding="utf-8")

        for token in (
            'id="roleFilter"',
            'id="evidenceFilter"',
            "engine-capability-profiles.json",
            "reference-only",
            "verified-for-target",
            "geospatial-engine-selection",
            "WEB_GIS_GUIDE.md",
            "MOBILE_GIS_GUIDE.md",
        ):
            self.assertIn(token, explorer)

        self.assertIn('value="engine-selection"', wizard)
        self.assertIn("reference-only", wizard)
        self.assertIn('value="geospatial-engine-selection"', home)
        self.assertIn("docs/MOBILE_GIS_GUIDE.md", home)
        self.assertIn("docs/WEB_MOBILE_GUIDE.ar.md", home)

    def test_0006_plan_archived_with_cross_references(self):
        self.assertFalse((ROOT / "plans" / "active" / "0006_Mobile-and-Web-GIS-Expansion").exists())
        arch_dir = ROOT / "plans" / "archive" / "0006_Mobile-and-Web-GIS-Expansion"
        self.assertTrue(arch_dir.is_dir())
        status = json.loads((arch_dir / "STATUS.json").read_text(encoding="utf-8"))
        self.assertEqual("ARCHIVED_ABSORBED_BY_0007", status["status"])
        self.assertEqual("P08", status["archived_in_phase"])


if __name__ == "__main__":
    unittest.main()
