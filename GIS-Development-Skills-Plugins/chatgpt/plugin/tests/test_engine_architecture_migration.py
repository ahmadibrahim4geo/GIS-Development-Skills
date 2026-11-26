"""Tests for P01 Engine V2 taxonomy, v1/v2 architecture schema compat, and root agent wiring."""
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class EngineArchitectureP01Tests(unittest.TestCase):
    def test_v1_flow_fixture_backward_compatibility_E23(self):
        """E23: Existing v1 architecture flow fixture remains valid after v2 additions."""
        validator = load_module("validate_architecture_flow")
        flow = json.loads(
            (ROOT / "examples/architecture-visualization/qgis-ribbon.flow.json").read_text(encoding="utf-8")
        )
        errors = validator.validate_flow(flow)
        self.assertEqual([], errors)

    def test_v2_schema_and_taxonomy_integrity(self):
        schema_path = ROOT / "schemas" / "architecture-v2.schema.json"
        self.assertTrue(schema_path.is_file())
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertEqual("2.0", schema["properties"]["schema_version"]["const"])
        for req_field in (
            "schema_version",
            "intent",
            "source_host",
            "target_host",
            "ui",
            "components",
            "capability_requirements",
            "preserved_invariants",
            "license_policy",
        ):
            self.assertIn(req_field, schema["required"])

        taxonomy = json.loads((ROOT / "references" / "engine-capability-taxonomy.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(taxonomy["domains"]), 11)
        self.assertGreaterEqual(len(taxonomy["capability_support_states"]), 7)
        self.assertGreaterEqual(len(taxonomy["claim_confidence_grades"]), 7)
        self.assertGreaterEqual(len(taxonomy["bilingual_synonyms"]), 7)

        arch_doc = (ROOT / "references" / "engine-architecture-taxonomy.md").read_text(encoding="utf-8")
        self.assertIn("UI.js", arch_doc)
        self.assertIn("unresolved", arch_doc)
        self.assertIn("reference-inspired-ui", arch_doc)
        self.assertIn("multi-engine-composition", arch_doc)

    def test_root_agents_policy_wired_and_references_exist(self):
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        for token in (
            "Discover Before Building",
            "Reuse Before Reinventing",
            "engine-architecture-taxonomy.md",
            "engine-capability-taxonomy.json",
            "build-vs-reuse-policy.md",
            "Mandatory Plugin Lifecycle Policy",
            "plans/active/0007_Master-Integration/MASTER_AGENT_PROMPT.md",
        ):
            self.assertIn(token, agents)
        self.assertNotIn("](plans/", agents, "AGENTS.md is bundled into ZIP and must not use markdown links to plans/")


if __name__ == "__main__":
    unittest.main()
