"""Regression checks for intent ownership, routing and DoneProof plan binding.

These test offline structure and deliberate rejection, not real host execution.
"""
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


intent = load("intent_release", "intent_router.py")
proof = load("doneproof_release", "verify_completion.py")


class ReleaseGateTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((ROOT / "examples/intent-orchestrator/example-plan.json").read_text("utf-8"))
        task = self.plan["tasks"][0]
        self.report = {
            "schema_version": "1.0", "request_id": self.plan["request_id"],
            "task_id": task["id"], "revision": self.plan["revision"],
            "overall_status": "verified",
            "criteria": [{
                "id": "C{}".format(n + 1), "statement": criterion, "status": "verified",
                "evidence": [{
                    "type": "artifact_readback", "reference": "TEST_ONLY/observation-{}".format(n),
                    "observed": "Synthetic observation, NOT runtime proof", "result": "pass",
                    "revision": self.plan["revision"]
                }]
            } for n, criterion in enumerate(task["acceptance_criteria"])]
        }

    def test_mobile_and_permission_intent_hints_reachable(self):
        hints = intent.route_hints("Build Android mobile GIS with offline sync and GNSS")
        self.assertIn("gis-mobile-application-development", hints["suggested_skills"])
        self.assertIn("gis-security-guardian", hints["suggested_skills"])
        hints = intent.route_hints("صلاحيات الجهاز والبلوتوث")
        self.assertIn("system-capabilities-and-permissions", hints["suggested_skills"])

    def test_unhashable_inputs_return_errors_not_exceptions(self):
        cases = [
            ("status", [], "status must"),
            ("tasks", [], "tasks must"),
        ]
        for field, value, token in cases:
            with self.subTest(field=field):
                draft = copy.deepcopy(self.plan)
                draft[field] = value
                self.assertTrue(any(token in e for e in intent.validate_plan(draft)))
        draft = copy.deepcopy(self.plan)
        draft["tasks"][0]["risk"] = []
        self.assertTrue(any("risk" in e for e in intent.validate_plan(draft)))
        draft = copy.deepcopy(self.plan)
        draft["tasks"][0]["tools"] = [{"tool_id": "host.test", "side_effect": []}]
        self.assertTrue(any("side_effect" in e for e in intent.validate_plan(draft)))

    def test_domain_owner_cannot_be_silently_inferred(self):
        draft = copy.deepcopy(self.plan)
        draft["tasks"][0].pop("owner_skill")
        workflow = intent.compile_workflow(draft)
        self.assertFalse(workflow["valid"])
        self.assertIn("owner_skill", " ".join(workflow["errors"]))
        draft["tasks"][0]["owner_skill"] = "completion-evidence"
        draft["tasks"][0]["skills"].append("completion-evidence")
        self.assertFalse(intent.compile_workflow(draft)["valid"])

    def test_workflow_lists_completion_and_journal_owners(self):
        workflow = intent.compile_workflow(self.plan)
        self.assertTrue(workflow["valid"], workflow["errors"])
        for step in workflow["steps"]:
            self.assertEqual("agent-development-journal", step["journal_owner"])
            self.assertIn("completion-evidence", step["completion_gate"])

    def test_strict_plan_binding_succeeds_on_full_matching_criteria(self):
        self.assertEqual([], proof.validate(self.report))
        self.assertEqual([], proof.validate_against_plan(self.report, self.plan))

    def test_omitted_or_rewritten_criterion_rejected(self):
        altered = copy.deepcopy(self.report)
        altered["criteria"].pop()
        altered["overall_status"] = "verified"
        self.assertTrue(proof.validate_against_plan(altered, self.plan))
        altered = copy.deepcopy(self.report)
        altered["criteria"][0]["statement"] = "We ran a unit test"
        self.assertTrue(proof.validate_against_plan(altered, self.plan))

    def test_wrong_revision_request_and_task_rejected(self):
        for field, value in (("revision", "r0"), ("request_id", "OTHER"), ("task_id", "UNKNOWN")):
            with self.subTest(field=field):
                changed = copy.deepcopy(self.report)
                changed[field] = value
                self.assertTrue(proof.validate_against_plan(changed, self.plan))

    def test_status_consistency_requires_realistic_summary(self):
        self.report["overall_status"] = "partial"
        self.assertTrue(any("overall_status" in e for e in proof.validate(self.report)))
        self.report["overall_status"] = "verified"
        self.report["criteria"][0]["status"] = "blocked"
        self.report["criteria"][0]["reason"] = "No host"
        self.assertTrue(proof.validate(self.report))

    def test_release_cli_rejects_unbound_verified_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "report.json"
            plan = Path(tmp) / "plan.json"
            report.write_text(json.dumps(self.report), encoding="utf-8")
            plan.write_text(json.dumps(self.plan), encoding="utf-8")
            cmd = [sys.executable, str(ROOT / "scripts/verify_completion.py"), str(report),
                   "--require-verified"]
            unbound = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            self.assertNotEqual(0, unbound.returncode)
            bound = subprocess.run(cmd + ["--plan", str(plan)], capture_output=True, text=True, timeout=15)
            self.assertEqual(0, bound.returncode, bound.stdout + bound.stderr)

    def test_duplicate_json_keys_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text('{"task_id":"one","task_id":"two"}', encoding="utf-8")
            with self.assertRaises(ValueError):
                proof.read_json(bad)


if __name__ == "__main__":
    unittest.main()
