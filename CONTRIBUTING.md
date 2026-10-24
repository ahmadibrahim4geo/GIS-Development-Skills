# Contributing

We welcome improvements to platform workflows, vetted libraries, examples, tests, translations and documentation.

## Proposing a library

1. Open an issue with the **exact GitHub owner/repo URL** (names like EarthMapper or GeoLibra are ambiguous).
2. Explain what a GIS developer can build with it, its supported stack, maintenance/activity evidence, upstream documentation and license.
3. Add/update a JSON record in `references/project-catalog.json` with all required fields; mark unknown upstream license `verify-upstream` instead of guessing.
4. Run `python scripts/validate_catalog.py`, `python scripts/validate_api_catalog.py`, `python scripts/validate_skill_pack.py`, and `python -m unittest discover -s tests -v`.
5. Provide a small, reproducible example only if you are authorized to publish it. Our original code is MIT; third-party code keeps its own license.

## Submit a code template

Include the supported **product and version**, expected inputs and outputs, environment requirements, handling of CRS and units, command to test, failure cases and source/credit. Never claim untested proprietary GIS integration works.

## Pull request review checklist

- [ ] All source URLs are legitimate, canonical and relevant.
- [ ] License/attribution is preserved; no copied third-party material without permission.
- [ ] No API tokens, credentials, private data or unlicensed map tiles.
- [ ] Version-specific behavior documented and tests provided or clearly marked unverified.
- [ ] No breaking changes in the catalog JSON structure unless versioned.
## Add or change a specialist agent skill

Maintain valid YAML metadata in `skills/<skill-name>/SKILL.md`; the name must match its lower-case hyphenated folder and the description must not exceed 1024 characters. Make the skill solve a distinct use case, link to domain references rather than copy long guides, and describe versions, inputs, risks, exact QA evidence and what was not tested. Keep `gis-development` as the entry point for cross-platform routing. Run the full validator after edits, update the website skill counter and README, and never claim native GIS execution from generic Python syntax checks.
