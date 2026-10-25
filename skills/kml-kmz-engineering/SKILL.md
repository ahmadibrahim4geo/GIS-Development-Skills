---
name: kml-kmz-engineering
description: Build secure, interoperable KML/KMZ import, export, rendering, conversion and round-trip workflows for desktop GIS, ArcGIS, QGIS and web maps.
---

# KML & KMZ Engineering

**Free-first default:** Follow [GIS free-first and licensing policy](../../references/free-first-policy.md); test open-source parsers where suitable, and disclose licensed host dependencies separately.

Use this skill when a GIS application or toolbox reads, writes, converts, renders or packages KML (OGC KML 2.2) or KMZ (ZIP package containing KML and resources). Load only the sections relevant to the task.

## Requirements discovery
- Identify target runtimes (ArcGIS Pro, legacy ArcMap, QGIS, GDAL/OGR, Cesium, Google Earth, MapLibre), versions and licensing.
- Identify whether **geometry-only conversion** or **faithful KML document rendering** is needed. Do not claim GDAL/OGR or ArcPy feature conversion preserves all KML constructs.
- Record required feature support: Placemark, Point, LineString, Polygon with holes, MultiGeometry, folders, ExtendedData, Style/StyleMap, icon and label styles, GroundOverlay, NetworkLink, Region/LOD, Camera/LookAt, TimeStamp/TimeSpan, altitudeMode, extrude, gx:Track, gx:Tour and COLLADA Model. Mark unsupported features explicitly.

## Coordinate systems and geometry
- KML geographic coordinates are longitude, latitude, optional altitude in WGS 84; never silently treat them as projected coordinates. Validate coordinate order, range, geometry rings, dateline crossings and altitude interpretation.
- Transform incoming/outgoing project CRS explicitly, using tested axis-order settings and datum transformations. Preserve Z where supported; distinguish clampToGround, relativeToGround and absolute altitude.
- Validate XML namespace handling, missing geometry, malformed XML, encoding, and empty files.

## Safe KML/KMZ loading
- Parse XML with secure settings: disable external entities, DTD resolution and external fetches; prefer defusedxml for untrusted Python inputs.
- Treat KMZ as untrusted ZIP: reject absolute paths, ../ traversal, symlink escapes, encrypted/unsupported members, excessive member count, oversized expanded payloads and extreme compression ratios. Enforce configurable total uncompressed size and per-entry limits *before* extraction; extract only into a controlled temporary directory.
- Do not automatically fetch NetworkLinks, remote icons, models or overlays. Require explicit user consent, restrict schemes to approved protocols, apply timeouts and size limits, and document privacy/network behavior.
- Resolve relative resource paths within the package without allowing escape. Avoid unbounded in-memory XML trees or decompression; use streaming/chunking where practical.

## Non-negotiable style fidelity on imported KML/KMZ

**PRESERVE FIRST (default):** For external KML/KMZ (received from colleagues, loaded from disk, restored from saved project), the imported author's style is authoritative. **Do not repaint points, lines or polygons; do not replace original pin symbols with your app's default icons; do not assign a new style palette or discard original styles on open/save.** See the [complete mandatory behavior and acceptance checklist](../../references/kml-kmz-symbol-preservation.md).

