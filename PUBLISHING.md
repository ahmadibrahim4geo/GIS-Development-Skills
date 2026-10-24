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

## Publish the static homepage with GitHub Pages

The repository includes a standalone responsive bilingual `index.html` and `assets/logo.svg` / `assets/icon.svg`. It loads `references/project-catalog.json` and `references/free-geospatial-apis.json` from the same repository directory, so the cards reflect future catalog updates.

1. Open the repository **Settings → Pages** (requires repo administrator access).
2. Under **Build and deployment**, select **Deploy from a branch**.
3. Select branch **main**, folder **/(root)**, then **Save**.
4. After GitHub Pages successfully publishes the page, check https://ahmadibrahim4geo.github.io/GIS-Development-Skills/ . Verify the catalog/API tabs, keyword and category search, Arabic RTL toggle, responsive mobile layout, and relative JSON requests. The URL should **not** be advertised as live until the Pages deploy reports success.

Opening `index.html` directly from a `file://` URL may block JSON fetching due to browser security policies. Use GitHub Pages or a local HTTP server such as `python -m http.server` from the repository root. No API keys or external JavaScript libraries are needed to display the page.
