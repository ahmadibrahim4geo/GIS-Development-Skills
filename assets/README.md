# GIS Development Skills — Visual Identity

**Approved direction:** Concept 02 — **Layered Geospatial G**.

**Primary name:** GIS Development Skills  
**Slogan:** The Heart of Geospatial Innovation  
**Arabic meaning:** قلب الابتكار في التقنيات الجغرافية

The design is based on the author's selected concept featuring a cyan-to-mint **G** over two tilted geospatial layers: a topographic contour sheet and a coordinate grid. These layers connect the visual identity to real GIS workflows instead of relying on a generic globe or location pin.

## Canonical assets

| File | Purpose |
|---|---|
| [logo.svg](logo.svg) | Full name + approved slogan, used at the top of the English and Arabic READMEs. The website hero uses semantic HTML wordmark text for reliable typography |
| [icon.svg](icon.svg) | Compact layered G used by the navigation header and browser favicon |
| [brand-refresh.css](brand-refresh.css) | Responsive presentation styling, consistent with the same colors |
| [../index.html](../index.html) | Live landing page layout, headings, catalog and creator section |

**Important correction (2026-10-24):** The earlier hand-drawn SVG G did not visually match the approved concept. Both SVG files now embed the **same raster asset scaled from the approved Layered Geospatial G image**, so the icon stays consistent. These are SVG containers with raster icon content, **not fully vector versions of the illustrated symbol**. The full brand wordmark in `logo.svg` remains SVG text, while the website hero deliberately uses styled HTML text to avoid stretched letters or excessive fixed character spacing. The full-size concept image remains in the design conversation, not in the repository.

## Brand language

- Dark background: `#101B23`
- Primary cyan: `#0BC2EA`
- Middle turquoise: `#23DED0`
- Mint-green highlight: `#B2FC92`
- Primary text: `#F5F9FB`
- Secondary text: `#B2CED5`

Avoid competing design motifs (a standalone globe, giant pin, or unrelated contour G). Use the **same layered G** on GitHub, the homepage, social presentations and small-screen icons. Keep the full name readable independently of the logo on accessible pages. Avoid custom `letter-spacing` on the big wordmark; support reflow on mobile without stretching the G.

## Non-negotiable wording

Display the approved slogan immediately below the project name:

> The Heart of Geospatial Innovation

And **preserve this original project-purpose line verbatim** immediately below the website hero logo and near the start of `README.md`:

> Build GIS tools, plugins and geospatial applications with a verifiable development workflow.

## How to update branding

1. Refine the approved **Layered Geospatial G** only; do not silently replace it with another logo proposal.
2. Update `logo.svg` and `icon.svg` in the same change.
3. Keep `index.html` and `assets/brand-refresh.css` synchronized.
4. Confirm Arabic RTL language handling and mobile width, plus readable GitHub README previews.
5. Run `python -m unittest discover -s tests -v` and inspect GitHub Pages deployment.

The repository's external About image / social preview is a separate GitHub administrator UI setting. It is not changed simply by committing these SVGs.
