#!/usr/bin/env python3
"""Create optional restoration candidates after an external Face Restoration Gate."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


Box = tuple[int, int, int, int]


def slice_box(width: int, height: int, direction: str, anchor: int) -> Box:
    index = anchor - 1
    if direction == "vertical":
        return (round(index * width / 4), 0, round((index + 1) * width / 4), height)
    return (0, round(index * height / 4), width, round((index + 1) * height / 4))


def valid_box(box: Box, size: tuple[int, int]) -> bool:
    left, top, right, bottom = box
    return 0 <= left < right <= size[0] and 0 <= top < bottom <= size[1]


def face_core_composite(source: Image.Image, candidate: Image.Image, box: Box, feather: int) -> Image.Image:
    if not valid_box(box, source.size):
        raise SystemExit(f"Invalid face box {box} for image size {source.size}.")

    mask = Image.new("L", source.size, 0)
    if feather > 0:
        left, top, right, bottom = box
        outer = (
            max(0, left - feather),
            max(0, top - feather),
            min(source.width, right + feather),
            min(source.height, bottom + feather),
        )
        ImageDraw.Draw(mask).rectangle(outer, fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(max(1, feather / 2)))

    ImageDraw.Draw(mask).rectangle(box, fill=255)
    final = Image.composite(source, candidate, mask)
    if ImageChops.difference(source.crop(box), final.crop(box)).getbbox() is not None:
        raise SystemExit("Face-core pixel verification failed; output was not written.")
    return final


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create an optional restoration candidate with explicit face-gate and geometry safeguards."
    )
    parser.add_argument("--source", required=True, type=Path, help="Original user-supplied image")
    parser.add_argument("--generated", required=True, type=Path, help="Visually coherent candidate")
    parser.add_argument("--output", required=True, type=Path, help="Protected composite candidate")
    parser.add_argument("--mode", required=True, choices=("face-mask", "face-core", "source-mask", "full-anchor"))
    parser.add_argument("--face-box", nargs=4, type=int, metavar=("X0", "Y0", "X1", "Y1"))
    parser.add_argument("--mask", type=Path, help="Grayscale or alpha mask for an irregular Reality module")
    parser.add_argument("--aligned-source", type=Path, help="Geometrically registered source image for face restoration")
    parser.add_argument("--face-gate-failed", action="store_true", help="Confirm Candidate A failed the Face Restoration Gate")
    parser.add_argument("--alignment-verified", action="store_true", help="Confirm source-to-candidate face geometry was verified")
    parser.add_argument("--mask-excludes-primary-face", action="store_true", help="Confirm a source-mask has zero coverage over the primary face")
    parser.add_argument("--no-primary-face", action="store_true", help="Confirm full-anchor restoration cannot overwrite a primary face")
    parser.add_argument("--feather", type=int, default=0, help="Blend ring outside exact face core")
    parser.add_argument("--direction", choices=("vertical", "horizontal"))
    parser.add_argument("--anchor", type=int, choices=range(1, 5), metavar="{1,2,3,4}")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.feather < 0:
        raise SystemExit("--feather must be non-negative.")
    if args.mode in ("face-mask", "face-core") and not args.face_gate_failed:
        raise SystemExit("Face restoration is conditional; pass --face-gate-failed only after Candidate A fails the gate.")
    if args.mode in ("face-mask", "face-core") and not args.alignment_verified:
        raise SystemExit("Pixel-level face restoration requires verified source-to-candidate geometry; pass --alignment-verified only after checking alignment.")
    if args.aligned_source is not None and not args.alignment_verified:
        raise SystemExit("--aligned-source requires --alignment-verified.")
    if args.mode == "source-mask" and not args.mask_excludes_primary_face:
        raise SystemExit("--mode source-mask requires --mask-excludes-primary-face so it cannot bypass the Face Restoration Gate.")
    if args.mode == "full-anchor" and not args.no_primary_face:
        raise SystemExit("--mode full-anchor is restricted to scenes confirmed to have no primary face; pass --no-primary-face.")

    with Image.open(args.source) as source_image, Image.open(args.generated) as candidate_image:
        source = source_image.convert("RGBA")
        candidate = candidate_image.convert("RGBA")
        if source.size != candidate.size:
            raise SystemExit(
                f"Size mismatch: source={source.size}, candidate={candidate.size}. "
                "Do not resize the protected source."
            )

        restoration_source = source
        if args.aligned_source is not None:
            with Image.open(args.aligned_source) as aligned_image:
                restoration_source = aligned_image.convert("RGBA")
            if restoration_source.size != candidate.size:
                raise SystemExit("Aligned source size does not match candidate size.")

        if args.mode == "face-mask":
            if args.mask is None:
                raise SystemExit("--mask is required for --mode face-mask.")
            with Image.open(args.mask) as mask_image:
                if mask_image.size != candidate.size:
                    raise SystemExit(f"Mask size {mask_image.size} does not match image size {candidate.size}.")
                mask = mask_image.getchannel("A") if "A" in mask_image.getbands() else mask_image.convert("L")
            final = Image.composite(restoration_source, candidate, mask)
            message = "Created gated irregular face-restoration candidate; compare it against Candidate A"
        elif args.mode == "face-core":
            if args.face_box is None:
                raise SystemExit("--face-box is required for --mode face-core.")
            box = tuple(args.face_box)
            final = face_core_composite(restoration_source, candidate, box, args.feather)
            message = f"Created last-fallback rectangular face candidate: box={box}, feather={args.feather}"
        elif args.mode == "source-mask":
            if args.mask is None:
                raise SystemExit("--mask is required for --mode source-mask.")
            with Image.open(args.mask) as mask_image:
                if mask_image.size != source.size:
                    raise SystemExit(f"Mask size {mask_image.size} does not match image size {source.size}.")
                mask = mask_image.getchannel("A") if "A" in mask_image.getbands() else mask_image.convert("L")
            final = Image.composite(source, candidate, mask)
            message = f"Restored irregular source Reality module from mask: {args.mask}"
        else:
            if args.direction is None or args.anchor is None:
                raise SystemExit("--direction and --anchor are required for --mode full-anchor.")
            box = slice_box(*source.size, args.direction, args.anchor)
            anchor_pixels = source.crop(box)
            final = candidate.copy()
            final.paste(anchor_pixels, box[:2])
            if ImageChops.difference(anchor_pixels, final.crop(box)).getbbox() is not None:
                raise SystemExit("Full-Anchor pixel verification failed; output was not written.")
            message = f"Restored and verified full source Anchor: anchor={args.anchor}, box={box}"

        args.output.parent.mkdir(parents=True, exist_ok=True)
        final.save(args.output)
        print(message)


if __name__ == "__main__":
    main()
