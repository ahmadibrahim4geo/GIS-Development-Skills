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

1. Run `python scripts/validate_catalog.py`, `python scripts/validate_api_catalog.py`, `python scripts/validate_skill_pack.py`, and `python -m unittest discover -s tests -v`.
2. Ensure every new source has license and source-availability notes.
3. Wait for the GitHub Actions checks to pass on the commit being released.
4. Tag the tested commit with the appropriate next semantic version (for example `vX.Y.Z` after accepting that exact commit) and publish a GitHub Release when ready.
5. State clearly that templates are reference implementations, not GIS-app integration-tested binaries.

## Free-first website QA

The index should show **every specialist from manifest skill_ids**, allow paging past 60 catalog results, and default API results to free-compatible tiers while preserving optional access to paid/trial records. Run static validators and the JavaScript syntax check, then verify the published URL in a real browser for EN/AR, mobile layout, cost selector, paging, external links and network fallback. Static code/CI does not prove browser deployment. Read [free-first policy](references/free-first-policy.md).

## Publish the static homepage with GitHub Pages

The complete copy-ready description, topics and Pages settings are maintained in [docs/REPOSITORY_SETTINGS.md](docs/REPOSITORY_SETTINGS.md). **Committing these files does not change GitHub About or Pages admin settings.**

The repository includes a standalone responsive bilingual `index.html` and `assets/logo.svg` / `assets/icon.svg`. It loads `references/project-catalog.json` and `references/free-geospatial-apis.json` from the same repository directory, so the cards reflect future catalog updates.

1. Open the repository **Settings → Pages** (requires repo administrator access).
2. Under **Build and deployment**, select **Deploy from a branch**.
3. Select branch **main**, folder **/(root)**, then **Save**.
4. After GitHub Pages successfully publishes the page, check https://ahmadibrahim4geo.github.io/GIS-Development-Skills/ . Verify the catalog/API tabs, keyword and category search, Arabic RTL toggle, responsive mobile layout, and relative JSON requests. The URL should **not** be advertised as live until the Pages deploy reports success.

Opening `index.html` directly from a `file://` URL may block JSON fetching due to browser security policies. Use GitHub Pages or a local HTTP server such as `python -m http.server` from the repository root. No API keys or external JavaScript libraries are needed to display the page.

**Documentation revision is not a GitHub Release.** A README badge or changelog section alone does not create a tag or downloadable release. Verify any published release on the repository's Releases page before advertising it as available.

## GIS agent operational publication checks

Validate the [derived manifest](references/repository-manifest.json) using `python scripts/build_manifest.py --check` and the [acceptance example](templates/gis-acceptance.example.json) with `python scripts/validate_evidence.py templates/gis-acceptance.example.json`. Run the standard offline CI tests before publishing.

[Native acceptance tests](native_tests/README.md) require real ArcGIS Pro and QGIS. [Weekly documentation URL checks](docs/SERVICE_MONITORING.md) are isolated and nonblocking, and cannot prove endpoint JSON availability, provider licensing or host compatibility.

Retain all previously published files and design elements; keep English and Arabic READMEs and `index.html` synchronized with new functionality.
