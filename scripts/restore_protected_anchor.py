#!/usr/bin/env python3
"""Restore one logical quarter from the source and verify exact pixel equality."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageChops


def slice_box(width: int, height: int, direction: str, anchor: int) -> tuple[int, int, int, int]:
    index = anchor - 1
    if direction == "vertical":
        return (round(index * width / 4), 0, round((index + 1) * width / 4), height)
    return (0, round(index * height / 4), width, round((index + 1) * height / 4))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Paste the exact source Reality Anchor over a generated poster and verify it."
    )
    parser.add_argument("--source", required=True, type=Path, help="Original user-supplied image")
    parser.add_argument("--generated", required=True, type=Path, help="Generated poster before restoration")
    parser.add_argument("--output", required=True, type=Path, help="Final protected composite")
    parser.add_argument("--direction", required=True, choices=("vertical", "horizontal"))
    parser.add_argument("--anchor", required=True, type=int, choices=range(1, 5), metavar="{1,2,3,4}")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with Image.open(args.source) as source_image, Image.open(args.generated) as generated_image:
        source = source_image.convert("RGBA")
        generated = generated_image.convert("RGBA")
        if source.size != generated.size:
            raise SystemExit(
                f"Size mismatch: source={source.size}, generated={generated.size}. "
                "Do not resize the protected source; regenerate at the source dimensions."
            )

        box = slice_box(*source.size, args.direction, args.anchor)
        anchor_pixels = source.crop(box)
        final = generated.copy()
        final.paste(anchor_pixels, box[:2])

        restored = final.crop(box)
        if ImageChops.difference(anchor_pixels, restored).getbbox() is not None:
            raise SystemExit("Protected Anchor verification failed; output was not written.")

        args.output.parent.mkdir(parents=True, exist_ok=True)
        final.save(args.output)
        print(f"Restored and verified source pixels in anchor {args.anchor}: box={box}")


if __name__ == "__main__":
    main()
