# Self-contained skill distribution

The source checkout keeps shared material in repository-level `references/`,
`scripts/`, `examples/`, `templates/` and `fixtures/` directories. Individual
skills also link to sibling skills. A command that copies only
`skills/<name>/` therefore has not preserved the complete local dependency
graph merely because `SKILL.md` itself was installed.

## Verified local bundle path

Run the standard-library builder from the repository root with Python 3.11 or
newer. Choose a new output location; existing outputs are never overwritten.

```powershell
python scripts/build_skill_bundle.py --output-dir dist/skill-release
python scripts/build_skill_bundle.py --check dist/skill-release/gis-development-suite.zip
python -B scripts/build_skill_bundle.py --identity dist/skill-release/gis-development-suite --format json
```

Run `--identity` on the bundle root selected by the client. The command reports
the actual path and hash of its `SKILL.md` and the content fingerprint derived
from the bundle inventory. Two builds from the same Git commit can contain
different working-tree content. Compare their fingerprints and use `--check`
to verify all installed files against the selected inventory.

The command produces:

```text
dist/skill-release/
  gis-development-suite/          # inspectable expanded distribution
    SKILL.md                       # suite entrypoint
    bundle-manifest.json           # file sizes and SHA-256 hashes
    skills/                        # core router and specialists
    references/ scripts/ ...       # shared runtime guidance and helpers
  gis-development-suite.zip       # deterministic archive
  gis-development-suite.zip.sha256
```

The build uses an explicit repository allowlist. It rejects symlinks,
sensitive-looking credential/key files, individual files larger than 10 MiB,
expanded bundles larger than 25 MiB, and output paths that would contain the
source repository. It excludes Git internals, `.agent-development-log/`,
virtual environments, caches, package directories and previous build outputs.

The post-build audit verifies:

- required router, security, evidence, journal and plan files;
- every manifest size and SHA-256 digest;
- absence of unexpected or missing files;
- all local Markdown link targets remain inside and present in the bundle;
- skill IDs agree with `references/repository-manifest.json`.

The ZIP uses sorted paths, a fixed timestamp and fixed file permissions so two
builds from the same source bytes and Git commit have the same SHA-256.

## Source checkout versus installable archive

The repository source remains the contributor/development surface. The bundle
is the release-candidate consumption surface for users who need the core router
and its shared dependencies together. Do not point users to a single nested
skill install as a verified complete route until an isolated installation test
shows that its external references are present.

The archive has a root skill named `gis-development-suite`. A compatible
Agent Skills installer may accept a local or release-asset archive, for example:

```powershell
npx skills add path/to/gis-development-suite.zip --skill gis-development-suite
```

That command is a **candidate integration command**, not evidence in this
repository that a particular CLI version or coding-agent client completed the
installation. Before publishing support for a client, record its exact CLI and
agent versions, install into an isolated project, confirm the installed file
manifest, trigger a routing smoke request, and report the observed result.

From an expanded or freshly unpacked archive you can run
`python -m tests.test_contextual_routing` at the bundle root. This exercises the
included CLI routing code and skill inventory with bilingual inputs without
writing to an agent client's installed skills directory.

## Use one policy across agent clients

Use the repository `AGENTS.md` for project rules and the expanded pack's
`SKILL.md` for entry into the bundled skills. Use client instructions to find
either entry and keep the bundle tree intact.

| Client | Check in a fresh session |
| --- | --- |
| Codex | Confirm the workspace `AGENTS.md` or the explicit bundle entry. Compare the active bundle with the approved fingerprint. |
| Claude Code | Verify the workspace instruction source. The adjacent `CLAUDE.md` imports `AGENTS.md` for sessions that use Claude-specific instruction files. [Instruction discovery](https://code.claude.com/docs/en/memory) |
| VS Code Copilot | Confirm the active chat harness, the workspace instructions and its recognized skill location. [Instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions) · [Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills) |
| Antigravity | Verify the workspace rules and the client's skill location. Preserve the full bundle when selecting a skill. [Rules](https://antigravity.google/docs/rules-workflows/) · [Skills](https://antigravity.google/docs/skills) |
| Other readers | Provide the absolute `AGENTS.md` or bundle `SKILL.md` path. Record which files and checks the session can access. |

Verify discovery and live tool capabilities separately. Use authorized local
tools when the client provides equivalent checks, and report missing actions
as BLOCKED or NOT RUN as appropriate. The user configures the model in the client.

## Evidence boundary

Passing the builder and audit is repository/offline evidence only. It does not
install QGIS, ArcGIS, GDAL, an AI model or an MCP server; it does not execute an
agent prompt; and it does not establish T2-T4 native GIS evidence. Fill the
[GIS acceptance report](../templates/GIS_ACCEPTANCE_REPORT.md) and apply
[DoneProof](../skills/completion-evidence/SKILL.md) before making broader release
claims.

