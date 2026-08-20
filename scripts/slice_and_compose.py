#!/usr/bin/env python3
"""Deterministic four-zone slicing and compositing for the Four-Slice Reality Poster.

The image model never decides the slicing. This script:

- defines the four exact integer zones (vertical or horizontal) that tile the
  source at its original size with no gaps or overlaps (--mode prepare);
- writes one per-zone context crop for separate rendering (Scheme A) and
  optional full-canvas inpaint masks (Scheme B);
- composes the final poster by pasting rendered zones back at fixed
  coordinates, always keeping the Reality Anchor pasted from the source
  (--mode compose / --mode enforce-anchor);
- verifies that the output is one continuous source-ratio image whose scene
  appears exactly once, with the anchor region unchanged (--mode verify).

Any layout where the whole photograph is repeated (2x2 grid, strip, contact
sheet) is geometrically impossible in the output of this script.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from PIL import Image, ImageChops, ImageDraw, ImageFilter

Box = Tuple[int, int, int, int]
LEVELS = (30, 65, 90)


def exact_edges(size: int, n: int = 4) -> List[int]:
    """Split [0, size] into n integer segments that tile exactly (no gaps/overlap)."""
    if size < n:
        raise SystemExit(f"Image dimension {size} is too small for {n} slices.")
    base, rem = divmod(size, n)
    return [i * base + min(i, rem) for i in range(n + 1)]


def zones_for(direction: str, width: int, height: int) -> List[Box]:
    if direction == "vertical":
        xs = exact_edges(width, 4)
        return [(xs[i], 0, xs[i + 1], height) for i in range(4)]
    ys = exact_edges(height, 4)
    return [(0, ys[i], width, ys[i + 1]) for i in range(4)]


def overlap_area(zone: Box, box: Box) -> int:
    x0, y0, x1, y1 = zone
    bx0, by0, bx1, by1 = box
    ix0, iy0 = max(x0, bx0), max(y0, by0)
    ix1, iy1 = min(x1, bx1), min(y1, by1)
    if ix1 <= ix0 or iy1 <= iy0:
        return 0
    return (ix1 - ix0) * (iy1 - iy0)


def pick_anchor(zones: List[Box], face_boxes: List[Box]) -> int:
    """0-based anchor index. Fallback is Logical Zone 2 (second from left/top)."""
    if not face_boxes:
        return 1
    best, best_area = 0, -1
    for i, zone in enumerate(zones):
        area = sum(overlap_area(zone, fb) for fb in face_boxes)
        if area > best_area:
            best, best_area = i, area
    return best


def assign_levels(anchor: int, levels: List[int]) -> Dict[int, int]:
    non_anchor = [i for i in range(4) if i != anchor]
    return {zone: level for zone, level in zip(non_anchor, levels)}


def crop_box_for(zone: Box, direction: str, width: int, height: int, margin: float) -> Box:
    x0, y0, x1, y1 = zone
    if direction == "vertical":
        m = int(margin * (x1 - x0))
        return (max(0, x0 - m), 0, min(width, x1 + m), height)
    m = int(margin * (y1 - y0))
    return (0, max(0, y0 - m), width, min(height, y1 + m))


def parse_face_boxes(raw: Optional[str]) -> List[Box]:
    if not raw:
        return []
    boxes: List[Box] = []
    for part in raw.split(";"):
        part = part.strip()
        if not part:
            continue
        vals = [int(v) for v in part.split(",")]
        if len(vals) != 4:
            raise SystemExit(f"Invalid face box {part!r}; expected x0,y0,x1,y1.")
        boxes.append(tuple(vals))
    return boxes


def load_manifest(workdir: Path) -> dict:
    path = Path(workdir) / "manifest.json"
    if not path.is_file():
        raise SystemExit(f"No manifest.json in {workdir}; run --mode prepare first.")
    return json.loads(path.read_text())


def save_output(canvas: Image.Image, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output)


def pixels_differ(a: Image.Image, b: Image.Image) -> bool:
    """True when two images differ in any color band.

    Image.getbbox() on RGBA images only inspects the alpha band, so compare in
    RGB to catch real pixel changes.
    """
    return ImageChops.difference(a.convert("RGB"), b.convert("RGB")).getbbox() is not None


def enforce_anchor(canvas: Image.Image, source: Path, manifest: dict) -> None:
    anchor = manifest["anchor"] - 1
    zone = tuple(manifest["zones"][anchor]["box"])
    with Image.open(source) as im:
        src = im.convert("RGBA")
    if src.size != canvas.size:
        raise SystemExit("Source/canvas size mismatch in anchor enforcement.")
    canvas.paste(src.crop(zone), zone[:2])
    if pixels_differ(src.crop(zone), canvas.crop(zone)):
        raise SystemExit("Anchor pixel verification failed; output was not written.")


def cmd_prepare(args: argparse.Namespace) -> None:
    source = Path(args.source)
    if not source.is_file():
        raise SystemExit(f"Source not found: {source}")
    with Image.open(source) as im:
        width, height = im.size
    zones = zones_for(args.direction, width, height)

    if args.anchor == "auto":
        anchor = pick_anchor(zones, args.face_boxes)
    else:
        anchor = int(args.anchor) - 1  # CLI is 1-based like restore_protected_anchor.py

    if sorted(args.levels) != sorted(LEVELS):
        raise SystemExit(f"--levels must be a permutation of {list(LEVELS)}; got {args.levels}")
    level_map = assign_levels(anchor, args.levels)

    workdir = Path(args.workdir)
    crops_dir = workdir / "crops"
    masks_dir = workdir / "masks"
    rendered_dir = workdir / "rendered"
    for d in (crops_dir, masks_dir, rendered_dir):
        d.mkdir(parents=True, exist_ok=True)

    manifest_zones = []
    with Image.open(source) as im:
        img = im.convert("RGBA")
        for i, zone in enumerate(zones):
            crop_box = crop_box_for(zone, args.direction, width, height, args.margin)
            crop = img.crop(crop_box)
            crop_path = crops_dir / f"zone{i}.png"
            crop.save(crop_path)
            mask_path = None
            if args.masks:
                mask = Image.new("L", (width, height), 0)
                ImageDraw.Draw(mask).rectangle(zone, fill=255)
                mask_path = masks_dir / f"mask_zone{i}.png"
                mask.save(mask_path)
            manifest_zones.append(
                {
                    "index": i,
                    "box": list(zone),
                    "crop_box": list(crop_box),
                    "crop": str(crop_path),
                    "mask": str(mask_path) if mask_path else None,
                    "level": "anchor" if i == anchor else level_map[i],
                    "rendered": str(rendered_dir / f"zone{i}.png"),
                }
            )

    manifest = {
        "source": str(source),
        "direction": args.direction,
        "size": [width, height],
        "anchor": anchor + 1,
        "margin": args.margin,
        "zones": manifest_zones,
    }
    manifest_path = workdir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))

    print(f"Prepared deterministic four-zone layout -> {manifest_path}")
    print(f"Direction={args.direction}  size={width}x{height}  anchor=Logical Zone {anchor + 1}")
    for z in manifest_zones:
        kind = "anchor" if z["level"] == "anchor" else f"{z['level']}% abstraction"
        print(
            f"  zone {z['index'] + 1}: {kind} | box={tuple(z['box'])} | "
            f"crop={z['crop']} | rendered={z['rendered']}"
            + (f" | mask={z['mask']}" if z["mask"] else "")
        )
    print("Render each abstract zone crop with the per-zone prompt block, then run --mode compose.")


def cmd_compose(args: argparse.Namespace) -> None:
    manifest = load_manifest(args.workdir)
    source = Path(manifest["source"])
    with Image.open(source) as im:
        canvas = im.convert("RGBA")
    if canvas.size != tuple(manifest["size"]):
        raise SystemExit("Source changed since prepare; re-run --mode prepare.")

    rendered_dir = Path(args.rendered_dir)
    for z in manifest["zones"]:
        if z["level"] == "anchor":
            continue
        rendered_path = Path(z["rendered"])
        if not rendered_path.is_file():
            rendered_path = rendered_dir / f"zone{z['index']}.png"
        if not rendered_path.is_file():
            raise SystemExit(f"Missing rendered zone {z['index'] + 1}: {rendered_path}")
        with Image.open(rendered_path) as ri:
            rendered = ri.convert("RGBA")
        crop_box = tuple(z["crop_box"])
        zone = tuple(z["box"])
        cw, ch = crop_box[2] - crop_box[0], crop_box[3] - crop_box[1]
        if rendered.size != (cw, ch):
            rendered = rendered.resize((cw, ch), Image.LANCZOS)
        rel = (
            zone[0] - crop_box[0],
            zone[1] - crop_box[1],
            zone[2] - crop_box[0],
            zone[3] - crop_box[1],
        )
        region = rendered.crop(rel)
        if args.feather > 0:
            mask = Image.new("L", (zone[2] - zone[0], zone[3] - zone[1]), 255)
            mask = mask.filter(ImageFilter.GaussianBlur(args.feather))
            canvas.paste(region, (zone[0], zone[1]), mask)
        else:
            canvas.paste(region, (zone[0], zone[1]))
        print(f"Pasted zone {z['index'] + 1} at {zone[:2]} level={z['level']}")

    enforce_anchor(canvas, source, manifest)
    save_output(canvas, Path(args.output))
    print(f"Composed one continuous poster -> {args.output}")


def cmd_enforce_anchor(args: argparse.Namespace) -> None:
    manifest = load_manifest(args.workdir)
    with Image.open(args.candidate) as im:
        canvas = im.convert("RGBA")
    if canvas.size != tuple(manifest["size"]):
        raise SystemExit(f"Candidate size {canvas.size} does not match {tuple(manifest['size'])}.")
    enforce_anchor(canvas, Path(manifest["source"]), manifest)
    save_output(canvas, Path(args.output))
    print(f"Anchor (Logical Zone {manifest['anchor']}) enforced from source -> {args.output}")


def cmd_verify(args: argparse.Namespace) -> None:
    manifest = load_manifest(args.workdir)
    output = Path(args.output)
    if not output.is_file():
        raise SystemExit(f"Output not found: {output}")
    with Image.open(output) as im:
        out = im.convert("RGBA")
    width, height = manifest["size"]
    if out.size != (width, height):
        raise SystemExit(f"Size mismatch: output={out.size}, expected {(width, height)}")
    with Image.open(manifest["source"]) as im:
        src = im.convert("RGBA")

    zones = manifest["zones"]
    if manifest["direction"] == "vertical":
        xs = sorted({z["box"][0] for z in zones} | {z["box"][2] for z in zones})
        if xs != exact_edges(width, 4):
            raise SystemExit("Zones do not tile the full width exactly.")
    else:
        ys = sorted({z["box"][1] for z in zones} | {z["box"][3] for z in zones})
        if ys != exact_edges(height, 4):
            raise SystemExit("Zones do not tile the full height exactly.")

    anchor = manifest["anchor"] - 1
    zone = tuple(zones[anchor]["box"])
    if pixels_differ(src.crop(zone), out.crop(zone)):
        raise SystemExit("Anchor region differs from source; layout guarantee broken.")

    for z in zones:
        if z["level"] == "anchor":
            continue
        box = tuple(z["box"])
        if not pixels_differ(src.crop(box), out.crop(box)):
            print(f"  warning: zone {z['index'] + 1} is pixel-identical to its source slice; "
                  "no abstraction appears to have been applied.")

    print(
        f"Verified: one continuous {width}x{height} image, 4 exactly-tiled regions, "
        f"anchor (zone {anchor + 1}) == source, scene appears once."
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--mode", required=True, choices=("prepare", "compose", "enforce-anchor", "verify"))
    parser.add_argument("--source", type=Path, help="Original user-supplied image")
    parser.add_argument("--output", type=Path, help="Final poster path (compose/enforce-anchor/verify)")
    parser.add_argument(
        "--workdir",
        type=Path,
        default=Path("four-slice-work"),
        help="Directory holding manifest, crops, masks, and rendered zones",
    )
    parser.add_argument("--direction", choices=("vertical", "horizontal"), help="Slice direction (prepare)")
    parser.add_argument(
        "--anchor",
        default="auto",
        help="auto | 1..4 (1-based Logical Zone); auto = largest face-box overlap, else Logical Zone 2",
    )
    parser.add_argument(
        "--face-boxes",
        help='Semicolon list of x0,y0,x1,y1 boxes, e.g. "10,20,80,140;200,30,260,150"',
    )
    parser.add_argument(
        "--levels",
        default="30,65,90",
        help="Permutation of 30,65,90 assigned in spatial order to the three non-anchor zones",
    )
    parser.add_argument(
        "--margin",
        type=float,
        default=0.12,
        help="Context margin around each zone crop, as a fraction of the zone's slice width/height",
    )
    parser.add_argument(
        "--masks",
        action="store_true",
        help="prepare also writes full-canvas inpaint masks (Scheme B)",
    )
    parser.add_argument(
        "--rendered-dir",
        type=Path,
        help="Directory with rendered zone images (compose); defaults to workdir/rendered",
    )
    parser.add_argument(
        "--candidate",
        type=Path,
        help="Full-canvas inpainted candidate (enforce-anchor)",
    )
    parser.add_argument(
        "--feather",
        type=int,
        default=0,
        help="Optional small blur ring in px for pasted zone edges (0 = hard edge)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.feather < 0:
        raise SystemExit("--feather must be non-negative.")
    if args.mode == "prepare":
        if args.source is None or args.direction is None:
            raise SystemExit("--source and --direction are required for --mode prepare.")
        args.face_boxes = parse_face_boxes(args.face_boxes)
        args.levels = [int(x) for x in args.levels.split(",")]
        cmd_prepare(args)
    elif args.mode == "compose":
        if args.output is None:
            raise SystemExit("--output is required for --mode compose.")
        args.rendered_dir = args.rendered_dir or (args.workdir / "rendered")
        cmd_compose(args)
    elif args.mode == "enforce-anchor":
        if args.output is None or args.candidate is None:
            raise SystemExit("--output and --candidate are required for --mode enforce-anchor.")
        cmd_enforce_anchor(args)
    else:
        if args.output is None:
            raise SystemExit("--output is required for --mode verify.")
        cmd_verify(args)


if __name__ == "__main__":
    main()
