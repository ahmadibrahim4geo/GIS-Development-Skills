---
name: visual-asset-discovery-integration
description: Find, inspect, prepare and integrate images, thumbnails, official logos, screenshots, illustrations, covers and backgrounds into desktop, web, mobile and other projects. Use for thumbnail, visual asset, image search, logo sourcing, preview cards, سامبنيل, ثَمبنيل, صورة مصغرة, صورة لكل اختيار, صور توضيحية or شعارات, including when a reviewed UI task needs meaningful imagery. Choose sources dynamically from the project's current website/provider and any relevant internet source; no fixed provider list or search order. Distinguish real data previews from illustrative or generated pictures.
---

# Visual Asset Discovery & Integration

Apply the [free-first policy](../../references/free-first-policy.md). Receive the reviewed goal through [GIS Development](../gis-development/SKILL.md); use [Security Guardian](../gis-security-guardian/SKILL.md), [DoneProof](../completion-evidence/SKILL.md) and [Development Journal](../agent-development-journal/SKILL.md). Support general projects as well as GIS. Treat terrain selectors as one example, not the scope boundary.

## Establish the visual brief

For each UI slot, record its subject, role, intended meaning, logical dimensions, pixel-density variants, target theme/platform, accessibility text and whether the image must be a faithful preview. Inspect the supplied example and project assets first. Keep user branding and originals unchanged.

Distinguish a command icon, a brand mark, an illustrative thumbnail and an actual data/application preview. Never silently satisfy a thumbnail/photo request with a generic icon, emoji, decorative SVG or unrelated stock picture. Use the existing icon system when the requested object really is a command icon.

## Discover and acquire

**Project-driven source selection:** derive the search from the current task, subject and project context. There is no fixed website/provider allowlist or mandatory search order. Inspect relevant images already embedded or linked in the website, documentation, product/data pages or media resources the project is using. If a suitable reusable image is there, use it directly after the normal relevance/source/terms review; do not require an unrelated image-library search first. Add, skip or replace candidate sources as the project changes, and stop when the visual brief is satisfied.

1. Inspect actual host capabilities: web/image search, HTTP/file retrieval, source-service connector, screenshot/render capture and optional image generation. Follow [MCP/native capability routing](../mcp-integration-and-tool-orchestration/SKILL.md) where needed. A SKILL.md cannot grant internet access or install tools; report a missing capability accurately.
2. Choose the appropriate route, not a rigid provider sequence:
   - **Official logo:** prefer authoritative brand/media resources; a verified matching asset from another suitable source may also be used. Verify identity, usage terms and variant. Preserve proportions, colors, clear space and alpha; never generate a replacement for an existing official mark.
   - **Data/model preview:** render or capture the actual selected data/provider when available. For scientific comparisons keep area, camera, lighting, scale and color interpretation consistent. Do not invent visible differences.
   - **Representative image:** inspect the project's current source website and any relevant internet source. Use appropriate images found inside the source's own pages directly when suitable; documentation, galleries and image indexes are optional routes. Expand subject, synonyms, language and source type when needed.
   - **Screenshot:** capture the relevant running application or use a licensed current official screenshot. Record application/version/context; never pass a mockup off as a working feature.
   - **Custom illustration:** invoke an available generation/design skill when appropriate and permitted. Label generated/illustrative material; use real data/rendering for factual map, numerical, scientific or model-specific evidence.
3. Treat [source and optional skill references](../../references/visual-asset-sources.md) as non-exhaustive examples, never required destinations or prerequisites for selecting an unlisted source. Choose relevant available tools and sources for this project. Do not auto-install external skills, keys or paid providers. Search-engine results are discovery candidates, not permission to redistribute.
4. Open the original asset page, inspect the image itself and verify relevance, authorship, reuse/derivative terms and attribution. Reject a mismatched model, watermark, uncertain license or low-quality crop. For brand marks check brand rules separately from the asset package license.
5. Download the selected asset through an authorized host tool and inspect the saved file. Respect rate limits/Retry-After and provider conditions; do not scrape a login wall or bypass a restriction. After a bounded retry, change to an appropriate source or state the exact missing input. A search card or displayed image group is not a downloaded project asset.

## Prepare and integrate

Use the [workflow, metadata and raster helper](../../references/visual-asset-workflow.md). Keep an original and create named project-local variants; use contain/padding for logos and uncropped factual previews, and an intentional crop for representative photography. Preserve transparency. Adapt formats to the target host, verify real small-size readability, and avoid unauthorized upscaling/recoloring.

Hand the target platform owner a manifest with source page/file, creator, license URL, attribution, representation type, intended use, alt text, local paths, dimensions and content hashes. Store required credits in a shipped credits/About resource; a developer-only log may not satisfy the asset's terms. Use local bundled files for offline projects, map each option to the correct asset, and preserve selected/disabled/focus states. Do not introduce a new image CDN dependency silently.

Verify packaged paths from the actual project subpath/install location, resource inclusion, offline loading, light/dark background and DPI variants. Add a sensible loading/error state without treating it as the delivered image. Image decode/readback proves only the asset, not a running target UI.

## Ownership and evidence

Own asset discovery, suitability, provenance and preparation. UI/UX owns layout/accessibility; Desktop/Web/Mobile owns resource loading and packaging; Cartography/Terrain/Remote Sensing owns scientific depiction. Request screenshots or actual data renders from their responsible host rather than replacing those owners.

Keep `request_id`, `task_id`, `asset_id` and applicable `command_id`/`trace_id` across handoffs. Record searches and inspected sources, selection reasons, rejected substitutions, acquired paths, actual tool results, tests and missing capabilities. Report independently: T0 routing/metadata; T1 local preparation/readback; T2 live source/engine; T3 actual UI; T4 packaged offline behavior. Do not claim a download, official identity, native rendering, installation or completed integration without observed evidence.

For cross-agent adapters (Cursor, Claude), see [agents](agents/README.md). For automated benchmark evaluation, run [evaluate_visual_skill.py](../../scripts/evaluate_visual_skill.py). For practical Arabic/English requests and independent acceptance scenarios, see [the example](../../examples/visual-assets/README.md).
