# Plan 0008: Adaptive Agent Reasoning & Engineering Framework (AAREF)

- **Plan ID:** `0008_Agent-Intelligence-AAREF`
- **Status:** `APPROVED` (Authorized by user `"اوك"` in live host session `2026-11-26`)
- **Revision:** `rev-1`
- **Target Scope:** `d:\My Software\Skills\GIS Development Skills`
- **Master Specification:** `D:\My Software\Skills\GIS_AGENT_INTELLIGENCE_MASTER_DEVELOPMENT_PLAN.md`
- **Baseline Audit:** `reports/AR00_BASELINE_AUDIT.md` (Git `HEAD 7c0eb7da`, `AGENTS.md` SHA-256 `6dd2c9fadc5f9a9e322cb87455b8bcd3b2dbe4f5dd7e70201d1e04524f6beb67`)
- **Compatibility Contract:** Preserves `plans/active/0007_Master-Integration/` (`P00–P11`), all 37 skills, Brand Kit 3.1, `#author` panel, verbatim English mission sentence, bilingual user guides, and 7-platform plugin adapters.

## 1. Architectural Decisions Summary

1. **Extend Existing Owners (Zero Skill Bloat):** Keep 37 canonical skills; embed AAREF capabilities into `AGENTS.md`, `prompt-intent-orchestrator`, `gis-development`, `gis-security-guardian`, `completion-evidence`, `agent-development-journal`, and GIS domain specialists, backed by consolidated English technical guides in `references/agent-reasoning/`.
2. **Progressive Disclosure in `AGENTS.md`:** Streamline `AGENTS.md` into an authoritative English constitution retaining every test-enforced invariant (`## Start here`, `Discover Before Building`, `Reuse Before Reinventing`, taxonomy/policy references, `Mandatory Plugin Lifecycle Policy`, `plans/active/0007_Master-Integration/MASTER_AGENT_PROMPT.md` with zero markdown links pointing to `plans/`), indexed via `references/agent-reasoning/rule-registry.json`, with website/Brand Kit markup rules cleanly referenced in `references/agent-reasoning/website-and-repo-contracts.md`.
3. **Decoupled Adaptive Reasoning (`L0–L5`) & Impact Gating (`I0–I4`):** Extend `scripts/intent_router.py` cleanly with `L0–L5` workflow depth, `I0–I4` independent authorization risk gates, `intent_revision`, `material_unknowns`, `inferred_assumptions`, and method selection without relaxing existing approval gates or falsely claiming natural-language comprehension in offline Python.
4. **Scientific Integrity, Failure Recovery, & Honest Review Attribution:** Enforce `review_mode` validation in `scripts/verify_completion.py`, Decision Capsules + Checkpoints + Quarantined/Sanitized Lessons (`CANDIDATE -> REVIEWED -> VALIDATED -> ACTIVE -> SUPERSEDED/REJECTED`) in `scripts/development_journal.py`, and repeated-failure replanning rules without auto-editing policy files.
5. **Strict English Technical Consistency:** Author all central rules, schemas, scripts, AAREF references, and technical reports in English; convert non-test Arabic prose in audited technical references/docs to English while keeping bilingual EN/AR user guides (`README*.md`, `HOW_TO_USE*.md`, website UI) and test-asserted Arabic keywords intact.
6. **Empirical GAIB Evaluation + Independent Review + 7-Platform Plugin Rebuild:** Run isolated before (`A`, `B`) vs after (`C`) evaluations, pass an isolated `INDEPENDENT_AGENT` review gate, fix `PortableAdapter` (`description` + `icon`) and unified credit (`"The Heart of Geospatial Innovation — By Ahmed Ibrahim"`), and rebuild all 7 plugins via `Update-All-Plugins.ps1 -BuildOnly`.

## 2. Phase Roadmap (`AR00–AR10`)

| Phase | Deliverable | Owner | Gate / Exit Evidence |
|---|---|---|---|
| `AR00` | Baseline audit, HEAD/hash lock, existing tests, Conditions A & B evals | `agent-development-journal` | `reports/AR00_BASELINE_AUDIT.md`, `reports/gaib/baseline_A.json`, `baseline_B.json`, journal `#0125-#0126` |
| `AR01` | Rule migration matrix, ADR-0008, `rule-registry.json`, refactored `AGENTS.md`, `website-and-repo-contracts.md` | `prompt-intent-orchestrator` | `plans/active/0008_.../02_Rule_Migration_Matrix.json`, `03_ADR_AAREF_Architecture.md`, `04_Reviewed_Plan.json`, `audit_agent_policy.py` |
| `AR02–AR03` | `L0–L5` adaptive controller, `I0–I4` impact gate, hypotheses/alternatives/failure recovery in `intent_router.py` & `prompt-intent-orchestrator` | `prompt-intent-orchestrator` | Backwards-compatible CLI + new unit tests (`test_aaref_policy_and_reasoning.py`) |
| `AR04–AR05` | Scientific GIS invariants, router/orchestration state machine, Security Guardian trust decoupling, DoneProof `review_mode`, domain skill links | `gis-development`, `gis-security-guardian`, `completion-evidence` | Domain scientific checks, graph reachability PASS, `verify_completion.py` unit tests |
| `AR06` | Decision Capsules, compact Checkpoints, quarantined & sanitized Lessons store + `token-optimization-triad.md` update | `agent-development-journal` | Secret redaction / quarantine / anti-self-modification tests |
| `AR07` | Deterministic policy/graph/security/English-doc checks + comprehensive unit suite | `completion-evidence` | `audit_agent_policy.py`, `validate_skill_pack.py`, `audit_skill_graph.py`, `security_audit.py`, full `unittest` |
| `AR08` | GAIB Pilot + Holdout (`evaluate_agent.py`) + Condition `C` subagent + A vs B vs C comparison | `completion-evidence` | `reports/gaib/AR08_GAIB_REPORT.md` & `.json` |
| `AR08.5` | Isolated `INDEPENDENT_AGENT` review of spec, migration matrix, and git diffs; remediate findings | Isolated Reviewer Subagent | Severity-ranked findings report + post-fix re-test |
| `AR09` | `PortableAdapter` + credit alignment + 7-platform rebuild (`Update-All-Plugins.ps1 -BuildOnly`) + docs/manifest/CHANGELOG sync | `completion-evidence` | `pipeline.py --check-only` `UP_TO_DATE` (`exit_code=0`), `build_manifest.py --check` |
| `AR10` | Final validators, full test re-run, DoneProof plan-bound verification, journal closure, Arabic final summary | `completion-evidence` | `verify_completion.py --plan ... --require-verified`, honest `NOT RUN` native boundary |
