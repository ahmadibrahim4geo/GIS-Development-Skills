# Contributing

We welcome improvements to platform workflows, vetted libraries, examples, tests, translations and documentation.

## Proposing a library

1. Open an issue with the **exact GitHub owner/repo URL** (names like EarthMapper or GeoLibra are ambiguous).
2. Explain what a GIS developer can build with it, its supported stack, maintenance/activity evidence, upstream documentation and license.
3. Add/update a JSON record in `references/project-catalog.json` with all required fields; mark unknown upstream license `verify-upstream` instead of guessing.
4. Run `python scripts/validate_catalog.py` and `python -m unittest discover -s tests -v`.
5. Provide a small, reproducible example only if you are authorized to publish it. Our original code is MIT; third-party code keeps its own license.

## Submit a code template

Include the supported **product and version**, expected inputs and outputs, environment requirements, handling of CRS and units, command to test, failure cases and source/credit. Never claim untested proprietary GIS integration works.

## Pull request review checklist

- [ ] All source URLs are legitimate, canonical and relevant.
- [ ] License/attribution is preserved; no copied third-party material without permission.
- [ ] No API tokens, credentials, private data or unlicensed map tiles.
- [ ] Version-specific behavior documented and tests provided or clearly marked unverified.
- [ ] No breaking changes in the catalog JSON structure unless versioned.