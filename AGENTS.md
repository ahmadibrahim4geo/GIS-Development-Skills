# Agent rules for this repository

- Edit the canonical `skills/gis-development/SKILL.md`; do not create duplicate skills for each small change.
- Maintain concise progressive-disclosure reference guides under `references/`.
- Keep platform compatibility, migration, licenses, CRS/measurement and source provenance prominent.
- Never copy code from catalog entries without examining that upstream license.
- Run `python scripts/validate_catalog.py` and `python -m unittest discover -s tests -v` for changes.
- Keep titles/descriptions developer focused. Clearly label illustrative templates as untested inside host apps until verified.