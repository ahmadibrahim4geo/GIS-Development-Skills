## Outcome

What user or developer outcome does this change improve? Link the issue when one
exists.

## Scope and compatibility

- Target GIS host(s), versions and operating systems:
- Inputs, outputs, CRS/units and data provenance:
- License or external-service constraints:
- Files or behaviour intentionally left unchanged:

## Evidence

- Commands actually executed:
- Fixtures and expected result:
- Observed result and output readback:
- Highest honest evidence tier (T0–T4):
- Native or external checks that remain NOT RUN:

## Safety and review checklist

- [ ] The change is within the reviewed issue/request scope.
- [ ] Existing skills, catalogs, branding, bilingual controls and user data are preserved.
- [ ] New outputs are non-destructive by default; risky changes have rollback notes.
- [ ] Third-party code/assets were not copied without source and license review.
- [ ] Credentials, private GIS data and exact device location are absent.
- [ ] English/Arabic user-facing surfaces and generated counts are synchronized where applicable.
- [ ] `python scripts/validate_catalog.py` passes.
- [ ] `python scripts/validate_api_catalog.py` passes.
- [ ] `python scripts/validate_skill_pack.py` passes.
- [ ] `python scripts/security_audit.py --root .` passes.
- [ ] `python -m unittest discover -s tests -v` passes, or failures are documented above.

Green CI is repository evidence only. It does not prove licensed ArcGIS/QGIS,
native UI, live provider or packaged clean-machine behaviour unless those exact
checks are recorded above.
