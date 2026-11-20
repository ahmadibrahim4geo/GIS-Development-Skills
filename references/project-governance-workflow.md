# Project governance and secure skill intake

This cross-cutting protocol extends the existing repository-wide skill
orchestration, GIS Development Router, Agent Development Journal,
GIS Security Guardian, DoneProof, remote sensing and code discovery skills.
It does not replace any existing specialist, manifest, code source or journal.

The implemented helper is scripts/project_governance.py. It uses Python's
standard library and does not download, install or execute external skills.

## Roles and ordered workflow

1. **Engineering Director / Intent:** identify the original user request,
   intended output, active reviewed plan/revision, protected data and acceptance
   criteria. Retrieve project context and compare with actual Git/files.
2. **Project Structure Engineer / Architect:** discover existing folders,
   solution/build files, module ownership and source/data boundaries. Classify
   each proposed restructure KEEP, EXTEND or REFACTOR. Seek user approval for
   consequential moves and protect existing project architecture.
3. **Toolchain Engineer:** discover available IDE, SDK, compiler, GUI designer,
   GIS engine and build tools, recording actual versions and authorized access.
   Do not assume software installed on a user PC is visible to a cloud agent.
4. **Domain experts and developers:** reuse existing relevant GIS specialists,
   vetted SDK references and libraries. Pass task IDs, input/output contracts,
   affected files and actual observed tool results between roles.
5. **Security and QA:** test from protected fixtures, read back outputs,
   inspect dependencies and permissions, prevent malicious skills and secrets
   exposure; use scientific checks for CRS, units, NoData, sensor, QA masks and
   spatial fidelity. T0/T1 does not establish native GIS T2-T4.
6. **Release and Journal:** build on the actual target platform, link native
   acceptance and security evidence, place user-test artifacts appropriately,
   update existing development journal and the compact context handoff.

Roles are responsibilities, not a claim that the host runs separate models.
The host still owns approvals, tool permissions, application execution and
native Windows/GIS tests.

## Root structure policy

The user project root receives AGENTS.md, PROJECT_STRUCTURE.md,
.gis-project-governance.json, plans/active/, plans/archive/, reports/,
context/CURRENT_HANDOFF.md, testing data/, testing results/,
New Skill/candidates/, New Skill/approved/, New Skill/promotion/, and
dist/user-testing/. The original project code and project-native layout
are never moved just to match a universal template.

| Location | Ownership and purpose |
| --- | --- |
| AGENTS.md | Additive project instructions, not an executable sandbox |
| PROJECT_STRUCTURE.md | Human-readable directory inventory and root-file descriptions |
| .gis-project-governance.json | Explicit purposes supplied for permanent folders |
| plans/active/ | Sequential drafts, original requests and plan status |
| plans/archive/ | Preserved plan history after evidence-linked closure |
| reports/ | Engineering and QA evidence and investigation |
| context/CURRENT_HANDOFF.md | Lightweight current state, not a replacement for the journal |
| testing data/ | USER OWNED fixtures; inputs are read-only unless separately authorized |
| testing results/ | GENERATED numbered test runs, screenshots, outputs and readback |
| New Skill/candidates/ | UNTRUSTED source metadata; never automatic skill activation |
| New Skill/approved/ | Only separately approved and legally reusable skill copies |
| New Skill/promotion/ | Review material for future integration into the main skill suite |
| dist/user-testing/ | Testable builds; do not call an unverified build stable |

The helper ensures the testing data folder exists even if empty. It creates
small .gitkeep placeholders and ignores actual user fixtures and generated
outputs in Git by default. Users must not put secrets or proprietary fixtures
in public commits. A run under testing results is labeled NOT RUN until a
real test has executed and evidence is recorded.

For fixture use, inspect formats, CRS/units, NoData, data provenance, sensor
metadata and expected values where relevant. Never write in place to testing
data. A run may use explicitly synthetic fixtures if clearly labeled, but
must report real-data tests as NOT RUN when no user data is present.

