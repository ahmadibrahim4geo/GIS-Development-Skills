# Failure Recovery, Independent Review & Sanitized Learning

> Canonical specification for AAREF requirements `REQ-FAIL-01..11`, `REQ-ROLE-01..10`, `REQ-CTX-01..12`, and `REQ-LRN-01..09`.

## 1. Root-Cause Failure Protocol & Anti-Loop Limits

1. **Reproduce Before Fixing:** Record exact tool/runtime version, minimal fixture, expected vs observed output, and stderr/logs. State explicitly when reproduction is impossible.
2. **Isolate First Divergence:** Separate symptoms from causal origin across layers (`data -> config -> permissions -> dependency -> API -> logic -> lifecycle -> renderer -> packaging -> host runtime`). Read actual error messages; do not guess from filenames.
3. **Discriminating Experiment:** Test the smallest change separating competing hypotheses while leaving original inputs untouched. Never change multiple unrelated variables blindly.
4. **Fix Root Cause + Add Regression Check:** Never mask an engine or CRS bug in the UI layer. Add a focused test capturing before/after behavior.
5. **Repeat-Failure Circuit Breaker:**
   - Track exact failure signatures (`error_type + failing_boundary + command/step`).
   - **After 2 identical failures without new diagnostic evidence:** Trigger `REPLAN` — switch hypothesis, tool, or fixture inspection.
   - **After 3 unjustified repeat failures (or any security/permission block):** Halt retries cleanly and emit `BLOCKED` / `PARTIAL` with exact unresolved cause. Security or external side-effect errors must **never** auto-retry.

| Failure Category | Required Agent Response |
|---|---|
| `transient_network / rate_limit` | Respect provider terms & bounded backoff; zero captcha/auth bypass |
| `permission / auth_denied` | Halt action, state missing host permission explicitly; never read/leak secrets |
| `tool_unavailable` | Route to authorized equivalent or mark `NOT_RUN` / `BLOCKED`; never simulate native execution |
| `compile / dependency_lock` | Read exact compiler/lock error and Python/SDK version (`py314 != arcgispro-py3`); avoid blind upgrades |
| `data / crs_invalid` | Isolate raw input, report missing/invalid CRS or corrupted records without mutating source files |
| `test_regression` | Trace exact diff/hypothesis causing regression; revert only agent-authored broken patch within scope |
| `scientific_inconsistency` | Withdraw ungrounded numerical claim; re-verify primary equations, scaling constants, and units |
| `scope_conflict` | Halt out-of-scope edits; surface diff against approved `intent_revision` for user decision |

On partial task completion across multi-item batches, deliver only verified safe artifacts, tag overall status `PARTIAL`, and never hide failing criteria or use destructive git reset/clean without consent.

## 2. Role Architecture & Review Mode Truthfulness

Core Plan `0007` mandates **4 core roles** (`Programmer -> Independent Reviewer -> Tester -> Acceptance`) for consequential work, enriched cleanly by **12 optional logical functions** (`Intent Analyst`, `Researcher`, `Architect`, `Strategist`, `Programmer`, `Scientific Reviewer`, `Critical Reviewer`, `Security Reviewer`, `Tester`, `Optimizer`, `Acceptance Auditor`, `Learning Curator`). Never spawn redundant subagent processes when one focused pass satisfies the step cleanly.

### 2.1 Honest `review_mode` Attribution (`verify_completion.py`)

Every verification report should explicitly classify review independence:
- `INDEPENDENT_AGENT`: Genuine isolated subagent or separate session receiving the spec, migration/traceability matrix, and code diffs/artifacts *without* programmer self-justifications, backed by an observed subagent ID/transcript or log artifact.
- `HUMAN_REVIEW`: Documented human inspection and sign-off in the live host session.
- `SELF_REVIEW`: Same model and context reviewing its own work (previously referred to as `SAME_AGENT_REVIEW`). Never disguise `SELF_REVIEW` as `INDEPENDENT_AGENT`.
- `NOT_RUN`: No review performed.

Reviewers inspect spec compliance first, then correctness/security/scientific accuracy; a reviewer never fixes code and then certifies its own fix as independent. Report findings using structured fields: `finding_id`, `severity`, `requirement_id`, `path_or_evidence`, `observed`, `expected`, `impact`, `recommended_fix`, `disposition`.

## 3. Checkpoints & Sanitized Engineering Lessons (`development_journal.py`)

- **Checkpoints (`Context Intelligence`):** Long-horizon resume snapshots capture `task_id`, `root`, `head`, `working_tree_summary`, `intent_revision`, `plan_ref`, `completed_ids`, `pending_ids`, `evidence_refs`, `critical_decisions`, `known_failures`, `protected_inputs`, `next_authorized_action`, `environment_status`, and `timestamp`. On resume, inspect actual `HEAD` and workspace files before running the next authorized slice.
- **Quarantined Learning Pipeline:** Lessons extracted from journal steps follow strict lifecycle promotion inside `.agent-development-log/lessons.jsonl`:
  `CANDIDATE -> REVIEWED -> VALIDATED -> ACTIVE -> SUPERSEDED / REJECTED`.
- **Sanitization & Anti-Poisoning Guards:**
  - Reject automatic promotion from single unverified guesses or external/untrusted tool text.
  - Redact secrets, tokens, credential paths, private emails/phones, internal client filenames, and sensitive project coordinates before storing portable lessons.
  - **Zero Policy Self-Modification:** Neither `development_journal.py` nor any autonomous loop may modify `AGENTS.md` or relax Security Guardian / approval rules automatically; constitutional edits always require reviewed requirements, regression checks, and human/owner approval.
