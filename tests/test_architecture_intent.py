"""Offline counterexamples for architecture intent and flow contract loss.

These tests neither interpret arbitrary language nor operate a real GIS UI.
"""
import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name + ".py"))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


router = module("intent_router")
flows = module("validate_architecture_flow")


class ArchitectureIntentTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((ROOT / "examples/architecture-visualization/qgis-ribbon.plan.json").read_text("utf-8"))
        self.task = self.plan["tasks"][1]
        self.flow = json.loads((ROOT / "examples/architecture-visualization/qgis-ribbon.flow.json").read_text("utf-8"))

    def test_ribbon_and_uijs_requests_reach_architectural_review(self):
        for prompt in ("حوّل واجهة QGIS إلى ribbon مع الحفاظ على الأدوات",
                       "حوّل أدوات QGIS إلى ribbon واربطها بمحرك واجهة UI.js",
                       "اعمل Ribbon في QGIS من غير تغيير المحرك",
                       "Build a standalone QGIS app with UI.js ribbon"):
            with self.subTest(prompt=prompt):
                result = router.route_hints(prompt)
                self.assertTrue(result["architecture_review"]["required"])
                self.assertIn("prompt-intent-orchestrator", result["suggested_skills"])
                self.assertEqual("unresolved", result["architecture_review"]["delivery_model"])
                self.assertIsNone(result["goal"])
                self.assertTrue(result["requires_semantic_review"])
                self.assertNotIn("qgis-plugin-development", result["suggested_skills"])

    def test_small_label_change_does_not_force_architecture(self):
        for prompt in ("Change one button label and color", "غيّر اسم الزر ولونه", "Change ribbon button color", "غيّر لون زر ribbon"):
            self.assertFalse(router.route_hints(prompt)["architecture_review"]["required"])

    def test_processing_backend_is_not_assumed_to_be_hosted_plugin(self):
        hints = router.route_hints("Explain the data flow from UI.js ribbon to QGIS processing and map refresh")
        self.assertTrue(hints["architecture_review"]["required"])
        self.assertNotIn("qgis-plugin-development", hints["suggested_skills"])
        self.assertIn("gis-data-flow-diagnostics", hints["suggested_skills"])

    def test_contract_roundtrip_preserves_invariants_and_correlation(self):
        self.task.update(command_id="sample.buffer", trace_id="fixture-only-not-observed",
                         input_schema={"type": "object"}, output_schema="schemas/result.json",
                         input_contract={"dataset_id": "opaque"}, output_contract="new-output-only",
                         input_artifact_id="input-fixture", output_artifact_id="output-fixture",
                         handoff_contracts=[{"from_task": "R1", "contract_ref": "examples/architecture-visualization/qgis-ribbon.flow.json"}])
        original = copy.deepcopy(self.plan)
        result = router.compile_workflow(self.plan)
        self.assertTrue(result["valid"], result["errors"])
        for key in ("constraints", "non_goals", "assumptions", "open_questions"):
            self.assertEqual(self.plan[key], result[key])
        step = result["steps"][1]
        self.assertEqual(self.task["description"], step["description"])
        for key in (*router.TASK_CONTRACT_FIELDS, "architecture"):
            self.assertEqual(self.task[key], step[key])
        self.assertEqual(self.task["architecture"]["flow_spec_ref"], step["visualization"]["flow_spec_ref"])
        self.assertEqual("task_dependency", result["handoffs"][0]["kind"])
        self.assertEqual(self.task["handoff_contracts"][0]["contract_ref"], result["handoffs"][0]["contract_ref"])
        self.assertNotIn("data_contract", result["handoffs"][0])
        step["architecture"]["preserved_invariants"].append("changed-preview-only")
        self.assertEqual(original, self.plan)
        self.assertFalse(result["can_execute"])
        self.assertFalse(step["visualization"]["gis_execution_proven"])

    def test_unknown_uijs_identity_is_preserved_and_blocks_implementation_readiness(self):
        self.task["architecture"]["ui_framework"]["name"] = "UI.js"
        result = router.compile_workflow(self.plan)
        self.assertTrue(result["valid"], result["errors"])
        step = result["steps"][1]
        self.assertEqual("UI.js", step["architecture"]["ui_framework"]["name"])
        self.assertEqual("NEEDS_DISCOVERY", step["architecture_status"])
        self.assertTrue(any("ui_framework" in s for s in step["architecture_blockers"]))
        self.assertFalse(result["host_permissions_verified"])
        self.assertFalse(result["can_execute"])

    def test_invalid_identity_role_status_and_local_refs_fail(self):
        for key, value in (("flow_spec_ref", "../outside.json"), ("flow_spec_ref", "https://example.org/flow"),
                           ("command_inventory_ref", "C:/outside.json"), ("flow_spec_ref", "."),
                           ("change_type", []), ("preserved_invariants", []), ("integration_mode", "automatic")):
            plan = copy.deepcopy(self.plan)
            plan["tasks"][1]["architecture"][key] = value
            self.assertFalse(router.compile_workflow(plan)["valid"], (key, value))
        for field, value in (("role", "geospatial-engine"), ("status", "runtime-verified"),
                             ("status", "source-reviewed")):
            plan = copy.deepcopy(self.plan)
            plan["tasks"][1]["architecture"]["ui_framework"][field] = value
            self.assertFalse(router.compile_workflow(plan)["valid"], (field, value))

    def test_reviewed_identities_still_require_native_preflight(self):
        arch = self.task["architecture"]
        for role in router.ARCHITECTURE_ROLES:
            arch[role].update(status="source-reviewed", source_ref="reviewed-source@fixture", version="fixture-1")
        arch.update(source_host="Fixture QGIS host", target_host="Same fixture QGIS host")
        arch["command_inventory_ref"] = "examples/architecture-visualization/qgis-ribbon.flow.json"
        result = router.compile_workflow(self.plan)
        self.assertEqual("REQUIRES_PREFLIGHT", result["steps"][1]["architecture_status"])
        self.assertFalse(result["can_execute"])
        arch["target_host"] = "Unresolved target host"
        self.assertEqual("NEEDS_DISCOVERY", router.compile_workflow(self.plan)["steps"][1]["architecture_status"])

    def test_invalid_declared_handoff_cannot_silently_disappear(self):
        for value in ([{"from_task": "missing", "contract_ref": "flow.json"}],
                      [{"from_task": "R1", "contract_ref": "../flow.json"}], "not-an-array"):
            self.task["handoff_contracts"] = value
            self.assertFalse(router.compile_workflow(self.plan)["valid"])

    def test_legacy_abstract_and_nonarchitectural_plans_remain_compatible(self):
        for fixture in ("examples/intent-orchestrator/example-plan.json",
                        "examples/architecture-visualization/plan.example.json"):
            plan = json.loads((ROOT / fixture).read_text("utf-8"))
            result = router.compile_workflow(plan)
            self.assertTrue(result["valid"], result["errors"])
            self.assertTrue(all("architecture" not in step for step in result["steps"]))

    def test_proposed_flow_is_consistent_but_never_runtime_proof(self):
        self.assertEqual([], flows.validate_flow(self.flow))
        self.assertTrue(all(e["evidence_basis"] == "proposed" and e["source_ref"] is None for e in self.flow["edges"]))

    def test_flow_requires_connected_result_error_and_state_paths(self):
        for kind in ("result", "error", "state"):
            flow = copy.deepcopy(self.flow)
            flow["edges"] = [e for e in flow["edges"] if e["kind"] != kind]
            self.assertTrue(flows.validate_flow(flow), kind)
        flow = copy.deepcopy(self.flow)
        # A disconnected result elsewhere cannot stand in for the engine return.
        flow["edges"] = [e for e in flow["edges"] if e["id"] != "engine-result"]
        self.assertTrue(any("result return path" in e for e in flows.validate_flow(flow)))

    def test_detached_state_edge_cannot_stand_in_for_ui_update(self):
        self.flow["nodes"].extend([{"id": "detached-a", "role": "unrelated"}, {"id": "detached-b", "role": "unrelated"}])
        self.flow["edges"] = [edge for edge in self.flow["edges"] if edge["kind"] != "state"]
        self.flow["edges"].append({**self.flow["edges"][0], "id": "direct-result", "from": "gis-engine", "to": "ribbon-ui", "kind": "result"})
        self.flow["edges"].append({**self.flow["edges"][0], "id": "unrelated-state", "from": "detached-a", "to": "detached-b", "kind": "state"})
        self.assertTrue(any("connected UI/map state" in e for e in flows.validate_flow(self.flow)))

    def test_migration_requires_complete_declared_source_mapping(self):
        for modify in (lambda f: f.pop("source_commands"),
                       lambda f: f["source_commands"].append("unmapped-existing-command"),
                       lambda f: f["command_mappings"][0].update(after="")):
            flow = copy.deepcopy(self.flow)
            modify(flow)
            self.assertTrue(flows.validate_flow(flow))

    def test_async_policy_and_thread_ownership_are_explicit(self):
        flow = copy.deepcopy(self.flow)
        del flow["async_policy"]["cancellation"]
        self.assertTrue(flows.validate_flow(flow))
        flow = copy.deepcopy(self.flow)
        flow["edges"][0]["thread_owner"] = ""
        self.assertTrue(flows.validate_flow(flow))

    def test_preserved_mapping_cannot_omit_its_command_flow(self):
        for edge in self.flow["edges"]:
            edge["command_id"] = None
        self.assertTrue(any("correlated request flow" in e for e in flows.validate_flow(self.flow)))

    def test_flow_evidence_is_per_edge_and_unattributed_observed_claim_fails(self):
        self.flow["edges"][0].update(evidence_basis="source-reviewed", source_ref="source.py:10@fixture")
        self.assertEqual([], flows.validate_flow(self.flow))
        self.assertEqual("proposed", self.flow["edges"][1]["evidence_basis"])
        self.flow["edges"][1]["evidence_basis"] = "runtime-observed"
        self.assertTrue(flows.validate_flow(self.flow))

    def test_persistence_requires_connected_readback(self):
        self.flow["persistence_required"] = True
        self.assertTrue(flows.validate_flow(self.flow))
        prototype = self.flow["edges"][0]
        self.flow["nodes"].extend([{"id": "output", "role": "persisted artifact"}, {"id": "reader", "role": "independent reader"}])
        self.flow["edges"].extend([
            {**prototype, "id": "save", "from": "map-canvas", "to": "output", "kind": "persist"},
            {**prototype, "id": "reopen", "from": "output", "to": "reader", "kind": "readback"}])
        self.assertEqual([], flows.validate_flow(self.flow))
        self.flow["edges"][-1]["from"] = "ribbon-ui"
        self.assertTrue(flows.validate_flow(self.flow))

    def test_duplicate_ids_unknown_fields_and_dangling_nodes_fail(self):
        for mutate in (lambda f: f["edges"].append(copy.deepcopy(f["edges"][0])),
                       lambda f: f["edges"][0].update(to="not-a-node"),
                       lambda f: f["edges"][0].update(runtime_verified=True)):
            flow = copy.deepcopy(self.flow)
            mutate(flow)
            self.assertTrue(flows.validate_flow(flow))

    def test_flow_cli_and_draft_gate_never_execute(self):
        flow = subprocess.run([sys.executable, "-X", "utf8", "-B", "scripts/validate_architecture_flow.py",
                               "examples/architecture-visualization/qgis-ribbon.flow.json"],
                              cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(0, flow.returncode, flow.stdout + flow.stderr)
        blocked = subprocess.run([sys.executable, "-X", "utf8", "-B", "scripts/intent_router.py", "--plan",
                                  "examples/architecture-visualization/qgis-ribbon.plan.json", "--workflow", "--gate", "--format", "json"],
                                 cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(1, blocked.returncode, blocked.stderr)
        self.assertFalse(json.loads(blocked.stdout)["can_execute"])


if __name__ == "__main__":
    unittest.main()
