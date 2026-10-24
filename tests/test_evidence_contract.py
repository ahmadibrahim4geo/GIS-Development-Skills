"""Evidence verification and agent decision route checks."""
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("evidence", ROOT / "scripts/validate_evidence.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.report = json.loads((ROOT / "templates/gis-acceptance.example.json").read_text(encoding="utf-8"))

    def test_example_is_complete(self):
        self.assertEqual(module.validate(self.report), [])

    def test_native_claim_requires_logs(self):
        self.report["evidence_tier"] = "T3"
        self.report["status"] = "pass"
        self.assertTrue(any("native" in x or "evidence_links" in x for x in module.validate(self.report)))

    def test_missing_fields(self):
        self.report.pop("target")
        self.assertIn("Missing field: target", module.validate(self.report))

    def test_unverified_result_cannot_pass(self):
        self.report["status"] = "pass"
        self.assertTrue(module.validate(self.report))

    def test_core_router_retains_all_full_guidance(self):
        router = (ROOT / "skills/gis-development/SKILL.md").read_text(encoding="utf-8")
        archived = (ROOT / "references/gis-development-full-guidance.md").read_text(encoding="utf-8")
        self.assertGreater(len(archived), 10000)
        self.assertLess(len(router), 5500)
        self.assertIn("references/gis-development-full-guidance.md", router)
        self.assertIn("references/agent-decision-tree.md", router)


if __name__ == "__main__":
    unittest.main()
