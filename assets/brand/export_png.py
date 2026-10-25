#!/usr/bin/env python3
"""Export brand master SVGs to PNG without changing the original native vectors.

Install CairoSVG only when PNGs are needed: pip install cairosvg
Examples:
  python assets/brand/export_png.py
  python assets/brand/export_png.py --out-dir ./brand-exports
"""
from __future__ import annotations

import argparse
from pathlib import Path


PRESETS = {
    "favicon.svg": (32, 64),
    "icon.svg": (128, 256, 512),
    "logo-dark.svg": (1000, 1400),
    "logo-light.svg": (1000, 1400),
    "logo-compact-dark.svg": (850,),
    "logo-compact-light.svg": (850,),
    "banner-dark.svg": (1200, 1600),
    "banner-light.svg": (1200, 1600),
}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out-dir", type=Path, default=Path(__file__).parent / "exports")
    args = p.parse_args()
    try:
        import cairosvg
    except ImportError as exc:
        raise SystemExit("CairoSVG is required: pip install cairosvg") from exc

    root = Path(__file__).resolve().parent
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for asset, widths in PRESETS.items():
        source = root / asset
        if not source.is_file():
            raise SystemExit(f"Missing vector source: {source}")
        for width in widths:
            dest = args.out_dir / f"{source.stem}-{width}px.png"
            cairosvg.svg2png(url=str(source), write_to=str(dest), output_width=width)
            print(dest)
    print("All PNG exports are derived from the editable SVG masters.")


if __name__ == "__main__":
    main()
