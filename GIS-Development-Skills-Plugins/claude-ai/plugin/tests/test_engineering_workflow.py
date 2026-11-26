"""Verify approval, output collisions and persisted workflow progression."""

from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import tempfile
import unittest

from scripts import engineering_workflow as workflow
from scripts import project_governance as governance


class LocalWorkflowTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        governance.init(self.root)
        (self.root / "testing data/points.json").write_text('{"count": 1}', encoding="utf-8")
        self.check = {"artifact": "facts.json", "comparison": "json", "expected": {"count": 1}}
        (self.root / "expected.json").write_text(json.dumps({"checks": [self.check]}), encoding="utf-8")
        created = governance.new_test_run(self.root, "Workflow", inputs=("points.json",), expect="expected.json")
        self.work = self.root / created["run"]

    def plan(self, dependencies=False):
        task = {
            "id": "A", "title": "Fixture", "description": "Count a synthetic input",
            "kind": "terrain", "priority": "must", "risk": "medium",
            "skills": ["terrain-hydrology-lidar", "gis-security-guardian"],
            "owner_skill": "terrain-hydrology-lidar", "depends_on": [],
            "acceptance_criteria": ["Reads the expected count."],
            "tools": [{"tool_id": "fixture", "side_effect": effect} for effect in ("read", "write")],
        }
        return {
            "schema_version": "1.0", "request_id": "WF-TEST", "revision": "r1",
            "language": "en", "status": "draft", "original_request": "Run a test",
            "approval": {"approved_by_user": False, "approved_revision": None, "high_risk_approved": False},
            "assumptions": [], "open_questions": [], "goal": "Demonstrate handoffs",
            "target": "Temporary fixture", "desired_outcomes": ["Produced output"],
            "success_criteria": ["Observed reread"],
            "tasks": [task, {**task, "id": "B", "depends_on": ["A"]}] if dependencies else [task],
        }

    def action(self):
        def execute(inputs, outputs):
            value = json.loads(inputs["points.json"].read_text(encoding="utf-8"))
            (outputs / "facts.json").write_text(json.dumps(value), encoding="utf-8")

        return workflow.BoundAction("fixture", ("points.json",), "count-a", (self.check,), execute)

    def test_plan_json_does_not_grant_capabilities(self):
        plan = self.plan()
        plan["status"] = "approved"
        plan["approval"].update(approved_by_user=True, approved_revision="r1")
        attempted = []
        controller = workflow.LocalWorkflow(plan, self.work, {"A": self.action()},
                                            lambda request: attempted.append(request) or False)
        with self.assertRaises(PermissionError):
            controller.run("A")
        self.assertEqual(attempted[0].effects, ("read", "write"))
        self.assertFalse((self.work / "WORKFLOW.json").exists())
        self.assertEqual(list((self.work / "outputs").iterdir()), [])

    def test_same_workspace_rejects_overlapping_artifact_ownership(self):
        action = self.action()
        with self.assertRaisesRegex(ValueError, "overlaps"):
            workflow.LocalWorkflow(self.plan(True), self.work,
                                   {"A": action, "B": replace(action, output_group="count-a/nested")},
                                   lambda request: True)

    def test_dependency_is_rechecked_and_revision_is_bound(self):
        plan = self.plan(True)
        action = self.action()
        actions = {"A": action, "B": replace(action, output_group="count-b")}
        controller = workflow.LocalWorkflow(plan, self.work, actions, lambda request: True)
        with self.assertRaisesRegex(ValueError, "required task artifacts"):
            controller.run("B")
        self.assertEqual(controller.run("A")["state"], "DONE")
        (self.work / "outputs/count-a/attempt-01/facts.json").write_text('{"count": 9}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "required task artifacts"):
            controller.run("B")
        revised = deepcopy(plan)
        revised["revision"] = "r2"
        controller = workflow.LocalWorkflow(revised, self.work, actions, lambda request: True)
        with self.assertRaisesRegex(ValueError, "changed plan"):
            controller.run("A", resume=True)

    def test_rollback_and_resume_retain_attempts_and_gis_scoping(self):
        plan = self.plan()
        actions = {"A": self.action()}
        controller = workflow.LocalWorkflow(plan, self.work, actions, lambda request: True)
        profile = controller.teams["A"]
        self.assertIn("gis", [role["id"] for role in profile["roles"]])
        self.assertNotIn("rendering", [role["id"] for role in profile["roles"]])
        self.assertEqual(controller.run("A")["state"], "DONE")
        self.assertEqual(controller.rollback("A")["state"], "REWORK")
        resumed = workflow.LocalWorkflow(plan, self.work, actions, lambda request: True)
        result = resumed.run("A", resume=True)
        self.assertEqual((result["state"], result["attempts"]), ("DONE", 2))
        self.assertIn("RESUMED", {entry["state"] for entry in result["events"]})
        self.assertTrue((self.work / "outputs/count-a/attempt-01/facts.json").is_file())
        self.assertTrue((self.work / "outputs/count-a/attempt-02/facts.json").is_file())


if __name__ == "__main__":
    unittest.main()
