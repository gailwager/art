#!/usr/bin/env python3
"""Apply a tiled diagonal "© Gail Wager" watermark to the site's full-size images.

Watermarks images in images/, images/oil_paintings/, images/thumbs/ and
images/thumbs/oil_paintings/ in place. Skips images/reference/ (not shown on
the site) and the home-page hero image, which stays clean by request.

Clean originals live in the private repo (art-originals); to re-run from
scratch, restore images/ from there first, then run this script.

Usage:
    python3 tools/watermark.py [--text "© Gail Wager"] [--opacity 70] [--angle 30]
"""

import argparse
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGE_DIRS = [
    REPO_ROOT / "images",
    REPO_ROOT / "images" / "oil_paintings",
    REPO_ROOT / "images" / "thumbs",
    REPO_ROOT / "images" / "thumbs" / "oil_paintings",
]
# The home-page hero image stays un-watermarked
EXCLUDE = {REPO_ROOT / "images" / "autumn in evergreen (3).jpg"}
EXTENSIONS = {".jpg", ".jpeg", ".png"}
FONT_PATH = "/System/Library/Fonts/Helvetica.ttc"


def make_overlay(size, text, opacity, angle, font_scale):
    """Build a transparent layer with the text tiled diagonally across it."""
    w, h = size
    diag = int(math.hypot(w, h)) + 8
    layer = Image.new("RGBA", (diag, diag), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    font_size = max(18, int(w * font_scale))
    font = ImageFont.truetype(FONT_PATH, font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]

    x_step = int(text_w * 1.6)
    y_step = int(text_h * 4.5)
    shadow = max(1, font_size // 30)

    row = 0
    for y in range(0, diag, y_step):
        # Offset alternate rows so marks don't line up in columns
        x0 = -(x_step // 2) if row % 2 else 0
        for x in range(x0, diag, x_step):
            # Dark under-layer then light text, so the mark reads on both
            # light and dark areas of a painting
            draw.text((x + shadow, y + shadow), text, font=font,
                      fill=(0, 0, 0, opacity // 2))
            draw.text((x, y), text, font=font,
                      fill=(255, 255, 255, opacity))
        row += 1

    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=False)
    left = (diag - w) // 2
    top = (diag - h) // 2
    return layer.crop((left, top, left + w, top + h))


def watermark_file(path, text, opacity, angle, font_scale):
    with Image.open(path) as im:
        fmt = im.format
        im = ImageOps.exif_transpose(im)
        base = im.convert("RGBA")
        overlay = make_overlay(base.size, text, opacity, angle, font_scale)
        out = Image.alpha_composite(base, overlay)
        if fmt == "PNG":
            out.save(path, format="PNG")
        else:
            out.convert("RGB").save(path, format="JPEG", quality=88,
                                    optimize=True, progressive=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", default="© Gail Wager")
    parser.add_argument("--opacity", type=int, default=70,
                        help="text alpha 0-255 (default 70)")
    parser.add_argument("--angle", type=float, default=30.0)
    parser.add_argument("--font-scale", type=float, default=0.045,
                        help="font size as a fraction of image width")
    parser.add_argument("files", nargs="*", type=Path,
                        help="specific files to watermark (default: all)")
    args = parser.parse_args()

    if args.files:
        targets = args.files
    else:
        targets = sorted(
            p for d in IMAGE_DIRS for p in d.iterdir()
            if p.is_file() and p.suffix.lower() in EXTENSIONS
            and p not in EXCLUDE
        )

    failed = []
    for path in targets:
        try:
            watermark_file(path, args.text, args.opacity, args.angle,
                           args.font_scale)
            try:
                shown = path.relative_to(REPO_ROOT)
            except ValueError:
                shown = path
            print(f"watermarked  {shown}")
        except Exception as exc:
            failed.append(path)
            print(f"FAILED       {path}: {exc}", file=sys.stderr)

    print(f"\n{len(targets) - len(failed)} watermarked, {len(failed)} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
