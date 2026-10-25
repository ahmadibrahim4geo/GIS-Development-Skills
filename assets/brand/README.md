# GIS Development Skills — official brand identity

**Identity:** GIS Development Skills  
**Tagline:** The Heart of Geospatial Innovation

This is the user-approved **Layered Map** concept, faithfully rebuilt as **native editable SVG vectors**. Paths, circles, rectangles and SVG text are separate vector elements; there are **no embedded PNG, WebP, bitmap textures, gradients, shadows or background rectangles inside transparent logos**.

## Assets

| Asset | Purpose |
| --- | --- |
| `logo-dark.svg` | Full transparent identity for dark website/page surfaces |
| `logo-light.svg` | Full transparent identity for light surfaces |
| `banner-dark.svg` | Solid charcoal, responsive GitHub README/banner |
| `banner-light.svg` | Solid white alternate banner |
| `logo-compact-dark.svg` | Compact horizontal logo for dark navigation |
| `logo-compact-light.svg` | Compact horizontal logo for light navigation |
| `icon.svg` | Independent editable vector map-layers icon |
| `favicon.svg` | Lightweight favicon variant |
| `palette.json` | Stable names, hex codes and typographic rules |

## Exact palette (flat fills only)

- **Dark blue:** `#0B3D91` — mapping, base layer, dark typography.
- **Blue:** `#1467C8` — primary brand blue on light backgrounds.
- **Readable blue on dark:** `#398CE3` — the same blue family at higher contrast for G and Geospatial on charcoal.
- **Cyan:** `#1CC8E8` — map route, GIS S, Innovation and middle layer.
- **Green:** `#82D53E` — waypoint, I dot, Skills and Heart.
- **White:** `#FFFFFF` — top map tile, white main text on dark mode.
- **Charcoal:** `#101B24` — dark *banner background only*, not the transparent SVG.

**Letters**: G blue, I white on dark/navy on light with a green dot, S cyan. Development white on dark/navy on light; Skills green. The tagline uses five independently editable SVG text objects: **The** white/navy, **Heart** green, **of** white/navy, **Geospatial** blue, **Innovation** cyan.

## Visual gallery and PNG raster exports

- [Brand showcase](showcase.html) — side-by-side preview for dark, light, compact and icon-only variants.
- [Design tokens](tokens.css) — centralized flat-color CSS custom properties.
- [PNG export utility](export_png.py) — optional local creation of raster assets (favicon 32/64px, icon 128/256/512px, logo and banner widths) using CairoSVG. It writes to `exports/` and **never replaces SVG source files**.

## Editing & exporting

- Open `logo-dark.svg` / `logo-light.svg` in Inkscape, Illustrator, or an SVG-capable editor. Recolor path fills and individual text nodes, then save as SVG.
- Keep the **full name and tagline exactly unchanged** and always preserve icon proportions.
- SVG text uses Inter with Arial fallback. For font-independent print delivery, convert text to outlines in your editor; keep an editable master copy.
- Use `logo-dark.svg` on dark backgrounds and `logo-light.svg` on light backgrounds. Use `banner-dark.svg` for repository documentation.
- Do not rebuild the SVG by embedding raster files. Raster PNG exports can be created as needed from these SVG masters.

## Typography and non-overlap rule

**Do not give `Skills` a hardcoded SVG `x` coordinate.** The two name words now share one `<text id="brand-name">` element with consecutive `<tspan>` children. SVG computes the starting position of `Skills` from the *actual rendered width* of `Development` for the viewer's available font and then applies a positive `dx` gap. The five colored tagline words follow the same rule inside `<text id="brand-tagline">`.

This design prevents the recurring **Development/Skills collision** in large, compact, dark and light outputs and prevents color-word collisions when fonts differ across GitHub, Windows, browsers and image renderers. When editing font family, weight or size, keep this flowed tspan structure. The regression tests in `tests/test_landing_page.py` and `tests/test_readme_layout.py` enforce it. Do not convert consecutive words back to separately hardcoded absolute `x` values.

## Layout and reuse

- All transparent logo and icon SVGs retain **transparent backgrounds**.
- Avoid applying CSS `object-fit: cover`, forced square cropping, or duplicate HTML text over the logo.
- The `index.html` hero, navigation, social preview and English/Arabic README should use the assets from this folder.
- This identity is project artwork; third-party branding in source catalogs retains its own licensing.
