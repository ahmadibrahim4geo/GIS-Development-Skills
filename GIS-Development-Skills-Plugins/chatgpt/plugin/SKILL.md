---
name: gis-development-suite
description: Route and support verifiable GIS software development across QGIS, ArcGIS, desktop, web, data and automation using the bundled specialist skills, safety gates, examples and evidence contracts.
license: MIT
---

# GIS Development Skills — self-contained suite

This distribution preserves the repository's shared files so its relative
references remain available after packaging.  It contains instructions and
deterministic helpers; it does not install GIS software, grant licenses or
prove native execution.

Start with [the shared project policy](AGENTS.md#start-here). Identify the goal and proof of success, apply the security and token policies, and use the required project and specialist checks. Read [skill readiness](references/project-governance-workflow.md#skill-readiness-before-use) for the capabilities you need.

Work in [small verified steps](references/portable-execution-guidance.md#work-within-existing-ownership). Review the saved state on resumption, collect evidence before reporting results, and use the [GitHub delivery workflow](PUBLISHING.md#approved-github-delivery) when it is in scope. Use the model selected by the user.

To identify the bundle used by a session, run `python -B scripts/build_skill_bundle.py --identity . --format json` from the directory containing this `SKILL.md`. Compare the entry path and fingerprint with the authorized distribution.

Use [the bilingual How to Use guide](docs/HOW_TO_USE.md) and
[Arabic guide](docs/HOW_TO_USE.ar.md) for practical requests and limitations.
