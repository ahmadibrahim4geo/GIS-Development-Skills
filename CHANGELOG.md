# Unreleased — Master Integration V2, Multi-Platform Plugin Lifecycle & Web/Mobile Engineering (2026-11-25)

- Complete Phases `P00–P11` of `plans/active/0007_Master-Integration`:
  - **Engine Selection V2 & 461 Capability Profiles (`skills/geospatial-engine-selection`):** Added atomic capability taxonomy (`references/engine-capability-taxonomy.json`), 1:1 `references/engine-capability-profiles.json` (461 projects), `schemas/engine-*.schema.json`, 6 discovery/comparison/recommendation/audit CLI helpers (`scripts/{discover_engines,compare_engines,recommend_stack,validate_engine_profiles,engine_repo_metadata,inventory_ui_actions}.py`), source-fork `KEEP/HIDE/DISABLE/REMOVE` & clean-room reference UI guides, and 8 example stacks (`examples/engine-selection/`).
  - **Web GIS (`W01–W12`, `WEB-01..18`) & Mobile GIS (`M01–M10`, `MOB-01..20`) Expansions:** Added pure-ESM `examples/web-gis/`, SQLite WAL 15-field offline sync `examples/mobile-gis/`, `docs/{WEB_GIS_GUIDE,MOBILE_GIS_GUIDE,WEB_MOBILE_GUIDE.ar}.md`, interactive filters in `explorer.html` & `project-wizard.html`, Node contract suite (`tests/web-gis/web_gis_contract.test.mjs`), and Mobile contract suite (`tests/mobile-gis/test_mobile_contracts.py`).
  - **Unified Plugin Lifecycle (`plugin-system/` & `GIS-Development-Skills-Plugins/`):** Implemented `portable` plus 6 client adapters (`codex`, `chatgpt`, `claude-code`, `claude-ai`, `antigravity`, `cursor`), tracked `.agents/plugins/marketplace.json`, `.claude-plugin/marketplace.json`, `.cursor/rules/gis-development-skills.mdc`, opt-in loop-safe hooks, external `%LOCALAPPDATA%` owner config via `Update-My-Platforms.ps1`, and SHA-pinned `.github/workflows/plugin-{validate,build,release}.yml`.
  - **GitHub Delivery Reconciliation (`origin/main` + Docs/Web):** Integrated `0adcbeb` + `8747283` (`modern-web-guidance` skill #37 + paired UI/UX Pro Max readiness `scripts/web_guidance.py` + accessible copy/picker improvements), refreshed `README.md`, `README.ar.md`, `index.html`, and `explorer.html` for all 37 skills / 461 profiles / 7 plugin targets, and synchronized `references/repository-manifest.json`.
  - **Honest Verification & QA (`P10`–`P11`):** Consolidated full T0/T1 verification, ZIP/Git secret hygiene, and honest `NOT_RUN` declarations for absent T2–T4 native GIS/GPU/browser/mobile/CLI runtimes inside `reports/plugin-lifecycle/023_QA_REPORT.md` and `026_P11_FINAL_ACCEPTANCE.md`.

# Unreleased — universal desktop CAD/GIS, parametric modeling, and reversible AI copilot standards (2026-11-19)

- Establish a universal engineering standard across all desktop CAD/GIS applications, geoprocessing tools, and AI copilot development, incorporating specifications from 78 open-source GitHub repositories, 7 industry benchmarks, interactive prototypes, and local software projects.
- Add `references/urban-design-competency-coverage.md` mapping 55+ technical competencies (LOD 0-3, Double Precision Local Origin, decoupled core, 4 subsurface networks), 78 GitHub repositories, 7 industry benchmarks, and local projects to universal standards.
- Add `references/urban-design-source-registry.json` and `references/urban-design-sources.md` auditing all 78 repositories with strict license classification (MIT, Apache-2.0, LGPL v3 dynamic linking for SARibbon/ADS, GPL clean-room rules, PolyForm Noncommercial quarantine) and supply chain threat modeling.
- Add `references/native-cad-gis-desktop-architecture.md` establishing C++20/Qt6 vs Godot 4 vs UE5 engine tradeoff evaluations, Camera-Relative Local Render Origin shifting, Dark CAD UI design tokens, contextual ribbons (`SARibbon`), dockable panels (`Qt-ADS`), dynamic property inspector (`QtPropertyBrowser`), and locked metric scales 1:500–1:5000 (`Lock-Canvus-Zoom`).
- Add `references/urban-hierarchy-parametric-modeling.md` defining the 8-layer spatial data hierarchy, relational DAG cascading engine, ASAM OpenDRIVE clothoid networks, Streetmix cross-section assemblies, earcut polygon triangulation with interior holes, Clipper2 setbacks, open BIM (IFC 4.3), and 4 subsurface infrastructure networks.
- Add `references/urban-simulation-engines.md` standardizing astronomical solar/shadow calculations (Ladybug concepts), stormwater D8 runoff and roadway gully spacing (`SmartGully` pattern), and microscopic multimodal traffic simulation (Eclipse SUMO XML).
- Add `references/reversible-cad-ai-copilot.md` and `references/urban-export-studio.md` specifying mandatory `QUndoStack` / `Ctrl+Z` reversibility, strict C++ JSON Schema validation (`pboettch/json-schema-validator`), selection context awareness, ISO A0–A4 true-scale plotting (`Smart Plot PDF`), 3D flythrough cameras (`Contour`), and vector roundtrips.
- Add `references/token-optimization-triad.md` and `references/agent-context-memory-architecture.md` formalizing Ponytail (pre-coding), Caveman (surgical patches), Token Optimizer (cleanup), and the modular 5-file `context/` architecture.
- Update target skills (`gis-desktop-application-development`, `geospatial-data-processing`, `terrain-hydrology-lidar`, `geospatial-ai-agents`), enrich `scripts/intent_router.py` with bilingual CAD/GIS keywords, and synchronize English/Arabic READMEs without exceeding router character limits. Native GIS T2–T4 runtimes remain NOT RUN.
- Tune `skills/gis-desktop-application-development` and `skills/prompt-intent-orchestrator`: upgrade frontmatter description, activate clickable markdown links for all 10 architectural references, expand engine selection table with CAD engines (Clipper2, earcut, SARibbon, IfcOpenShell, libOpenDRIVE), add Desktop CAD/GIS Invariants section, and update homepage (`index.html`) quick options.

# Unreleased — remote sensing indices, band mappings, and scientific interpretation (2026-11-19)

- Enhance `skills/remote-sensing-pipelines` with a comprehensive spectral index catalog, physical band mappings, and scientific interpretation guidance without creating a duplicate skill.
- Add `references/remote-sensing-indices.json` (19 core indices across optical and SAR domains with mathematical ranges and authoritative citations) and `references/remote-sensing-indices.md`.
- Add `references/remote-sensing-sensor-band-mappings.md` documenting sensor bands across Landsat (TM/ETM+/OLI), Sentinel-2 MSI, MODIS, and HLS, with Level-2 surface reflectance scale factors ($DN \times 0.0000275 - 0.2$), Sentinel-2 L2A BOA offsets, and SAR linear power units.
- Add `references/remote-sensing-threshold-profiles.json` enforcing that classification thresholds are context-dependent and never universal constants; guard against automatic uncalibrated classification.
- Add `references/remote-sensing-index-source-registry.json` establishing a 6-tier hierarchy of official mission docs, peer-reviewed studies, and training materials with a 12-step dynamic discovery protocol.
- Add reproducible synthetic evaluation engine `examples/remote-sensing/synthetic_index_calculator.py` and 23 unit tests in `tests/test_remote_sensing_indices.py` covering exact formulas, edge cases (zero division, NaN, negative reflectance), alias disambiguation (NDWI, NDSI, RVI), and threshold safety guards.
- Integrate bilingual routing in `scripts/intent_router.py` and synchronize English and Arabic documentation. Native GIS T2–T4 runtimes remain NOT RUN.

# Unreleased — portable execution guidance (2026-11-15)

- Add shared model/agent-independent guidance with proportionate Lite/Standard/Deep effort, capability-based tools, reuse decisions and bounded diagnosis.
- Connect existing intake, routing, code discovery, agent engineering, journal and DoneProof owners; preserve approval, security and evidence requirements without adding a skill or parallel workflow.
- Explain the guidance in English/Arabic READMEs and the homepage guide. Cross-client behavior and native GIS execution remain unverified by these documentation changes.

# Unreleased — architectural intent and UI/engine contracts (2026-11-05)

- Route ribbon, UI shell and engine integration requests through explicit source/target and component ownership; keep unknown UI.js identity unresolved until source/version preflight.
- Preserve typed architecture, constraints, task descriptions, I/O contracts and command correlation in workflow previews; distinguish dependency edges from declared data contracts.
- Add renderer-independent flow validation and a proposed QGIS ribbon example covering command parity, connected result/error/state paths, asynchronous policies and readback.
- Gate code recipe applicability by the intended GIS platform, preventing generic ribbon/button terms from selecting ArcGIS Pro for QGIS requests.
- Extend bilingual wizard/homepage/README guidance and regression scenarios; keep all 35 skills and existing catalog counts. Full offline verification: 423 tests, 422 passed and one Windows symlink privilege skip. Native GIS T2–T4 and Archify rendering remain NOT RUN. See the [Arabic engineering review](docs/ARCHITECTURE_INTENT_REVIEW_2026-11-05.ar.md).
- Use no-clobber atomic rename for journal writes on Windows workspaces that disallow hard links; preserve existing canonical history.

# Unreleased — OpenGeoHub and time-aware Data Explorer reference (2026-10-30)

- Register five upstream GIS code/research repositories (scikit-map, soildb, GEDTM30, spatial-prediction-eml, spatial-layers) with root licenses or explicit unverified status.
- Register OpenGeoHub STAC API (`opengeohub-stac-api`) under public-fair-use in `free-geospatial-apis.json` (OAS 3.1, POST /search, COG assets, QML/SLD symbology), expanding API catalog to 53 services.
- Expand OpenGeoHub and OpenLandMap STAC data references, live Python client integration, routing links, a view-only Data Explorer contract, protocol distinctions (static STAC catalog, dynamic STAC API, COG byte serving, WMS/XYZ) and bilingual discovery notes.
- Integrate routing keywords in `intent_router.py` and `gis_code_discovery.py` for spatial prediction, soil properties, multi-epoch land cover, COG raster review, and research repository comparisons.
- Synchronize manifest and public inventory counters (193 project references, 53 APIs, 26 data repositories, 17 code/research sources across READMEs, index.html and explorer.html). Desktop runtime not modified.

# Unreleased — project-driven visual sources (2026-10-28)

- Clarify that visual source discovery has no fixed website/provider allowlist or mandatory search order. Sources change with the project and task.
- Permit direct selection of suitable imagery embedded or linked inside the current project source website, after the existing relevance/source/terms review. Named catalogs and optional skills remain non-exclusive examples.
- Align the source/workflow guides, acceptance example, policy, bilingual README and homepage wording. No runtime or provider restriction was introduced.

# Unreleased — visual asset discovery and integration (2026-10-27)

- Add a general specialist for internet/source discovery, official logos, thumbnails, illustrations, screenshots, covers and backgrounds, with source/brand review and real-versus-illustrative preview rules.
- Connect the main router, bilingual lexical hints, Desktop/Web/Mobile/UI specialists, free-first policy, README languages, homepage and Explorer. Preserve existing identity, author/footer and sources.
- Add an optional local Pillow helper for safe new raster variants, alpha/padding, source/variant hashes and metadata readback, with behavioral tests. It does not search, download, generate, authenticate licenses or prove native UI integration.
- Document extensible sources and optional related design/search skills without automatically installing dependencies or paid providers; require independent T2–T4 evidence for live source/render/UI/package behavior.

# Unreleased — conditional Archify visualization (2026-10-27)

- Add GIS Architecture & Workflow Visualization as shared support for explicit diagram explanations, reviewed feature designs, cross-component diagnosis and structural changes.
- Connect main/intent routing, validate declared purpose/type/evidence/language, retain domain ownership and non-executing workflow previews.
- Add an independently authored workflow example, bilingual copyable requests and runtime/license/Arabic RTL guidance; synchronize discovery, policy and generated skill inventory.
- External renderer/browser checks are separate from native GIS proof; missing optional runtime leaves unrelated GIS work available.

# Unreleased — MCP/native capability orchestration (2026-10-26)

- Add independent optional MCP Integration & Tool Orchestration skill, capability/effect registry, non-executing stdlib candidate selector with native fallback, and adversarial offline tests.
- Connect the capability preflight to the goal-first workflow CLI via `--mcp-inventory`; retain domain ownership, Security Guardian host gates, command/data trace, DoneProof and Journal responsibilities.
- Refresh bilingual README, homepage, Explorer, graph reachability, free-first catalog, generated inventory and CI checks without altering branded author/footer content.
- Candidate inventories and T1/T2 fixture checks **do not** prove a real connected MCP server, native GIS engine, device automation, approval or T3/T4 run.

# Unreleased — full skill workflow and release-readiness hardening (2026-10-26)

- Audit all **30 installed skills** for router reachability, documented handoffs, free-first coverage and lexical-domain routing, with a read-only standard-library auditor enforced by GitHub CI.
- Fix mobile and OS/device permission keyword routing; reject malformed plan fields safely and require one explicit accountable domain `owner_skill` for each compiled task.
- Strengthen DoneProof with a plan-bound release gate (`--plan --require-verified`) matching original request, task, revision and complete acceptance criteria. Reject duplicate/unsafe JSON and unsupported aggregate success claims. Logs remain host-observed, not authenticated by this offline tool.
- Require IMPORT and READBACK in lossless trace declarations; check consistent EXPORT/READBACK artifact identifiers when present, and add regression tests for gaps.
- Publish an engineering audit and responsibility ledger covering prompt → security → specialist → command/data diagnostics → native tests → DoneProof → journal, with explicit T0–T4 limits.
- Refresh bilingual READMEs, How to Use, publishing guide, Explorer and public `index.html` into an eight-stage workflow while leaving brand/author/footer data intact.
- GitHub Actions structural/static/offline checks cannot certify a live target GIS engine, a packaged desktop/mobile app, user approval or an external provider receipt.

# Unreleased — dedicated GIS Mobile Application Development (2026-10-26)

- Add independent Android/iOS mobile GIS skill with architecture, local geodata, GNSS, secure sign-in, offline-first synchronization and native release/test guidelines.
- Route mobile projects through the general GIS router and bilingual Project Wizard; keep Android/iOS device verification separate from Windows Desktop E2E.
- Introduce offline edit/idempotency/conflict regression fixture plus mobile device-evidence schema validator; do not claim an APK/IPA, a GNSS reading or live OAuth test from repository CI.
- Update the 29-skill inventory, free-first policies and mobile sources in the canonical 188-entry catalog, without overriding the existing author footer or desktop workflows.

# Unreleased — cross-platform system capability and permission skill (2026-10-26)

- Add platform-wide System Capabilities & Permissions Agent Skill, external skill/library candidate registry, native permission/driver acceptance contract and offline standard-library planner with tests.
- Integrate Device Context, GIS Router, Security, Desktop, Web, UX/E2E, bilingual Explorer/homepage and Project Wizard; preserve protected author details and existing runtime engines.
- Native permission prompts, hardware, Bluetooth/GPS and Windows installations have NOT been tested by these offline additions.

# Unreleased — four GIS UI quality specialist skills (2026-10-26)

- Add independent GIS UI Command Audit, Desktop E2E Testing, GIS Data Flow Diagnostics, and UI/UX Design & Testing skills, linked to the intent gateway, GIS Router, native Desktop Development, Security Guardian and shared evidence journal.
- Add responsibility/command/trace handoff contract and upstream source references; keep Windows UI Automation optional and disclose unverified upstream licenses.
- Add read-only Python stdlib HTML/XAML declaration inventory and synthetic GIS flow trace checker, with examples and regression tests. Offline classifications **do not** prove working GIS controls, real rendering, semantic CRS accuracy or native installers.
- Integrate bilingual GIS Explorer, homepage and Project Wizard quality-focus option with machine-readable draft plan; increase installable skill inventory from 23 to 27, preserve developer identity and user approval boundaries.
- Native Windows/QGIS/ArcGIS T2–T4 checks remain NOT RUN unless a real suitable application environment is observed.

# Unreleased — cross-PR integration and real workflow handoffs (2026-10-26)

- Integrate proposed Desktop GIS engineering (#25), repository-wide intent orchestration (#26), and the 188-source GIS catalog (#27) into one compatible PR, with combined CI regression tests.
- Fix 39 broken local Markdown links previously present in `docs/ENGINEERING_UPDATES_2026-10.md`, and add repository-wide link verification.
- Make the bilingual Project Wizard export a draft `gis-workflow-draft.json` plan matching the offline Intent Router schema; block export until the user goal and success criteria are explicit. Test actual Node DOM → Python workflow compiler handoff.
- Upgrade GitHub Actions checkout and setup-python to verified SHA-pinned Node.js 24 releases; eliminate the deprecated Node.js 20 actions warning.
- No native GIS runtime or authenticated hosting-agent approval has been tested; keep those acceptance tiers NOT RUN.

# Unreleased — GIS Software & Source Code Registry (2026-10-26)

- Extend the existing canonical project catalog from 148 to 188 **unique public repository links** (40 new, none copied) covering desktop, web, mobile, engines, spatial servers, .NET and remote sensing.
- Add a developer-facing decision guide and bilingual website entrypoint, plus router/Desktop/Web specialist links; preserve the author section and existing catalog rather than creating a second data store.
- Record preliminary GitHub availability/license metadata as **unverified for reuse**; no native builds, source imports or implied GIS engine/runtime compatibility.
- Add catalog field validation and regression tests for repository source categories, primary-skill routing, unique URLs, synchronized counters and disclaimers.

# Unreleased — Goal-first GIS skill workflow and Project Wizard integration (2026-10-26)

- Compile a user/AI-reviewed goal, desired outcomes, success criteria, owners and dependency graph into a read-only ordered workflow using `scripts/intent_router.py --workflow`; no autonomous execution or authenticated permissions claimed.
- Require explicit goal/outcome information for workflow compilation, reject unknown owners, cycles, missing dependencies, stale approval declarations, destructive operations without additional approval fields.
- Add bilingual goal and success-criteria fields, eight-stage execution preview, and invalidation for edits in the existing client-only Project Wizard. Preserve other wizard fields and the author's identity.
- Synchronize the cross-skill contract, Intent Orchestrator, core router, agent rules, EN/AR user guides, sample plans and regression tests.
- Keep source inspection read-only by default and distinguish host-level approval, T0/T1 offline checks and GIS-native T2/T4 verification.

# Unreleased — QGIS engine cross-skill compatibility and HTML routing (2026-10-25)

- Remove accidental single-application assumptions from generic QGIS Engine skill, references and agent prompts; retain existing project renderers and route to other specialists only when relevant.
- Separate QGIS Plugin and QGIS Engine pathways on bilingual homepage and Explorer. Add engine-aware Project Wizard selection, synchronized source-driven pathway counters and keyboard-accessible pathway cards.
- Extend offline regression tests for wizard English/Arabic generation, platform selection and QGIS engine link/compatibility contracts. Native QGIS execution remains an explicit separate acceptance level.
- Preserve every previous skill, catalog, author/footer contact, CSS brand and installer/host boundary.

# Unreleased — QGIS Engine Integration specialist (2026-10-25)

- Add a QGIS Core/GUI/Processing/Server standalone-engine skill, upstream source/license guide and native-only PyQGIS GeoPackage readback sample.
- Integrate new QGIS engine option with bilingual README, index, Explorer, desktop/plugin routing and decision tree; synchronize 23-skill inventory and offline tests.
- No claim of native QGIS/WPF runtime testing or packaged application validation.

# Changelog

## Unreleased — Project Wizard bilingual behavior and stale-export repair (2026-10-25)

- Fix Arabic translations for project types and generated Markdown plans; retain requirements when switching languages.
- Prevent stale plan downloads following input edits, and use project-specific specialist references in generated plans.
- Add Node DOM-interaction regression tests for English/Arabic generation, state changes, injection-safe text display and Markdown downloads.
- Link the wizard from the existing Explorer without altering developer profile/footer design.


## Unreleased — recover Project Wizard PR #12 on current main (2026-10-25)

- Resolved PR #12's stale main divergence without reverting the current bilingual homepage/footer, its GitHub Actions setup, security guardian, core router or KML author-style preservation.
- Published client-side bilingual GIS Project Wizard; Arabic and multilingual GIS specialist (22 skills), source review, reliability guides and KMZ fixture unit tests.
- Fixed invalid literal escaped newlines in the Wizard JS, synchronized manifest, README, homepage count, Explorer and free-first policy. Kept commercial host and native test limitations explicit.


## Unreleased — complete homepage redesign with in-page GIS How to Use (2026-10-25)

- Rebuild the homepage hero as a typographic 2-column studio layout with the original approved vector logo, workflow illustration and source-driven metrics.
- Move all essential install, platform selection, prompt-writing, permission/review, verification and journal guidance into the homepage; selectable eight-topic specialist command and bilingual sample request, clipboard controls, offline/manual route and FAQ.
- Add scoped responsive `assets/home-redesign.css` with a consistent charcoal/mint palette across sections. Preserve the existing bottom developer portrait, exact biography/contact markup and layout while recoloring backgrounds, accents and borders.
- Keep complete Explorer and existing GIS catalog/skills/QA functionality, add regression test for page functionality and author section stability.


## Unreleased — bilingual How to Use onboarding (2026-10-25)

- Expand index.html with an accessible English/Arabic onboarding walkthrough, four steps, real sample request with working copy button, coding-agent CLI and manual/self-study paths, FAQ and navigation link.
- Enhance Explorer's existing Quick Start rather than duplicating core functionality; add detailed English and Arabic usage guides, source/lifecycle caveats and regression tests.
- Preserve existing brand, footer/contact details, complete Explorer, GIS security/agent distinctions, dynamic skill catalog and release-gate CI checks.

# Changelog

## Unreleased — Agent Development Journal & Project Memory (2026-10-25)

- Add numbered append-only project-local request/action/revision/cancellation/rollback-intent/verification/handoff records with resumed context, hash-chain integrity and safe derived Markdown repair.
- Add standard-library offline CLI and tests, reference guide and a review of Planning with Files, Superpowers and Spec Kit (design inspiration only; no third-party tools installed).
- Update agent router integration, bilingual README/site, free-first matrix, manifest, security and CI. No automatic process monitoring, GIS host execution or Git rollback is claimed.


## Unreleased — Prompt Intent & Execution Orchestrator (2026-10-25)

- Add a review-first Arabic/English natural-language intent skill, dependency-aware plan format, skill routing and cross-cutting security requirements.
- Add offline standard-library keyword hints (not LLM inference), structured JSON validation, revision and risk approval assertions, ZEarth draft example and unit tests. The helper does not authenticate approval or execute GIS.
- Integrate router, decision tree, bilingual READMEs, bilingual website and derived inventory without replacing existing resources.


## Unreleased — Esri official references and Python environment audit (2026-10-25)

- Review original Apache-2.0 root license files of ten additional Esri official repositories. Record evidence and host/service caveats, with no new native-runtime validation claims (138 → 148 curated project links).
- Add offline, read-only ArcGIS Pro Python package version checker using a locally downloaded official Esri release matrix, synthetic unit tests, and a profile-aware Arcade authoring guide.
- Expand Esri integration, ArcGIS/desktop/cartography/catalog routing, and synchronize the English/Arabic README, index homepage and derived reference manifest. No proprietary Esri runtime, imagery or credentials included.

## Unreleased — Unified Icon Manager for GIS + protected KMZ adapter (2026-10-25)

- Treat icons as a general GIS library used across ArcGIS/QGIS/Cesium/web and desktop hosts, with a specialized new-KML/KMZ authoring/export adapter rather than a duplicated KMZ icon library.
- Extend catalog from 19 to 21 sources with user-provided Streamline (mixed-license discovery only by default) and Mapular (generator workflow inspiration only), and update CC BY-SA Map Icons Collection with 2026 SVG/PNG/custom colors and no-hotlink guidance.
- Add an operational Icon Manager design contract and a standalone offline bilingual HTML new-marker generator with SVG/PNG export; add a standard-library new PNG→KMZ exporter with ABGR, relative resources, style, hotspot and license metadata.
- Link both installable skills, map marker guide, Google/KML preservation requirements, bilingual website and README, while preserving footer and latest security/KML work. Third-party assets not copied; importing an existing KMZ never triggers icon replacement.
- Add deterministic Python unit tests for PNG validation, new KMZ packaging, KML colors, source permissions and docs/feature links. Demo is not native ZEarth/Google Earth integration.


## Unreleased — Map icon library and imported KMZ style protection (2026-10-25)

- Add eight independently licensed free/open map icon sources plus CesiumJS PinBuilder to the catalog (10 → 19), with KMZ export roles and font/plugin license distinctions.
- Preserve imported KML/KMZ icons, colors, opacity, label, line/polygon styles, StyleMaps, remote references and local asset bytes by default. Keep temporary rendering fallback distinct from explicit user-driven edits.
- Cross-link the existing Google/OGC KML compatibility work with a new dedicated preservation contract and icon-source selection guide.
- Add offline synthetic KMZ style/asset regression fixtures; update cartography and KML specialist skills, bilingual README and website without touching security work.


## Unreleased — Cartography styling and privacy-aware device context (2026-10-25)

- Add dedicated vector/raster cartography skill, 10-source license-aware style catalog, native format matrix, offline MapLibre point/line/polygon fixture and tests.
- Add device-context skill for system time/date/IANA timezone and explicit consent-based geolocation; distinguish device vs map scene location and simulated vs live Sunlight.
- Add offline stdlib Python context/timezone normalization fixture and DST/invalid-coordinates tests (not a GPS or solar position integration).
- Update router, decision tree, manifest, bilingual READMEs and searchable website style source tab; preserve existing project/API/data catalogs and footer.


## Unreleased — License evidence and free executable GIS examples (2026-10-25)

- Inspect source license files for 8 core GitHub projects, recording exact original license evidence and separating licensed product/service access from source rights. 130 projects remain unverified; no automatic false verification.
- Add a deterministic, network-free catalog license coverage reporter and guard rails for verified evidence metadata.
- Add fully local Horn slope ASCII raster and STAC ItemCollection metadata-filtering reference workflows with synthetic fixtures, unit/NoData/datetime tests and explicit T2-only evidence boundaries.
- Connect audited license progress, examples, skills, bilingual README/index, source intake process and CI validation.

## Unreleased — Blue Marble Geographics / Global Mapper specialist (2026-10-25)

- Add dedicated Global Mapper GMS, Python and licensed SDK engineering skill with version-specific runtime/redistribution controls.
- Add seven public third-party forks under Blue Marble's official GitHub organization and one independent, older GMS community scripting tutorial (138 curated code references).
- Document OpenMVG/OpenMVS photogrammetry, 3D Tiles, Cesium terrain tiling, glTF/Assimp/CGAL license caveats; no proprietary engine binaries or source copied.
- Synchronize English/Arabic README, index skill card and source count, router, desktop/web/terrain references, manifest and new offline regression tests. No native licensed runtime tested.

## Unreleased — Earth View and synchronized source intake (2026-10-25)

- Review Earth View's Three.js globe, NASA GIBS/Sentinel imagery, time-lapse, Electron and optional AI architecture, documenting upstream missing license and T0-only evidence.
- Add as 130th project; update web/desktop/remote-sensing/API skills and the bilingual index/READMEs without duplicating existing NASA/Copernicus APIs.
- Introduce atomic catalog/skill/README/index/manifest update checklist and additional count-drift regression validation.

## Unreleased — OpenGeoS agents and standalone GIS data source directory (2026-10-25)

- Add three installable specialists for dataset catalogs, typed geospatial agents and terrain/hydrology/LiDAR workflows.
- Add 25 distinct OpenGeoS software candidates to the project catalog (129 references) and a separate 24-entry geographic data source directory linking the owner-maintained larger database without mirroring it.
- Add a searchable bilingual data repository tab on the website, synchronize four source counts and document upstream licenses/access distinctions.
- Provide a deterministic offline search example, catalog validator and unit regression checks. Native GIS and upstream data endpoints remain unverified.

## Unreleased — agent routing, evidence and operational validation (2026-10-24)

- Preserve the entire former core instruction text verbatim in `skills/gis-development/LEGACY_FULL_SKILL.md` and an archived reference with corrected links; shorten the active Core Skill to a task router and specialist decision tree.
- Add auditable T0–T4 GIS Acceptance Report, machine-readable evidence validator, synthetic polygon/distance and binary fixture generator, native ArcGIS Pro/QGIS runtime harnesses.
- Add common before/after GIS mistake cases, security and performance guides, reproducible offline benchmarking and regression tests.
- Extend all 104 project and 39 API records with conservative verification metadata; add one derived manifest and CI checks for live counts.
- Add weekly isolated, rate-bounded public documentation availability reporting. Provider policy and actual JSON endpoint behavior remain separate validations.
- Refresh bilingual website, English/Arabic READMEs, agent/contribution/publishing rules and existing CI without removing prior assets or historical entries.


## Unreleased — production-oriented GIS skills and examples (2026-10-24)

- Non-destructively retain all earlier installable skills, curated sources, API records, templates, tests, bilingual UI and approved branding.
- Add three independent skills for spatial databases, geospatial vector/raster processing and remote-sensing pipelines (11 total).
- Add a deterministic synthetic network topology example and weather API-to-GeoJSON example with offline unit tests; include batch ArcGIS Pro PDF export, PostGIS sandbox SQL and STAC/COG validation procedure.
- Publish an evidence-based GIS Skill Quality Benchmark and production workflow reference; route from core skill, contribution rules, bilingual READMEs and homepage.
- Add six bilingual homepage cards, a reproducible example section, site navigation, updated skill count and example source syntax checks.

## Unreleased — site and repository experience (2026-10-24)

- Add two GEBCO_2026 access methods: no-key WMS visualization and CEDA OPeNDAP numeric global bathymetry/topography, increasing API catalog from 37 to 39 entries. Document source TID, 15 arc-second spacing, vertical datum caveats, public-domain credits, polar ice variants and no navigation use.
- Update English/Arabic site and README, discovery/integration/general/Desktop agent guidance and API validation regression tests.



- Add a dedicated **eighth** Geospatial API Integration skill and two new bilingual homepage pathway cards for data discovery and safe provider adapters.
- Extend the free/public geospatial API directory from 18 to **37 services** with 19 new documented providers and explicit access, license, coverage and quota warnings.
- Update bilingual homepage API count and explanatory text; add source-selection guidance to discovery, ArcPy, desktop and web GIS skills.
- Document migration from legacy HeiGIT and USGS endpoints; add regression checks for provider IDs and site counts.

- Add branded responsive bilingual static website, with interactive search/filter for the real GIS project and API catalogs.
- Add official vector logo, favicon, and GitHub Pages static-site support (`.nojekyll`).
- Improve English/Arabic README project introduction, status links and installable agent-skill metadata.
- Add reproducible landing-page checks and GitHub Issue forms for bugs and feature suggestions.
- Provide copy-ready repository About, topics, homepage and publication instructions under `docs/REPOSITORY_SETTINGS.md`; GitHub sidebar values must still be set by an authorized administrator.

## 0.3.5 — 2026-10-24

- Audit all installable skills, repository tools, geospatial templates, bilingual documentation and GitHub Pages source.
- Introduce a dedicated standalone Desktop GIS engineering skill and accompanying QA/release guide.
- Add a network-free skill pack validator covering official frontmatter rules, broken local links, site assets and synchronized project/API/skill counters with negative-case tests.
- Modernize developer rules and CI to validate all four Python template examples without implying native GIS execution.
- Clarify documentation revision vs actual GitHub Releases; avoid duplicating logo tagline under the wordmark.
- Publish prioritized findings and untested native GIS, API, installer and browser acceptance boundaries in `docs/TECHNICAL_AUDIT_2026-10-24.md`.

## 0.3.4 — 2026-10-24

- Remove an early-stage mobile GIS app from curated case studies and catalog recommendations; maintain only sufficiently mature engineering references.
- Update the searchable catalog to 104 entries while preserving six installable skills.
- Align bilingual documentation and website counters; add a regression test preventing accidental re-inclusion. No changes to the excluded app's own repository.

## 0.3.3 — 2026-10-24

- Inspect public, author-owned GIS projects and identify suitable first-party engineering references.
- Expand the source catalog to 105 repositories with explicit engineering roles, reference availability, original licensing and caveats.
- Add `references/ahmad-ibrahim-gis-case-studies.md` and an installable `arcgis-toolbox-engineering` skill covering Python 2/3 ArcPy, native acceptance tiers, scientific results, safe in-place geometry edits and Desktop migration.
- Add offline regression tests for case-study coverage and native-test disclosure; update primary skill, English/Arabic READMEs and GitHub Pages homepage to show six skills.
- Do not mirror third-party styles, run mutation workflows or claim ArcGIS-native processing was tested by the reference catalog CI.

## 0.3.2 — 2026-10-24

- Review Dr. Qiusheng Wu's official software directory (gishub.org/software) and add 40 verified, nonduplicate GitHub sources to the project catalog (84 total).
- Add `references/gishub-software.md` with stack selection, ArcGIS version boundaries, QGIS plugin workflows, spatial backend choices, provider/API licensing cautions and test criteria.
- Publish three independent agent skills: geospatial-data-discovery, qgis-plugin-development, and geospatial-web-mapping.
- Expand the general GIS development skill and English/Arabic documentation to route real development requests.
- Add offline regression tests while retaining unrelated branding, website and maintenance changes.

## 0.3.1 — 2026-10-24

- Add practical GeoLibre integration guidance covering its official agent skill, MCP server, Python API, plugin template and renderer-neutral architecture.
- Route GeoLibre-specific agent requests to the official upstream skill while keeping independent GIS QA and license rules.
- Link the new guide in English and Arabic documentation. No third-party code copied.

## 0.3.0 — 2026-10-24

- Add GeoLibre R (MIT; verified R source) and RustGIS (Apache-2.0; verified Rust workspace) with architecture and integration guide.
- Publish independently searchable 18-entry public/free GIS API reference (weather, climate, DEM, imagery, basemaps, OSM, soils, biodiversity) with explicit authentication, service limits, source terms and no-key caveats.
- Respect Open-Meteo commercial restrictions, OpenTopography personal keys, OSMF tile/Nominatim rules, and the ISRIC SoilGrids API pause.
- Add independent API catalog validation/filter scripts and regression tests.

## 0.2.0 — 2026-10-24

- Inspect exact AliAlkazraji and HIT-SIRS EarthMapper repositories, and distinguish a README-only desktop product showcase from a research paper without released model code.
- Add Windows .NET GIS architecture and GeoAI/satellite–map research reference guides.
- Curate upstream open-code projects for geometry, CRS, WebView2, imagery services, AI, and C#/.NET ArcGIS Pro SDK, including warnings for archived projects and license boundaries.
- Add automated source-availability and repo-identity regression checks.

## 0.1.0 — 2026-10-24

- Launch `gis-development` installable agent skill and six platform/domain reference modules.
- Curate initial 25 linked resources with exact owner/repo URLs and conservative license flags.
- Add ArcGIS Pro, ArcMap, QGIS, and standalone GeoJSON starter templates.
- Add zero-dependency catalog validation/search scripts and unit tests.
- Add contribution workflow and CI.
