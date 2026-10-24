# GIS Development Skills 🌍

**An open, installable Agent Skill for building reliable GIS tools, plugins, web maps, and desktop geospatial applications.**

Created by [Ahmed Ibrahim](https://github.com/ahmadibrahim4geo). Independent community resource; **not affiliated with Esri, QGIS, GeoRust, GeoLibre, or other catalogued projects**.

> **Status:** v0.2.0 expanded catalog and EarthMapper audit. Curated source pointers, development workflows, code starter templates and offline catalog tools. Templates are illustrative; production workflows must be tested in the target GIS installation.

[اقرأ بالعربية](README.ar.md) · [Contributing](CONTRIBUTING.md) · [Publishing](PUBLISHING.md) · [Catalog](references/project-catalog.json) · [Skill](skills/gis-development/SKILL.md)

## What makes this different from an awesome-list?

This repository includes a **working agent skill**: step-by-step architecture selection, compatibility rules, geospatial correctness checks, GIS application pathways, and reference starter code. The catalog is supporting evidence, **not a code-vending collection**. A coding agent must establish requirements, consult the relevant reference, verify package APIs, implement, and test before claiming success.

## Target development paths

| Your goal | Preferred starting path | Read |
|---|---|---|
| ArcMap 10.x geoprocessing script | Legacy ArcPy / compatible Python 2.7 | `references/arcmap-legacy.md` |
| ArcGIS Pro `.pyt` or script tool | Modern ArcPy / Python 3 | `references/arcgis-pro.md` |
| QGIS plugin / Processing toolbox | PyQGIS, Processing provider | `references/qgis.md` |
| GIS desktop application | Python/Qt, Tauri/Rust, or C# + interoperable core | `references/desktop-and-web.md`, `references/dotnet-gis.md` |
| 2D maps / web mapping | MapLibre, GeoLibre, appropriate provider | `references/desktop-and-web.md` |
| 3D globe / terrain | CesiumJS + verified imagery/terrain source | `references/desktop-and-web.md` |
| Spatial engines / big data | GDAL, PROJ, GEOS, GeoRust, Rasterio | `references/geospatial-foundations.md` |
| Satellite imagery / AI | Open GeoAI libraries and research **with explicit source availability** | `references/remote-sensing.md`, `references/geoai-satellite-map.md` |

## Exact EarthMapper projects: verified distinction

- **[AliAlkazraji/EarthMapper](https://github.com/AliAlkazraji/EarthMapper)** — Windows GIS product/feature reference (WPF, WebView2, 2D/3D, DEM, Sentinel-2, local GeoAI). **Root currently contains only README.md**; no source code or open-source license available to reuse.
- **[HIT-SIRS/EarthMapper](https://github.com/HIT-SIRS/EarthMapper)** — academic bidirectional satellite↔map generation framework. Inspected repository has README, assets and Apache-2.0 LICENSE, **but no runnable implementation or weights**.
- **[rmkemker/EarthMapper](https://github.com/rmkemker/EarthMapper)** — distinct older remote-sensing segmentation reference.

Read [`references/earthmapper-case-studies.md`](references/earthmapper-case-studies.md) for practical building blocks, caveats and test criteria.

## Installation for coding agents

After publishing this repository at `ahmadibrahim4geo/GIS-Development-Skills`:

```powershell
npx skills add ahmadibrahim4geo/GIS-Development-Skills --skill gis-development
```

Run inside a project to install to that project; `-g` installs globally. The public CLI is documented at https://github.com/vercel-labs/skills. The `npx` command requires Node.js; confirm your installation meets its current runtime requirements. The repository location is **proposed until it has been created and pushed to GitHub**.

For manual use, copy `skills/gis-development/` into the supported skills directory for your agent, or read `SKILL.md` directly.

## Examples

- "Build an ArcGIS Pro Python toolbox to validate polygons and preserve source attributes."
- "Create an ArcMap 10.8 script tool without Python 3 syntax."
- "Convert a geoprocessing algorithm to a QGIS Processing plugin, with a feature-level QA checklist."
- "Recommend a safe, open technology stack for a Windows GIS desktop app that opens GPKG, Shapefile, KML and GeoTIFF."
- "Compare CesiumJS, MapLibre, and GeoLibre for an offline-capable desktop viewer."

## Starter templates (not packaged GIS binaries)

- `templates/arcgis-pro-toolbox.pyt` — ArcGIS Pro Python toolbox example (copies features safely).
- `templates/arcmap-script-tool.py` — legacy ArcMap script-tool starter.
- `templates/qgis-processing-algorithm.py` — QGIS Processing algorithm starter.
- `templates/standalone-geojson-summary.py` — standard-library, non-destructive file checker.

## Catalog search (Python 3, no external packages)

```bash
python scripts/validate_catalog.py
python scripts/search_catalog.py --platform arcgis-pro
python scripts/search_catalog.py --query 3d
python -m unittest discover -s tests -v
```

The searchable data lives in [`references/project-catalog.json`](references/project-catalog.json). Project URLs and selected READMEs/root trees were checked during curation on 2026-10-24. **Entries are not a live feed**; check upstream documentation, branch, maintenance, version, security notices, license and service terms before adoption.

## Important safeguards

- Do not treat ArcMap (retired) and ArcGIS Pro as equivalent Python runtimes.
- Never copy third-party code into this repo without its actual license and attribution; linking is not the same as licensing derivative code.
- Verify coordinate reference systems, axis order, linear units, no-data behavior, geometry validity and data attribution.
- Never imply that an example runs in a proprietary GIS environment without testing it there.
- Do not use commercial or API-keyed basemap/terrain services unless licensing and credentials are agreed.

## Roadmap

1. **v0.1.0** — foundation skill, 25 curated references, 4 starter templates and local validation.
2. **v0.2.0** — EarthMapper source audit, Windows .NET stack, additional verified repository pointers, satellite-AI research separation.
3. **v0.3 (planned)** — tested sample data, ArcGIS/QGIS environment integration, packaging and advanced parameter validation.
4. **v0.4 (planned)** — reference 2D/3D GIS desktop implementation with offline data tests and strict license tracking.

Community proposals and verified pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License and third parties

This repository's **original** scripts, templates and written guidance are MIT licensed; each linked project keeps its **own** license. The catalog does not grant rights to re-use upstream code, imagery, hosted services, trademarks, or data.