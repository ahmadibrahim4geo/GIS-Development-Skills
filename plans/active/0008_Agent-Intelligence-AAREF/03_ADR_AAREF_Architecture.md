# ADR-0008: Adaptive Agent Reasoning & Engineering Framework (AAREF) Architecture

- **Status:** Approved within Plan `0008` (`2026-11-26`)
- **Authors:** Repository Architecture & Agent Intelligence Execution Team
- **Canonical Plan:** `plans/active/0008_Agent-Intelligence-AAREF/01_AAREF_Master_Plan.md`
- **Master Reference:** `D:\My Software\Skills\GIS_AGENT_INTELLIGENCE_MASTER_DEVELOPMENT_PLAN.md`

## 1. Context

Audit `AR00` (`reports/AR00_BASELINE_AUDIT.md`) confirmed that `AGENTS.md` (125 lines, 22.9 KB) and the 37 existing skills already establish strong goal-first intake (`prompt-intent-orchestrator`), single skill routing (`gis-development`), shared safety (`gis-security-guardian`), hash-chained project history (`agent-development-journal`), DoneProof (`completion-evidence`), and Master Integration V2 (`0007`) with plugin lifecycle packaging (`plugin-system/`). However, four structural limitations exist:

1. **Constitution Density & Duplication:** `AGENTS.md` mixes evergreen behavioral rules, website HTML markup rules, Brand Kit 3.1 layout notes, and plugin lifecycle procedures in repetitive prose without an explicit machine-auditable rule registry.
2. **Coupled Reasoning Depth vs. Authorization Risk:** Existing gating uses coarse `consequential` vs non-consequential categories rather than separating analytical depth (`L0 Direct` through `L5 Research`) from independent impact/authorization gating (`I0 Information` through `I4 Forbidden`).
3. **Cognitive & Scientific Method Fragmentation:** Systematic root-cause recovery (`replan` after repeated identical errors), scientific GIS verification invariants, review-mode truthfulness (`INDEPENDENT_AGENT` vs `SELF_REVIEW` / `NOT_RUN`), Decision Capsules, and sanitized lesson promotion exist only partially across prose documents rather than structured schemas and validators.
4. **English Technical Inconsistency & Plugin Metadata Drift:** Technical documents (`references/portable-execution-guidance.md`, `references/gis-software-source-registry.md`, `docs/OPENGEOHUB_OPENLANDMAP_SYNCHRONIZATION_REPORT_2026-10-30.md`, etc.) still contain inline Arabic sections, and manual pre-session edits in `GIS-Development-Skills-Plugins/` left `plugin-system/core/pipeline.py --check-only` in `VALIDATION_FAILED` while `PortableAdapter` omitted `icon` and `description`.

## 2. Decisions

1. **Zero New Redundant Skill (Preserve 37 Canonical Skills):** Do **not** add a 38th skill (`agent-reasoning-orchestration`) because `prompt-intent-orchestrator` (intake/planning), `gis-development` (general router), `gis-security-guardian` (impact/trust boundaries), `completion-evidence` (DoneProof/review truthfulness), and `agent-development-journal` (history/memory/lessons) already own every required lifecycle boundary cleanly.
2. **Progressive Disclosure in `AGENTS.md` + Consolidated `references/agent-reasoning/`:** Refactor `AGENTS.md` in crisp English with clear hierarchy (`Non-Negotiable Principles`, `Instruction Priority & Trust`, `Start Here`, `Adaptive Reasoning & Decision Flow`, `GIS Scientific Invariants`, `Orchestration, Review & Memory`, `Verification & DoneProof`, `Repository, Website & Plan 0007 Contracts`, `Mandatory Plugin Lifecycle Policy`) while offloading dense website/brand markup checklists to `references/agent-reasoning/website-and-repo-contracts.md` and indexing all rules in `references/agent-reasoning/rule-registry.json`. Preserve **every** verbatim token and prohibition (zero markdown links into `plans/`) required by existing regression tests (`tests/test_engine_architecture_migration.py`, `scripts/audit_skill_graph.py`, `tests/test_skill_distribution.py`).
3. **Decoupled `L0–L5` Depth and `I0–I4` Impact Controls in `scripts/intent_router.py`:** Add backward-compatible support for `intent_revision`, `impact_class` (`I0–I4`), `reasoning_level` (`L0–L5`), `material_unknowns`, `inferred_assumptions`, cognitive `methods`, and deterministic rule-based classification helpers — strictly enforcing that JSON fields never authenticate host consent.
4. **Deterministic Failure Recovery, Review Truthfulness & Sanitized Learning:** Extend `scripts/verify_completion.py` to validate `review_mode` (`INDEPENDENT_AGENT`, `HUMAN_REVIEW`, `SELF_REVIEW`, `NOT_RUN`) and independent reviewer evidence references without breaking v1 reports; extend `scripts/development_journal.py` with additive Decision Capsules, compact session-resume Checkpoints, and a quarantined Lessons store (`CANDIDATE -> REVIEWED -> VALIDATED -> ACTIVE -> SUPERSEDED/REJECTED`) with secret/PII sanitization and zero automatic self-modification of `AGENTS.md`.
5. **Single Authoritative English Technical Corpus + Bilingual User Guides:** Standardize `AGENTS.md`, `skills/*/SKILL.md` technical specs (preserving only explicit bilingual routing triggers tested in `tests/`), `references/`, `scripts/`, and technical reports in English while keeping bilingual EN/AR user-facing guides (`README.md`/`README.ar.md`, `HOW_TO_USE.md`/`HOW_TO_USE.ar.md`, `index.html`, `explorer.html`, `project-wizard.html`).
6. **Plan 0007 Alignment & Clean 7-Platform Rebuild:** Preserve `plans/active/0007_Master-Integration/` untouched, update `PortableAdapter` + brand credit string (`"The Heart of Geospatial Innovation — By Ahmed Ibrahim"`, `author.name: "Ahmad Ibrahim"`), and rebuild all 7 bundles exclusively through `Update-All-Plugins.ps1 -BuildOnly`.

## 3. Alternatives Considered

- **Option B — Create 18 Micro-Skills or a 38th Reasoning Skill:** Rejected. Adding more `SKILL.md` entrypoints increases context overhead, risks routing overlap with `prompt-intent-orchestrator` and `gis-development`, and violates progressive disclosure.
- **Option C — Keep Monolithic `AGENTS.md` with Appended Sections:** Rejected. Appending without consolidating duplicates degrades attention across limited context budgets and worsens rule discoverability.

## 4. Consequences & Limits

- **Positive:** Single accountable owner per decision, machine-auditable rule traceability, decoupled risk gating (`I0–I4`) vs effort allocation (`L0–L5`), quantitative before/after behavioral evaluation (`GAIB`), and restored plugin manifest consistency across all 7 targets.
- **Honest Limits:** Markdown policies and offline validators improve determinism and instruction clarity (`T0/T1`) but do not alter underlying model weights, enforce OS sandboxes by themselves, or substitute for absent native GIS/client runtimes (`ArcPy`, `QGIS CLI`, `ogr2ogr`, `Playwright`, `codex`, `claude`, `agy`, `cursor`), which must remain `NOT_RUN`.
