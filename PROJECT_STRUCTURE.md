# GIS Development Skills project structure

The source of record is the Git repository. The project publishes a static
site and distributes agent skills with shared references and CLI helpers.
The [project governance guide](references/project-governance-workflow.md)
explains how to audit a development project that uses this suite.

| Directory | Purpose |
| --- | --- |
| skills | General router, shared responsibilities and domain-specific skill entry points |
| references | Maintained guidance, catalog data, registries and evidence definitions |
| scripts | Standard-library validation, distribution, planning and governance tools |
| tests | Local regression coverage for scripts, catalogs, skills and the site |
| fixtures | Versioned, documented test inputs and expected results |
| testing data | Local, user-owned test inputs kept separate from outputs |
| testing results | Local run manifests, isolated fixture copies, outputs and readback receipts |
| examples | Portable and host-specific examples with documented acceptance limits |
| native_tests | Acceptance harnesses requiring the named GIS runtime |
| templates | Reusable plan, evidence and engineering templates |
| docs | Developer, setup, publishing and troubleshooting documentation |
| assets | Website styles, scripts, artwork and brand assets |
| GIS_Development_Skills_Complete_Brand_Kit | Original local brand source and delivery variants |
| Old - Safe to Remove | Local archive of superseded inputs and artwork with a recovery inventory |
| .github | GitHub Actions workflows and repository templates |
| .agent-development-log | Append-only development records, index and project memory |
| plans/active | Numbered plans with the original request, review status and traceability |
| plans/archive | Reviewed plans with recorded acceptance evidence |
| reports | Engineering and verification reports linked from plans and the journal |
| context | A short current handoff with links to the active plan and evidence |
| New Skill | Inert external-skill registry, quarantine review receipts and separately approved promotions |

Treat any local execution package or recovery copy as user input. Keep its
sources intact and use the versioned reports and plan to track implementation.

| Root files | Purpose |
| --- | --- |
| AGENTS.md | Repository engineering and approval rules |
| CLAUDE.md | Import of the shared repository rules for Claude Code |
| README.md and README.ar.md | Public introduction and setup instructions |
| index.html, explorer.html and project-wizard.html | Homepage, searchable GIS and skill catalog, and reviewable project-plan form |
| CHANGELOG.md and PUBLISHING.md | Release history and publishing procedure |
| CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md and LICENSE | Contribution guidelines, conduct, vulnerability reporting and source license |
| .gitignore, .nojekyll, robots.txt and sitemap.xml | Git exclusions and static site publishing or indexing configuration |
| doneproof-UDS*.json | Historical acceptance reports for the Universal Desktop Suite work |
