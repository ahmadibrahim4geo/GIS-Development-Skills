# Model & Client Harness Adaptation Policy

> Canonical specification for AAREF requirements `REQ-MOD-01..09`. Separates underlying language model behavior from client host capabilities across all supported targets.

## 1. Model vs Client Harness Separation

- **No Model Lock-In & No Secret Prompt Extraction:** Policies run under whatever model the user selects. Never require model switching automatically, never claim markdown instructions modify neural weights, and never instruct the host or subagents to extract or persist hidden internal thinking blocks / private system prompts. Record only factual inputs, reviewed alternatives, concise Decision Capsules, and observable tool evidence.
- **Capability Snapshot (Probe, Never Assume):** Classify each host session dimension honestly as `VERIFIED`, `UNSUPPORTED`, `UNKNOWN`, or `RELOAD_REQUIRED`:
  1. `root_and_scoped_instructions` (`AGENTS.md`, `.cursor/rules`, `CLAUDE.md`)
  2. `skills_discovery_and_on_demand_loading`
  3. `agent_delegation_and_isolated_reviewers` (required for `INDEPENDENT_AGENT`)
  4. `native_effort_control` (mapped only when documented in the active client runtime)
  5. `file_terminal_browser_native_gis` (actual CLI/SDK availability vs `NOT_RUN`)
  6. `hooks_and_deterministic_validators`
  7. `context_session_resume`
  8. `mcp_discovery_and_invocation` (host-authenticated grant required)
  9. `usage_telemetry` (`actual`, `estimated`, or `UNKNOWN` — never convert raw char counts to exact token counts without an observed tokenizer)
  10. `plugin_install_and_reload`

## 2. Client Adapter Compatibility Contract

Generated plugins in `GIS-Development-Skills-Plugins/` are **platform mappings** of the single canonical repository—never fork a conflicting rulebook per platform:

| Client / Target | Integration Reality & Verification Rule |
|---|---|
| **Antigravity** | Uses workspace rules (`AGENTS.md` / `GEMINI.md` per client rules), plugin manifest with Brand Kit icon/credit, and subagent isolation when available; verify live install via `agy` only if CLI is installed (`NOT_INSTALLED` / `MANUAL_ACTION_REQUIRED` otherwise) |
| **Codex** | Discovers root/local `AGENTS.md` and `.agents/plugins/marketplace.json` + `./skills`; respects sandbox/approval mode exposed by host |
| **Claude Code** | Loads `CLAUDE.md` (`@AGENTS.md`), `.claude-plugin/marketplace.json`, skills, and lifecycle hooks when host supports them |
| **Claude.ai / Cowork** | Cloud archive upload; lacks local repo auto-execution—disclose manual upload and verify remote runtime limits |
| **ChatGPT** | Static instruction/archive bundle (`supports_hooks: false`, zero local shell hooks); never claim workspace repo access unless files/connectors are explicitly attached |
| **Cursor** | `.cursor/rules/gis-development-skills.mdc` + `plugin.json`; respects IDE file/terminal permission prompts |
| **Portable Bundle** | Self-contained directory + ZIP with root `SKILL.md`, `AGENTS.md`, `skills/`, `references/`, `scripts/`, and zero `plans/` links |

Whenever an external client CLI (`agy`, `claude`, `codex`, `cursor`) is absent or requires GUI reload, report platform status strictly from `plugin-system/` allowed states: `BUILT`, `PASSED`, `SYNCED_VERIFIED`, `NOT_INSTALLED`, `UNSUPPORTED`, `RELOAD_REQUIRED`, `AUTH_REQUIRED`, or `MANUAL_ACTION_REQUIRED`.
