# Mandatory Plugin Lifecycle Policy (`plugin-system/`)

This policy implements the Plugin Lifecycle requirements alongside [root repository governance](../../AGENTS.md) and [distribution documentation](../../docs/SKILL_DISTRIBUTION.md).

## 1. Canonical Source Boundaries

- **Single Source of Truth:** Only edit canonical files in `skills/`, `references/`, `schemas/`, `scripts/`, `templates/`, `examples/`, `fixtures/`, `native_tests/`, `docs/`, `assets/`, `VERSION`, `AGENTS.md`, `CLAUDE.md`, and root pages.
- **Generated Output Isolation:** Never hand-edit generated files inside `GIS-Development-Skills-Plugins/`.
- **End-User Bundle Scope Isolation:** User plugin ZIPs MUST omit developer-only updater scripts (`Update-All-Plugins.*`, `Update-My-Platforms.*`), `plugin-system/`, `reports/`, `.agent-development-log/`, `.git/`, and any secret/local files.
- **Standalone Usability Preserved:** Individual `skills/*/SKILL.md` folders remain usable independently without requiring platform-specific plugin installation.

## 2. Digest & Change Detection

The engine computes deterministic SHA-256 digests (`hashing.py`) across:
- Canonical file paths and byte contents (independent of filesystem timestamps and beyond `git diff` alone, so untracked/renamed/deleted files are always detected).
- Key governance & template inputs: `VERSION`, `AGENTS.md`, `plans/active/0007_Master-Integration/MASTER_AGENT_PROMPT.md`, `plugin-system/config/source-map.json`, and `plugin-system/config/platforms.json`.
- Built target output integrity: corrupted or missing built manifests trigger automatic rebuild even if the canonical source digest has not changed.

## 3. Standardized Lifecycle States (22 Official States)

Every platform report entry and pipeline summary uses strictly one of these 22 states:

| State | Meaning |
|---|---|
| `UP_TO_DATE` | Source digest and existing built package match; no rebuild needed |
| `BUILT` | Package freshly built and staged deterministically |
| `PASSED` | Verification, schema, link, license, and security checks passed |
| `BUILD_FAILED` | Clean staging, bundling, or ZIP generation failed |
| `VALIDATION_FAILED` | YAML, Markdown link, schema, or parity validation failed |
| `SYNCED_VERIFIED` | Local install target synced and active installed hash verified equal |
| `SYNC_FAILED_ROLLED_BACK` | Local sync failed on this platform and rolled back to last known-good |
| `OUTDATED` | Installed version digest differs from latest built digest |
| `RELOAD_REQUIRED` | Files updated locally, client host reload/restart still required |
| `NOT_INSTALLED` | Target agent client CLI or install root not present locally |
| `UNSUPPORTED` | Target feature/hook not supported by platform contract |
| `AUTH_REQUIRED` | Platform portal/CLI session unauthenticated |
| `MANUAL_ACTION_REQUIRED` | Store submission or client setting requires explicit human step |
| `PREPARED_FOR_SUBMISSION` | Release artifact validated and staged locally; not yet uploaded |
| `PENDING_REVIEW` | Submitted externally and awaiting store/team review |
| `PUBLISHED_VERIFIED` | Authorized release verified published externally |
| `NOT_APPLICABLE` | Step inapplicable in current runtime (e.g., local desktop sync in Cloud CI) |
| `NETWORK_UNAVAILABLE` | Remote check timed out after bounded retries |
| `LOCKED` | Another updater process holds the project lock |
| `SECRET_LEAK_BLOCKED` | Secret pattern or forbidden credential file detected; halted |
| `ROLLED_BACK` | Platform explicitly restored to a prior known-good version snapshot |
| `NOT_RUN` | Stage/runtime intentionally skipped or host unavailable (`T2–T4`) |

## 4. License & Security Hard Gates

- **License Gate:** Sources lacking a redistribution-compatible or verified license in `references/project-catalog.json` remain reference-only (never silently bundled as vendored code).
- **Secret Leak Incident Protocol (`REQ-PL-037`):**
  1. Immediately abort build/publish with `SECRET_LEAK_BLOCKED` (exit code `2`).
  2. Report ONLY the file path and secret rule ID — **never print matched secret values** into console output, logs, JSON reports, or ZIPs.
  3. Require upstream credential revocation/rotation by the owner before retrying.
  4. Never rewrite Git history (`git filter-repo` / force push) without separate explicit owner authorization.
