# Claude Integration — Visual Asset Discovery & Integration

Instructions for integrating this skill into **Claude Code**, **Claude Desktop**, or custom Claude Projects.

## System Prompt Addendum

When handling UI tasks that require images, logos, thumbnails, or previews, inject the following prompt instruction:

```markdown
You are equipped with the Visual Asset Discovery & Integration capability.
When a user asks for visual assets, thumbnails, logos, or UI imagery:
1. Distinguish between official logos (brand-mark), factual data previews (actual-preview), and illustrative photography.
2. Never hallucinate image URLs or use external hotlinks that break offline.
3. Never generate AI images for established real-world brands or official organizations; source their verified vector or transparent raster assets.
4. Verify license permissions and maintain attribution in a local asset manifest.
5. Save assets locally and verify rendered dimensions, alpha transparency, and Retina 2x variants.
```

## Tool Integration Guidance

If Claude has access to Bash or local tools:
- Use `scripts/prepare_visual_asset.py` to deterministically create lossless variants, strip EXIF data, and compute SHA-256 hashes:
  ```bash
  python scripts/prepare_visual_asset.py --input /path/to/source.png --metadata /path/to/metadata.json --output-dir /path/to/dest --width 64 --height 64 --scales 1 2 --fit contain
  ```
- Reject any attempt to crop logos or upscale images beyond their native resolution.