## Project-structure auditing

Every permanent directory must have a documented purpose. The generated
inventory marks unknown directories NEEDS_DESCRIPTION instead of inventing
responsibilities. Important root files are described separately. Dependency
folders, cache, temporary build outputs and raw test data are excluded from
recursive scans to limit unnecessary reading and private-data exposure.

When code architecture genuinely needs refactoring, record impacted imports,
build definitions, Qt resource paths, WPF project references, test fixtures,
rollback and actual regression results before or after an approved migration.
The structure helper does not move code files or claim that build succeeded.

## Basic commands

From a checkout of the skill suite, run commands with an authorized target
project path:

    python scripts/project_governance.py --project PATH audit
    python scripts/project_governance.py --project PATH init
    python scripts/project_governance.py --project PATH sync
    python scripts/project_governance.py --project PATH register-folder --path "assets/icons" --purpose "Project UI icon files"
    python scripts/project_governance.py --project PATH new-plan --title "Map Engine" --request "Improve camera control and verify output"
    python scripts/project_governance.py --project PATH new-test-run --name "Raster NoData"
    python scripts/project_governance.py --project PATH close-plan --id 0001 --evidence "reports/map-engine.md"
    python scripts/project_governance.py --project PATH register-skill --name "Qt UI" --source "https://github.com/example/qt-skill" --purpose "Review Qt implementation" --revision "reviewed-sha"

The paths above are examples. The agent must use the real location of
scripts/project_governance.py in its accessible skill checkout; these commands
do not imply installation of the helper in every client.

**Status semantics:** new-plan creates a DRAFT, never authenticated approval.
close-plan checks existence of a nonempty project-local evidence file, then
archives it; presence of that file is NOT proof of successful GIS operation.
DoneProof and real tests are still required. new-test-run creates NOT RUN
placeholders and never changes the user fixture data.

The helper appends a short managed rules section to existing AGENTS.md while
preserving original text; sync does not replace a user-authored structure
document. All mutations require appropriate project-user permission.

## External skill acquisition is a security boundary

First inspect current suite/installed skills and accepted local libraries.
If a real capability gap remains, search authoritative and community skill
repositories dynamically rather than using a fixed allowlist. Compare
functional match, duplicate coverage, license, maintainer, version,
dependencies and host requirements.

Keep candidate source information in New Skill/candidates; registration does
not fetch, install or execute code. Do not place this directory in any
automatically activated agent skill path. Pin a revision before integration.
Review the skill text and entrypoints through GIS Security Guardian plus
suitable tools (for example NVIDIA SkillSpector, Cisco Skill Scanner, dependency
and secret scanners) when available. Any scanner can miss threats.

Executing or enabling an external skill requires separately authorized,
least-privileged and ideally isolated tests. Review redistribution rights
before copying any upstream bytes. Promote proven candidates using the
existing source intake, manifest, router and bilingual documentation workflow.
Do not duplicate skills merely because they have a different name.

Existing Anthropic, NVIDIA, Qt, Esri, remote sensing, GIS code discovery,
security and token optimization references remain in use. Catalog reference
status must not be misreported as installed or successfully tested.

## Token and memory policy

Use the existing Token Optimization Triad: read only relevant code ranges,
prefer surgical patches, compact excessive tool logs and keep verified
handoffs. Do not optimize away required security scans, scientific source
checks or native GIS tests. Resume by comparing context and journal records
against current files and source revision.

## Implemented vs planned

The current helper implements safe root bootstrap, directory registration,
a human-readable structure inventory, draft numbered plans and evidence-linked
archival, fixture/output separation, numbered test-run placeholders and
candidate-only skill registration. It **does not yet** implement dynamic online
skill search, malicious-code scanning, IDE automation, toolchain probing,
remote runtime execution, multi-agent dispatch, automatic source restructuring
or native GUI acceptance. Those capabilities need separate host integration
and observed end-to-end tests before claims of completion.
