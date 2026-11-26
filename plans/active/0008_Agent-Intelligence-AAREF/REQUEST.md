# Request 0008 — GIS Agent Intelligence & Governance (AAREF)

- **Request ID:** `GIS-AGENT-INTELLIGENCE-0008`
- **Plan Revision:** `r1`
- **Status:** `APPROVED` (approved by project owner in chat on `2026-11-26` after presenting `AR00` baseline audit and `0008` review card)
- **Source Plan Document:** `D:\My Software\Skills\GIS_AGENT_INTELLIGENCE_MASTER_DEVELOPMENT_PLAN.md`
- **Baseline Commit & Constitution Hash:** `7c0eb7da684c2670d5e020cbcc6c3b9f6de751bd` / `AGENTS.md` SHA-256 `6dd2c9fadc5f9a9e322cb87455b8bcd3b2dbe4f5dd7e70201d1e04524f6beb67`

## Verbatim User Objectives & Constraints

1. Adopt `GIS_AGENT_INTELLIGENCE_MASTER_DEVELOPMENT_PLAN.md` as the master development plan for evolving the central constitution (`AGENTS.md`), routing, and binding governance of `GIS Development Skills`.
2. Start with a comprehensive audit of the current repository, `AGENTS.md`, and all linked skills, references, and scripts (`AR00`), then execute phases `AR01–AR10` according to the approved governance and approval system.
3. Do not stop at theoretical instructions: evolve actual agent behavior, decision flow, adaptive reasoning (`L0–L5`), scientific & critical reasoning, planning, and failure recovery/learning.
4. Update existing skills as needed without duplicating ownership, preserve all 37 prior skills and capabilities, and integrate cleanly with Master Integration V2 (`0007`) and the 7-platform plugin lifecycle (`plugin-system/`).
5. Evaluate agent behavior before and after development with empirical evidence (`GAIB`), documenting review findings, test results, acceptance dispositions, and unresolved limitations.
6. **Language Constraint:** Use strict English in `AGENTS.md` and core technical/routing/governance files; audit and convert essential technical Arabic passages in core technical files to English for consistency while preserving bilingual English + Arabic user-facing explanation/importance guides (`README.md`/`README.ar.md`, `docs/HOW_TO_USE.md`/`docs/HOW_TO_USE.ar.md`, `index.html`, `explorer.html`, `project-wizard.html`, with English as the default developer-facing interface) and preserving Arabic routing/test fixtures.

## Approved Architectural Decisions (from `AR00` Review)

1. **Extend existing core owners (keep 37 skills):** Integrate AAREF capabilities into `prompt-intent-orchestrator`, `gis-development`, `gis-security-guardian`, `completion-evidence`, `agent-development-journal`, and domain specialists, backed by consolidated English references under `references/agent-reasoning/`.
2. **Preserve `0007` history & fix plugin working tree:** Keep `plans/active/0007_Master-Integration/` preserved intact; track AAREF under `plans/active/0008_Agent-Intelligence-AAREF/`; synchronize `PortableAdapter` icon/description (`"The Heart of Geospatial Innovation — By Ahmed Ibrahim"`, `author.name: "Ahmad Ibrahim"`) and rebuild all 7 plugin bundles deterministically via `Update-All-Plugins.ps1 -BuildOnly` in `AR09`.
3. **Strict English technical consistency:** Convert non-test Arabic technical prose in `references/` and non-`.ar.md` technical docs to English while retaining bilingual `.ar.md` guides, website i18n toggles, and Arabic routing keyword fixtures tested in `tests/`.
