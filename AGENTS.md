# Agent rules for this repository

- Maintain `skills/gis-development/SKILL.md` as the **general routing skill** and use domain-specific `skills/*/SKILL.md` for distinctly scoped engineering disciplines. Do not duplicate the same instructions across skills for minor changes.
- Maintain concise progressive-disclosure reference guides under `references/`.
- Keep platform compatibility, migration, licenses, CRS/measurement and source provenance prominent.
- Never copy code from catalog entries without examining that upstream license.
- Before publishing run `python scripts/validate_catalog.py`, `python scripts/validate_api_catalog.py`, `python scripts/validate_skill_pack.py`, and `python -m unittest discover -s tests -v`. All existing skills plus the dedicated Geospatial API Integration skill must remain discoverable.
- Keep titles/descriptions developer focused. Clearly label illustrative templates as untested inside host apps until verified.

- Maintain the static site at repository-root `index.html` and its assets in `assets/`; it must work at the project subpath under GitHub Pages, not only at a domain root.
- The website's project and GIS API cards must be loaded from the actual JSON catalog files; never introduce a second hardcoded catalog or claim third-party services are unrestricted.
- Preserve the English/Arabic language switch, RTL layout and accessible keyboard-driven search/filter controls.
- Treat GitHub repository sidebar About, topics, website URL, Discussions and Pages source as **administrator settings**; do not claim a Markdown commit changes them.
- If changing the website, keep `tests/test_landing_page.py` and the existing catalog tests passing.

## Project identity and website contract

- Approved brand title: **GIS Development Skills**; approved tagline: **The Heart of Geospatial Innovation**. Keep both in `assets/logo.svg` and the homepage hero.
- Preserve this original English mission sentence **verbatim** immediately below the hero logo and in the English README: `Build GIS tools, plugins and geospatial applications with a verifiable development workflow.`
- Visual language: **Approved Concept 02 — Layered Geospatial G**. A teal/mint geometric G over two tilted map layers (topographic contours and coordinate grid), on charcoal. Keep `assets/icon.svg` synchronized with `assets/logo.svg` and follow `assets/README.md`. Do not return to the earlier globe or contour-only G designs.
- The bilingual author panel `#author` is based on Ahmad Ibrahim's published biography and portrait on https://ahmadibrahim4geo.github.io/MIRSAD/ . Preserve meaningful contact links while keeping phone digits invisible in the UI, and do not repurpose MIRSAD-specific climate/consulting material as claims about this repository.
- The page enhancements live in `assets/brand-refresh.css`, loaded after inline base styles. Avoid duplication or breaking the existing working catalog filters, the language switch and GitHub Pages relative links.

- The logo SVG containers embed the same approved G bitmap: preserve that shared icon rather than recreating a stretched vector approximation. The homepage `hero-wordmark` renders the name and tagline in HTML with responsive CSS to prevent letter-spacing distortion. Preserve the exact original mission statement.

## Engineering evidence and website counts

- The website's initial project, API and skill counters must agree with the JSON catalogs and `skills/*/SKILL.md`; do not manually increase a counter without updating the actual source.
- Follow the published Agent Skills `SKILL.md` frontmatter format: name matches folder, lowercase kebab-case, description at most 1024 characters, progressive links to original references.
- A repository link, static test, mock ArcPy, screenshot or compiled Python package is not proof of successful **native** ArcGIS/QGIS/Desktop execution. Record T0-T4 evidence as defined in `references/ahmad-ibrahim-gis-case-studies.md` and `references/desktop-application-engineering.md`.
- Keep a standalone GIS application path distinct from ArcGIS SDK extensions and QGIS plugins. Verify full executable launch and packaging before stable claims.
- Do not re-add excluded immature reference projects without a fresh documented maturity review and user approval.
