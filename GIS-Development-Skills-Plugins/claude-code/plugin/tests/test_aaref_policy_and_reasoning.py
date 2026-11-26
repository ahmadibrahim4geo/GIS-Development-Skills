"""Deterministic policy, reasoning, DoneProof, and journal tests for AAREF."""
from __future__ import annotations

import copy
import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


audit_mod = _load("audit_agent_policy", "scripts/audit_agent_policy.py")
router_mod = _load("intent_router", "scripts/intent_router.py")
doneproof_mod = _load("verify_completion", "scripts/verify_completion.py")
journal_mod = _load("development_journal", "scripts/development_journal.py")


class AAREFPolicyAndReasoningTests(unittest.TestCase):
    def test_audit_agent_policy_passes_repository(self):
        result = audit_mod.audit_policy(ROOT)
        self.assertEqual("PASS", result["status"], result["errors"])
        self.assertGreaterEqual(result["rule_count"], 25)
        self.assertGreaterEqual(result["skill_count"], 37)

    def test_audit_agent_policy_rejects_banned_link_and_broken_anchor(self):
        with tempfile.TemporaryDirectory() as tmp:
            troot = Path(tmp)
            (troot / "skills" / "prompt-intent-orchestrator").mkdir(parents=True)
            (troot / "skills" / "prompt-intent-orchestrator" / "SKILL.md").write_text("---\nname: prompt-intent-orchestrator\n---\n", encoding="utf-8")
            (troot / "references" / "agent-reasoning").mkdir(parents=True)
            (troot / "AGENTS.md").write_text("# Root\n\nSee [bad](plans/secret.md)\n", encoding="utf-8")
            (troot / "references" / "agent-reasoning" / "rule-registry.json").write_text(json.dumps({
                "rules": [{
                    "rule_id": "R1",
                    "canonical_source": "references/missing.md",
                    "agents_anchor": "#nonexistent",
                    "scope": "repo",
                    "trigger": "always",
                    "strength": "MUST",
                    "owner": "unknown-skill",
                    "enforcement": ["test"],
                    "evidence": ["ev"],
                    "test_ids": ["t1"],
                    "legacy_mapping": ["AGENTS.md:1"],
                }]
            }), encoding="utf-8")
            res = audit_mod.audit_policy(troot)
            self.assertEqual("FAIL", res["status"])
            joined = "\n".join(res["errors"])
            self.assertIn("plans/", joined)
            self.assertIn("unknown owner skill", joined)
            self.assertIn("missing heading anchor", joined)
            self.assertIn("canonical_source file does not exist", joined)

    def test_rule_migration_matrix_valid(self):
        matrix_path = ROOT / "plans" / "active" / "0008_Agent-Intelligence-AAREF" / "02_Rule_Migration_Matrix.json"
        data = json.loads(matrix_path.read_text(encoding="utf-8"))
        known = router_mod.available_skills()
        for rule in data["rules"]:
            self.assertIn(rule["owner"], known)
            target_file = rule["canonical_source"].split("#")[0]
            self.assertTrue((ROOT / target_file).is_file(), target_file)

    def test_adaptive_classifier_decouples_depth_and_impact(self):
        direct = router_mod.classify_reasoning_profile({"read_only": True, "complexity": "low"})
        self.assertEqual("L0", direct["reasoning_level"])
        self.assertEqual("I0", direct["impact_class"])
        self.assertFalse(direct["requires_plan_review"])

        tiny_destructive = router_mod.classify_reasoning_profile({
            "complexity": "low", "reversibility": "low", "external_effect": "high", "security_impact": "high"
        })
        self.assertEqual("I3", tiny_destructive["impact_class"])
        self.assertTrue(tiny_destructive["requires_high_impact_gate"])

        deep_readonly = router_mod.classify_reasoning_profile({
            "read_only": True, "complexity": "high", "uncertainty": "high", "scientific_impact": "high"
        })
        self.assertEqual("L5", deep_readonly["reasoning_level"])
        self.assertEqual("I0", deep_readonly["impact_class"])
        self.assertFalse(deep_readonly["requires_high_impact_gate"])

        forbidden = router_mod.classify_reasoning_profile({"unsupported_or_forbidden": True})
        self.assertEqual("I4", forbidden["impact_class"])
        self.assertTrue(forbidden["blocked"])

    def test_intent_router_aaref_plan_fields_and_gates(self):
        plan = json.loads((ROOT / "examples" / "intent-orchestrator" / "example-plan.json").read_text(encoding="utf-8"))
        plan["status"] = "approved"
        plan["approval"] = {"approved_by_user": True, "approved_revision": "r1", "high_risk_approved": False}
        plan["intent_revision"] = "r1"
        plan["reasoning_level"] = "L3"
        plan["impact_class"] = "I2"
        plan["material_unknowns"] = []
        plan["inferred_assumptions"] = ["Preserve source DEM elevation unchanged"]
        plan["decision_capsules"] = [{
            "decision_id": "DEC-1",
            "question": "Grid rendering decoupling",
            "selection": "Keep layer state isolated",
            "short_rationale": "Avoids coupling grid display to labels",
            "review_mode": "INDEPENDENT_AGENT",
        }]
        ok = router_mod.compile_workflow(plan, require_approved=True)
        self.assertTrue(ok["valid"], ok["errors"])
        self.assertEqual("L3", ok["reasoning_level"])
        self.assertEqual("I2", ok["impact_class"])
        self.assertFalse(ok["can_execute"])

        high_imp = copy.deepcopy(plan)
        high_imp["impact_class"] = "I3"
        self.assertFalse(router_mod.compile_workflow(high_imp, require_approved=True)["valid"])

        forb = copy.deepcopy(plan)
        forb["impact_class"] = "I4"
        self.assertFalse(router_mod.compile_workflow(forb, require_approved=True)["valid"])

    def test_doneproof_enforces_honest_review_mode(self):
        base = {
            "schema_version": "1.0",
            "task_id": "T1",
            "revision": "r1",
            "overall_status": "verified",
            "review_mode": "INDEPENDENT_AGENT",
            "criteria": [{
                "id": "C1",
                "statement": "Checked",
                "status": "verified",
                "evidence": [{"type": "artifact_readback", "reference": "x.log", "observed": "ok", "result": "pass", "revision": "r1"}],
            }],
        }
        self.assertTrue(doneproof_mod.validate(base))
        good = copy.deepcopy(base)
        good["independent_review_evidence"] = {"reviewer_subagent": "subagent-123", "report": "reports/review.md"}
        self.assertEqual([], doneproof_mod.validate(good))

        dishonest_self = copy.deepcopy(good)
        dishonest_self["review_mode"] = "SELF_REVIEW"
        self.assertTrue(doneproof_mod.validate(dishonest_self))

        vacuous_list = copy.deepcopy(base)
        vacuous_list["independent_review_evidence"] = ["", {}]
        self.assertTrue(doneproof_mod.validate(vacuous_list))

        contradictory_not_run = copy.deepcopy(good)
        contradictory_not_run["review_mode"] = "NOT_RUN"
        self.assertTrue(doneproof_mod.validate(contradictory_not_run))

    def test_journal_capsules_checkpoints_and_quarantined_lessons(self):
        with tempfile.TemporaryDirectory() as tmp:
            proj = Path(tmp)
            journal_mod.init(proj)
            cap = journal_mod.record_capsule(proj, {
                "decision_id": "DEC-001",
                "task_id": "T1",
                "question": "CRS reprojection vs Define Projection",
                "selection": "Use explicit Project transform",
                "short_rationale": "Preserves geometric accuracy",
                "review_mode": "INDEPENDENT_AGENT",
            })
            self.assertEqual("DEC-001", cap["decision_id"])

            cp = journal_mod.write_checkpoint(proj, {
                "task_id": "T1",
                "root": "proj",
                "head": "abc123",
                "intent_revision": "r1",
                "protected_inputs": ["testing data/"],
                "next_authorized_action": "Run validator",
            })
            self.assertEqual("r1", cp["intent_revision"])

            with self.assertRaises(ValueError):
                journal_mod.propose_lesson(proj, {
                    "lesson_id": "L-BAD",
                    "source_task": "T1",
                    "domain": "crs",
                    "observed_problem": "Leak sk-1234567890abcdef1234",
                    "verified_cause": "Secret exposed",
                    "evidence_refs": ["log"],
                })
            with self.assertRaises(ValueError):
                journal_mod.propose_lesson(proj, {
                    "lesson_id": "L-DIRECT-ACTIVE",
                    "source_task": "T1",
                    "domain": "crs",
                    "observed_problem": "Attempt direct active",
                    "verified_cause": "Bypass",
                    "review_state": "ACTIVE",
                    "evidence_refs": ["log"],
                })
            with self.assertRaises(ValueError):
                journal_mod.propose_lesson(proj, {
                    "lesson_id": "L-AUTO-MOD",
                    "source_task": "T1",
                    "domain": "policy",
                    "observed_problem": "Modify policy",
                    "verified_cause": "Rule gap",
                    "auto_modify_policy": True,
                    "evidence_refs": ["log"],
                })

            cand = journal_mod.propose_lesson(proj, {
                "lesson_id": "L-001",
                "source_task": "T1",
                "domain": "remote-sensing",
                "observed_problem": "Landsat C2 SR offset bias when divided raw",
                "verified_cause": "0.0000275 * DN - 0.2 requires unpacking before normalized ratio",
                "evidence_refs": ["reports/eval.json"],
            })
            self.assertEqual("CANDIDATE", cand["review_state"])
            with self.assertRaises(ValueError):
                journal_mod.propose_lesson(proj, {
                    "lesson_id": "L-JSON-KEY-SECRET",
                    "source_task": "T1",
                    "domain": "api",
                    "observed_problem": "JSON serialized key",
                    "verified_cause": "leak",
                    "api_key": "topsecretvalue123",
                    "evidence_refs": ["reports/eval.json"],
                })
            with self.assertRaises(ValueError):
                journal_mod.propose_lesson(proj, {
                    "lesson_id": "L-NESTED-AUTOMOD",
                    "source_task": "T1",
                    "domain": "policy",
                    "observed_problem": "nested auto mod",
                    "verified_cause": "nested",
                    "meta": {"auto_modify_policy": True},
                    "evidence_refs": ["reports/eval.json"],
                })
            with self.assertRaises(ValueError):
                journal_mod.promote_lesson(proj, "L-001", "ACTIVE", reviewer="self", review_mode="SELF_REVIEW")
            with self.assertRaises(ValueError):
                journal_mod.promote_lesson(proj, "L-001", "REVIEWED", reviewer="rev-1", review_mode="INDEPENDENT_AGENT")
            journal_mod.promote_lesson(
                proj, "L-001", "REVIEWED", reviewer="rev-1",
                review_mode="INDEPENDENT_AGENT", independent_review_evidence="subagent-8e25afd2",
            )
            with self.assertRaises(ValueError):
                journal_mod.promote_lesson(proj, "L-001", "VALIDATED", reviewer="self", review_mode="SELF_REVIEW")
            journal_mod.promote_lesson(
                proj, "L-001", "VALIDATED", reviewer="rev-1",
                review_mode="INDEPENDENT_AGENT", independent_review_evidence="subagent-8e25afd2",
            )
            active = journal_mod.promote_lesson(proj, "L-001", "ACTIVE", reviewer="human-owner", review_mode="HUMAN_REVIEW")
            self.assertEqual("ACTIVE", active["review_state"])
            journal_mod.verify(proj)

    def test_english_consistency_on_audited_technical_docs(self):
        ar_rx = re.compile(r"[\u0600-\u06FF]")
        english_only_files = (
            "AGENTS.md",
            "references/agent-reasoning/website-and-repo-contracts.md",
            "references/agent-reasoning/adaptive-controller.md",
            "references/agent-reasoning/cognitive-and-decision-methods.md",
            "references/agent-reasoning/scientific-gis-reasoning.md",
            "references/agent-reasoning/failure-recovery-and-learning.md",
            "references/agent-reasoning/model-host-adaptation.md",
            "references/portable-execution-guidance.md",
            "references/gis-software-source-registry.md",
            "references/build-vs-reuse-policy.md",
            "references/visual-asset-sources.md",
            "docs/VISUAL_ASSETS_INTEGRATION_2026-10-27.md",
            "docs/OPENGEOHUB_OPENLANDMAP_SYNCHRONIZATION_REPORT_2026-10-30.md",
            "docs/WEB_GIS_GUIDE.md",
            "docs/MOBILE_GIS_GUIDE.md",
        )
        for rel in english_only_files:
            with self.subTest(file=rel):
                text = (ROOT / rel).read_text(encoding="utf-8")
                self.assertIsNone(ar_rx.search(text), f"Unexpected Arabic text in English technical doc: {rel}")
        geo_text = (ROOT / "references/geocoding-place-search.md").read_text(encoding="utf-8")
        self.assertNotIn("ملاحظات بالعربية", geo_text)
        self.assertIn("Cairo/القاهرة", geo_text)


if __name__ == "__main__":
    unittest.main()
