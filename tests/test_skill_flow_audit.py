"""Read-only regression tests for specialist reachability and role integrity."""
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("skill_flow_audit", ROOT / "scripts/audit_skill_graph.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class SkillFlowAuditTests(unittest.TestCase):
    def test_all_discoverable_skills_are_routed(self):
        result = mod.audit(ROOT)
        self.assertTrue(result["valid"], result["issues"])
        manifest = json.loads((ROOT / "references/repository-manifest.json").read_text("utf-8"))
        self.assertEqual(result["skills"], manifest["skill_count"])
        self.assertEqual(result["lexical_domains"], result["skills"] - len(mod.SHARED))
        self.assertIn("completion-evidence", result["shared_owners"])
        self.assertIn("gis-data-flow-diagnostics", result["conditional_owners"])

    def copy_minimal_tree(self, root):
        for source in ("AGENTS.md", "references/repository-manifest.json",
                       "references/free-first-policy.md",
                       "references/repository-wide-skill-orchestration.md",
                       "scripts/intent_router.py",
                       "skills/gis-development/SKILL.md"):
            destination = root / source
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / source, destination)
        for path in (ROOT / "skills").glob("*/SKILL.md"):
            target = root / "skills" / path.parent.name / "SKILL.md"
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists():
                target.write_text("# Standalone test skill\n", encoding="utf-8")

    def test_missing_direct_specialist_route_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.copy_minimal_tree(root)
            router = root / "skills/gis-development/SKILL.md"
            router.write_text(router.read_text("utf-8").replace(
                "../gis-mobile-application-development/SKILL.md",
                "../gis-development/SKILL.md"), encoding="utf-8")
            errors = mod.audit(root)["issues"]
            self.assertTrue(any("Unreachable" in e and "gis-mobile" in e for e in errors), errors)

    def test_missing_license_policy_entry_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.copy_minimal_tree(root)
            policy = root / "references/free-first-policy.md"
            policy.write_text(policy.read_text("utf-8").replace(
                "| `completion-evidence` |", "| completion-evidence |"), encoding="utf-8")
            errors = mod.audit(root)["issues"]
            self.assertTrue(any("Missing free-first policy entry: completion-evidence" in e
                                for e in errors), errors)

    def test_missing_prompt_hints_detected_without_executing_tools(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.copy_minimal_tree(root)
            hints = root / "scripts/intent_router.py"
            hints.write_text(hints.read_text("utf-8").replace(
                '("gis-mobile-application-development", (',
                '("broken-mobile-application-development", ('), encoding="utf-8")
            errors = mod.audit(root)["issues"]
            self.assertTrue(any("missing lexical route hints: gis-mobile" in e
                                for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
