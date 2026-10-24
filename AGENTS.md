# Agent rules for this repository

- Edit the canonical `skills/gis-development/SKILL.md`; do not create duplicate skills for each small change.
- Maintain concise progressive-disclosure reference guides under `references/`.
- Keep platform compatibility, migration, licenses, CRS/measurement and source provenance prominent.
- Never copy code from catalog entries without examining that upstream license.
- Run `python scripts/validate_catalog.py` and `python -m unittest discover -s tests -v` for changes.
- Keep titles/descriptions developer focused. Clearly label illustrative templates as untested inside host apps until verified.

- Maintain the static site at repository-root `index.html` and its assets in `assets/`; it must work at the project subpath under GitHub Pages, not only at a domain root.
- The website's project and GIS API cards must be loaded from the actual JSON catalog files; never introduce a second hardcoded catalog or claim third-party services are unrestricted.
- Preserve the English/Arabic language switch, RTL layout and accessible keyboard-driven search/filter controls.
- Treat GitHub repository sidebar About, topics, website URL, Discussions and Pages source as **administrator settings**; do not claim a Markdown commit changes them.
- If changing the website, keep `tests/test_landing_page.py` and the existing catalog tests passing.
