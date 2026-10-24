---
name: gis-development
description: Build, audit, debug or migrate GIS software and geoprocessing tools for ArcMap, ArcGIS Pro, QGIS, standalone desktop apps, 2D web mapping, 3D globes, remote sensing and geospatial Rust/Python stacks. Choose compatible spatial libraries, verify CRS and geospatial correctness, generate starter code, and test before claiming a GIS feature works.
license: MIT
---

# GIS Development — Agent Skill

Use this skill when designing or implementing a GIS **tool, add-in, plugin, desktop app, raster/vector processing pipeline, web map, or 3D globe**. This skill supplies decision and QA rules. It is **not** an installable substitute for ArcPy, QGIS, GDAL or vendor SDKs.

## Procedure: do this in order

1. **Identify the deliverable and deployment target.** Exact product + version (ArcMap 10.x, ArcGIS Pro major version, QGIS version, or standalone); OS; programming language; data formats; offline needs; license constraints; intended user interaction; test environment. If a crucial value is unknown, state an assumption, mark it unverified, and use the conservative route.
2. **Choose the right pathway.** Read one platform reference and `../../references/geospatial-foundations.md` for file and coordinate considerations. Use `../../references/project-catalog.json` to find *verified links*, not to uncritically import projects.
3. **Write a minimal architecture and acceptance contract.** Input schema, geometry type, expected CRS and units, optional elevation/Z/M, invalid/empty geometry behavior, nodata/masked raster behavior, output format/fields/metadata, working directory, dependencies and licensing.
4. **Protect portability.** ArcMap and ArcGIS Pro have separate runtime and API assumptions. Isolate GIS analysis from UI/ribbon wrappers; choose an engine only if allowed in that environment.
5. **Implement a vertical slice.** Start with an example from `../../templates/` if appropriate. Make a *functional end-to-end action* before adding extra commands; no placeholder commands presented as implemented.
6. **Verify source and licenses.** Re-check upstream APIs against the exact pinned release, its license and deployment constraints. Avoid unverified code recipes, private tokens or unsupported imagery endpoints.
7. **Test geospatial correctness.** Load known examples; verify geometry count and types, area/distance units, datum transformations, invalid features, NoData, output location, field names, and repeatability. Test user interface commands as actually wired, not just displayed.
8. **Deliver an auditable report.** Changed files, target version, what runs, what was tested (and where), what remains unverified, permissions/licenses, and exact next steps.

## Platform selector

| Target | Read | Typical API | Forbidden shortcut |
|---|---|---|---|
| ArcMap / ArcCatalog 10.x | `../../references/arcmap-legacy.md` | ArcPy + Python 2.7 in legacy installs | Claim Python 3 features work or use `arcpy.mp` |
| ArcGIS Pro | `../../references/arcgis-pro.md` | ArcPy / `.pyt` / Python 3 | Pretend `arcpy.mapping` equals `arcpy.mp` |
| QGIS | `../../references/qgis.md` | PyQGIS / Processing algorithms | Assume every version shares one Qt/PyQGIS API |
| Desktop / 2D / 3D | `../../references/desktop-and-web.md` | Tauri/Rust, Qt, MapLibre, CesiumJS | Treat rendering engine as geoprocessing engine |
| Remote sensing / AI | `../../references/remote-sensing.md`, `../../references/geoai-satellite-map.md` | GDAL, STAC, raster processing, model inference | Ignore radiometry, alignment, licensing and reproducibility |
| .NET GIS desktop / Pro SDK | `../../references/dotnet-gis.md` | WPF, WebView2, NetTopologySuite, ArcGIS Pro SDK | Assume .NET GIS components or ArcGIS SDK are free of platform and license constraints |
| Spatial libraries | `../../references/geospatial-foundations.md` | GDAL, PROJ, GEOS, GeoRust | Do metric buffers on longitude/latitude degrees |

## Required pre-delivery check

- [ ] Specify exact target runtime and versions; prove compatibility or clearly label assumptions.
- [ ] Validate input schema, field sizes (including 10-character Shapefile limits), output field aliases, Z/M and date/time behavior.
- [ ] Confirm CRS, transformation pipeline, axis order, distance/area units and rasters' pixel alignment.
- [ ] Make output deterministic, avoid overwriting raw inputs; use temporary files safely.
- [ ] Report data provenance, provider terms, secrets handling, and third-party licenses.
- [ ] Run static tests locally and application-level integration checks where the required app exists.
- [ ] For GUI: click-test each advertised ribbon/button/panel action; never count visual placement as functionality.
- [ ] Document incomplete tests, required installations, and known limitations.

## Catalog behavior

Open `../../references/project-catalog.json` for tools matching the exact need. For exact EarthMapper source review, read `../../references/earthmapper-case-studies.md`. The catalog includes **multiple EarthMapper repositories with different meanings**. Match the user's intended project by owner and purpose; do not assume one name maps to one software system. `GeoRust` is a Rust library ecosystem; `GeoLibre` is a geospatial app platform; `GeoLibra` is a distinct GitHub user and must not be conflated.

When new sources are needed, consult their official repositories/docs, verify the exact URL, and propose a catalog pull request with the required metadata. Source links are references and do not imply endorsed or guaranteed functionality. Distinguish **README-only product showcases**, **research papers with no released code**, **archived source repositories** and **actually inspectable source libraries** before suggesting code reuse.

## Example user requests

- "Create a Python toolbox for ArcGIS Pro that clips raster outputs to a study boundary."
- "Port this ArcMap geoprocessing script to ArcGIS Pro without breaking its parameter dialog."
- "Build a QGIS Processing plugin to create spatial buffers using a projected working CRS."
- "Select an open 2D+3D stack for a Windows GIS desktop viewer, including KML and GeoPackage."
- "Audit coordinate systems and identify why output area measurements are wrong."