- Keep **separate representations** of `original_imported_style`, `temporary_presentation_fallback` and `explicit_user_override`. Scene selection glow or temporary missing-image placeholder must never mutate exported KML.
- Parse and retain nested/shared `Style`, `StyleMap` normal/highlight pairs, `styleUrl`, inline style precedence; `IconStyle` href/color/scale/hotSpot/heading, `LabelStyle`, `LineStyle`, `PolyStyle` fill/outline/opacity, `BalloonStyle`, `ListStyle`, applicable `gx` styling and referenced screen/ground overlays. Do not treat colors as ordinary RGB; KML color hex order is **aabbggrr**.
- Preserve local KMZ icon PNG/JPEG paths and **identical original bytes** where possible. Preserve original remote href strings but never auto-fetch a network resource. Warn on unresolved/unsupported assets without replacing source styling. Avoid inventing hosted Google Earth icon URLs or bundling another author's copyright-protected icon.
- On user-chosen edit, apply to the selected feature(s) only, with undo/Reset Original, separate metadata and Save As where possible. Imported style remains accessible for lossless comparison.
- Source hierarchy, feature names, geometry, altitude, metadata and style groups remain intact; check round-trip **actual resolved styles and asset SHA-256**, not just feature count. If converter/library drops styles, detect and disclose loss; use a preservation-capable model instead of flattening to generic GIS geometry.
- For **new** user-authored features (not existing imports), consult [marker/icon sources](../../references/map-marker-icon-library.md): Pinhead/Maki/Temaki, Material Symbols, CC BY-SA Map Icons Collection, mixed-license Map Icons, Leaflet marker renderers, or Cesium PinBuilder. Convert allowed icons to packaged PNG assets if exporting KMZ; never apply these to existing imported features without explicit consent.

## Import and rendering
- Separate semantic document model (folder hierarchy, styles, resources, times, metadata) from GIS feature layers and renderer. Preserve original KML for features not representable in the target GIS schema.
- Support icons, labels, line/polygon styles and overlays where the renderer allows; document Google Earth extension gaps rather than silently dropping them.
- Keep a provenance and conversion-loss report with counts, unsupported nodes and warnings.

## Export and round trip
- Produce valid XML with correct namespaces, escaped text, geometry coordinate order and explicit style/resource references.
- Package a portable KMZ with the main KML document and all local referenced resources using safe relative paths. Avoid leaking machine-local paths or credentials.
- Test KML -> import -> export -> reimport and KMZ -> unpack -> repack -> reopen. Compare geometry/topology, CRS, feature counts, folder hierarchy, ExtendedData, time, styles, assets and altitude semantics. Classify expected versus unintended loss.
- Include compatibility fixtures for Google Earth, ArcGIS Pro, ArcMap (legacy), QGIS and Cesium; label tests as unverified until executed in real hosts.

## Performance, stability and crash prevention
- Benchmark increasing feature counts, deeply nested folders, many icons, large overlays and large KMZ archives. Measure peak RAM, elapsed time, UI responsiveness and recovery after cancellation.
- Apply memory budgets, lazy loading, background workers, progress reporting, cancellation and resource cleanup. Do not block the UI thread for large parsing or rendering tasks.
- Test corrupted ZIP/XML, zip bombs, missing icons, invalid coordinate strings, broken links and repeated open/close cycles. Record crash logs and memory trends.
- Never advertise a universal maximum feature count: publish measured environment-specific limits and graceful degradation behavior.

## Suggested implementations
- Python: defusedxml + zipfile with explicit resource limits; GDAL/OGR (KML or LIBKML driver when available) for feature conversion; PyQGIS for QGIS-specific layers.
- ArcGIS Pro: validate supported arcpy conversion tools in the installed release and test actual outputs. ArcMap: isolate Python 2.7/ArcPy compatibility code and test in its legacy host; do not assume shared Python 3 dependencies work.
- Web/desktop 3D: use a KML-capable renderer such as Cesium where supported, and explicitly test extensions. MapLibre-based applications generally require conversion or a separate KML parser and renderer.
- Check component licenses, bundled binaries, data rights and runtime availability; prioritize free/open-source paths.

## Acceptance checklist
- [ ] Target host and supported KML constructs documented
- [ ] Malformed and malicious inputs rejected safely
- [ ] Coordinate/altitude semantics verified
- [ ] Original imported colors/icons/line and polygon styles, StyleMaps, label properties and transparency remain unchanged by default
- [ ] Local KMZ assets (including original image bytes) and folder/style metadata retained
- [ ] Round-trip and cross-host fixtures executed
- [ ] Performance/stress/cancellation tests reported with measured limits
- [ ] Unsupported constructs and conversion losses disclosed
- [ ] Tests distinguished from unverified recommendations
