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
- **Blue:** `#1467C8` — GIS G and Geospatial.
- **Cyan:** `#1CC8E8` — map route, GIS S, Innovation and middle layer.
- **Green:** `#82D53E` — waypoint, I dot, Skills and Heart.
- **White:** `#FFFFFF` — top map tile, white main text on dark mode.
- **Charcoal:** `#101B24` — dark *banner background only*, not the transparent SVG.

**Letters**: G blue, I white on dark/navy on light with a green dot, S cyan. Development white on dark/navy on light; Skills green. The tagline uses five independently editable SVG text objects: **The** white/navy, **Heart** green, **of** white/navy, **Geospatial** blue, **Innovation** cyan.

## Editing & exporting

- Open `logo-dark.svg` / `logo-light.svg` in Inkscape, Illustrator, or an SVG-capable editor. Recolor path fills and individual text nodes, then save as SVG.
- Keep the **full name and tagline exactly unchanged** and always preserve icon proportions.
- SVG text uses Inter with Arial fallback. For font-independent print delivery, convert text to outlines in your editor; keep an editable master copy.
- Use `logo-dark.svg` on dark backgrounds and `logo-light.svg` on light backgrounds. Use `banner-dark.svg` for repository documentation.
- Do not rebuild the SVG by embedding raster files. Raster PNG exports can be created as needed from these SVG masters.

## Layout and reuse

- All transparent logo and icon SVGs retain **transparent backgrounds**.
- Avoid applying CSS `object-fit: cover`, forced square cropping, or duplicate HTML text over the logo.
- The `index.html` hero, navigation, social preview and English/Arabic README should use the assets from this folder.
- This identity is project artwork; third-party branding in source catalogs retains its own licensing.
