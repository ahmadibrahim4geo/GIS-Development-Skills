# Release and publishing notes

The project is published at https://github.com/ahmadibrahim4geo/GIS-Development-Skills.

## Update an existing checkout

```powershell
git clone https://github.com/ahmadibrahim4geo/GIS-Development-Skills.git
cd GIS-Development-Skills
python scripts/validate_catalog.py
python -m unittest discover -s tests -v
```

For subsequent releases, create a feature branch, add the updated files, open a pull request, and merge only after review and validation. Do not create a second repository.

## Confirm the agent skill is discoverable

```powershell
npx skills add ahmadibrahim4geo/GIS-Development-Skills --list
npx skills add ahmadibrahim4geo/GIS-Development-Skills --skill gis-development
```

If the installer does not discover the skill, verify the folder `skills/gis-development/SKILL.md` and the installed version of the skills CLI.

## Release checklist

1. Run `python scripts/validate_catalog.py` and `python -m unittest discover -s tests -v`.
2. Ensure every new source has license and source-availability notes.
3. Wait for the GitHub Actions checks to pass on the commit being released.
4. Tag the tested commit as `v0.2.0` (or the next version) and publish a GitHub Release when ready.
5. State clearly that templates are reference implementations, not GIS-app integration-tested binaries.