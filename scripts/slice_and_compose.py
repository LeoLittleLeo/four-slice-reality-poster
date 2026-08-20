#!/usr/bin/env python3
"""Deterministic four-zone slicing and compositing for the Four-Slice Reality Poster.

The image model never decides the slicing. This script:

- defines four regions that tile the source exactly (no gaps, no overlaps):
  * --boundary rect     -> four equal vertical/horizontal strips (integer coords)
  * --boundary contour  -> contour-aware irregular regions whose boundaries
                           follow strong edges while staying off faces and
                           within a balance band (default)
  * --boundary mask     -> four content-aware masks supplied by the agent,
                           normalized to exact tiling automatically
- writes one per-zone context crop for separate rendering (Scheme A) and the
  zone masks used for masked compositing and for full-canvas inpaint
  (Scheme B);
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
from collections import deque
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from PIL import Image, ImageChops, ImageDraw, ImageFilter

Box = Tuple[int, int, int, int]
LEVELS = (30, 65, 90)
BIG = 10 ** 6        # face penalty weight
STEP = 6             # max column change per row in boundary path search
BALANCE_RATIO = 2.5  # warn when max/min zone area ratio exceeds this


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


# ---------------------------------------------------------------------------
# Boundary construction
# ---------------------------------------------------------------------------

def rect_masks(direction: str, width: int, height: int) -> List[Image.Image]:
    masks = []
    for (x0, y0, x1, y1) in zones_for(direction, width, height):
        m = Image.new("L", (width, height), 0)
        ImageDraw.Draw(m).rectangle((x0, y0, x1 - 1, y1 - 1), fill=255)
        masks.append(m)
    return masks


def edge_and_face_images(source: Path, width: int, height: int,
                         face_boxes: List[Box]) -> Tuple[Image.Image, Image.Image]:
    with Image.open(source) as im:
        gray = im.convert("L")
    edges = gray.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.GaussianBlur(5))
    face = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(face)
    for (x0, y0, x1, y1) in face_boxes:
        pad = 10
        draw.rectangle(
            (max(0, x0 - pad), max(0, y0 - pad), min(width - 1, x1 + pad), min(height - 1, y1 + pad)),
            fill=255,
        )
    return edges, face


def rotated_face_boxes(face_boxes: List[Box], width: int, height: int) -> List[Box]:
    """Rotate 90 degrees counterclockwise: (x, y) -> (y, width - 1 - x)."""
    return [(y0, width - 1 - x1, y1, width - 1 - x0) for (x0, y0, x1, y1) in face_boxes]


def sliding_max_arg(arr: List[float], step: int) -> List[int]:
    """For each i, index of max(arr[max(0,i-step)..i])."""
    n = len(arr)
    out = [0] * n
    dq: deque = deque()
    for i in range(n):
        while dq and arr[dq[-1]] <= arr[i]:
            dq.pop()
        dq.append(i)
        while dq and dq[0] < i - step:
            dq.popleft()
        out[i] = dq[0]
    return out


def sliding_max_arg_rev(arr: List[float], step: int) -> List[int]:
    """For each i, index of max(arr[i..min(n-1,i+step)])."""
    n = len(arr)
    out = [0] * n
    dq: deque = deque()
    for i in range(n - 1, -1, -1):
        while dq and arr[dq[-1]] <= arr[i]:
            dq.pop()
        dq.append(i)
        while dq and dq[0] > i + step:
            dq.popleft()
        out[i] = dq[0]
    return out


def optimize_boundary(edge_data: bytes, face_data: bytes, stride: int,
                      lo: int, hi: int, step: int,
                      lb: Optional[List[int]]) -> List[int]:
    """Best top-to-bottom path within [lo, hi] maximizing edge strength.

    Penalizes passing through face pixels (BIG) and keeps a per-row lower
    bound `lb` so consecutive boundaries cannot cross or collapse.
    Returns one x value per row.
    """
    height = len(edge_data) // stride
    ncols = hi - lo + 1
    NEG = float("-inf")
    prev = [NEG] * ncols
    back: List[List[int]] = [[0] * ncols for _ in range(height)]
    first = edge_data[:stride]
    first_face = face_data[:stride]
    for c in range(ncols):
        x = lo + c
        prev[c] = first[x] - (BIG if first_face[x] else 0)
    for r in range(1, height):
        e_row = edge_data[r * stride:(r + 1) * stride]
        f_row = face_data[r * stride:(r + 1) * stride]
        fidx = sliding_max_arg(prev, step)
        bidx = sliding_max_arg_rev(prev, step)
        winidx = [fidx[i] if prev[fidx[i]] >= prev[bidx[i]] else bidx[i] for i in range(ncols)]
        winmax = [prev[winidx[i]] for i in range(ncols)]
        cur = [NEG] * ncols
        lb_r = lb[r] if lb is not None else lo
        if lb_r > hi:
            lb_r = hi
        for c in range(ncols):
            x = lo + c
            if x < lb_r:
                continue
            cur[c] = winmax[c] + e_row[x] - (BIG if f_row[x] else 0)
            back[r][c] = winidx[c]
        prev = cur
    best_c = max(range(ncols), key=lambda c: prev[c])
    path = [0] * height
    c = best_c
    path[height - 1] = lo + c
    for r in range(height - 1, 0, -1):
        c = back[r][c]
        path[r - 1] = lo + c
    return path


def snap_off_faces(path: List[int], face_boxes: List[Box], lo: int, hi: int,
                   lb: Optional[List[int]]) -> List[int]:
    """Push boundary rows out of any face box they cut through."""
    for (bx0, by0, bx1, by1) in face_boxes:
        for r in range(max(0, by0), min(len(path), by1)):
            x = path[r]
            if bx0 < x < bx1:
                left = bx0 - 2
                right = bx1 + 2
                target = left if (x - bx0) <= (bx1 - x) else right
                target = max(lo, min(hi, target))
                if lb is not None:
                    target = max(target, lb[r])
                if target <= hi:
                    path[r] = target
    return path


def contour_masks(direction: str, width: int, height: int,
                  edges: Image.Image, face: Image.Image,
                  face_boxes: List[Box], band: float, min_zone: float) -> List[Image.Image]:
    """Compute 3 irregular boundaries via edge-following path search."""
    orig_w, orig_h = width, height
    if direction == "horizontal":
        edges = edges.rotate(90, expand=True)
        face = face.rotate(90, expand=True)
        face_boxes = rotated_face_boxes(face_boxes, width, height)
        width, height = height, width
    stride = width
    edge_data = edges.tobytes()
    face_data = face.tobytes()
    band_px = max(1, int(band * width))
    min_sep = max(1, int(min_zone * width))
    paths: List[List[int]] = []
    prev_path = None
    for k in (1, 2, 3):
        nominal = k * width // 4
        lo = max(0, nominal - band_px)
        hi = min(width - 1, nominal + band_px)
        if k == 1:
            lo = max(lo, min_sep)
        if k == 3:
            hi = min(hi, width - 1 - min_sep)
        if hi < lo:
            hi = lo
        lb = None
        if prev_path is not None:
            lb = [p + min_sep for p in prev_path]
        path = optimize_boundary(edge_data, face_data, stride, lo, hi, STEP, lb)
        path = snap_off_faces(path, face_boxes, lo, hi, lb)
        paths.append(path)
        prev_path = path
    return masks_from_paths(direction, orig_w, orig_h, paths)


def masks_from_paths(direction: str, width: int, height: int,
                     paths: List[List[int]]) -> List[Image.Image]:
    masks = [Image.new("L", (width, height), 0) for _ in range(4)]
    if direction == "vertical":
        for r in range(height):
            xs = [0] + [paths[k][r] for k in range(3)] + [width]
            for k in range(4):
                if xs[k + 1] > xs[k]:
                    ImageDraw.Draw(masks[k]).line((xs[k], r, xs[k + 1] - 1, r), fill=255)
    else:
        for c in range(width):
            ys = [0] + [paths[k][c] for k in range(3)] + [height]
            for k in range(4):
                if ys[k + 1] > ys[k]:
                    ImageDraw.Draw(masks[k]).line((c, ys[k], c, ys[k + 1] - 1), fill=255)
    return masks


def normalize_masks(masks: List[Image.Image], width: int, height: int) -> List[Image.Image]:
    """Make supplied masks disjoint and gap-free: lower index wins overlaps,
    gaps are filled from the nearest owned pixel (BFS)."""
    labels = [[-1] * width for _ in range(height)]
    dq: deque = deque()
    for k, m in enumerate(masks):
        px = m.load()
        for y in range(height):
            for x in range(width):
                if px[x, y] > 127 and labels[y][x] == -1:
                    labels[y][x] = k
                    dq.append((x, y))
    while dq:
        x, y = dq.popleft()
        lab = labels[y][x]
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < width and 0 <= ny < height and labels[ny][nx] == -1:
                labels[ny][nx] = lab
                dq.append((nx, ny))
    out = [Image.new("L", (width, height), 0) for _ in range(4)]
    loaders = [o.load() for o in out]
    for y in range(height):
        for x in range(width):
            loaders[labels[y][x]][x, y] = 255
    return out


def check_tiling(masks: List[Image.Image], width: int, height: int) -> None:
    union = masks[0].copy()
    for m in masks[1:]:
        union = ImageChops.lighter(union, m)
    if union.getextrema() != (255, 255):
        raise SystemExit("Zone masks do not cover the full canvas (gaps detected).")
    for i in range(4):
        for j in range(i + 1, 4):
            if ImageChops.multiply(masks[i], masks[j]).getbbox() is not None:
                raise SystemExit(f"Zone masks {i + 1} and {j + 1} overlap.")
    counts = [m.histogram()[255] for m in masks]
    for i, c in enumerate(counts):
        if c == 0:
            raise SystemExit(f"Zone mask {i + 1} is empty.")


# ---------------------------------------------------------------------------
# Anchor and levels
# ---------------------------------------------------------------------------

def mask_region_area(mask: Image.Image, box: Box) -> int:
    x0, y0, x1, y1 = box
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(mask.width, x1), min(mask.height, y1)
    if x1 <= x0 or y1 <= y0:
        return 0
    hist = mask.crop((x0, y0, x1, y1)).histogram()
    return sum(hist[128:])


def pick_anchor(masks: List[Image.Image], face_boxes: List[Box]) -> int:
    """0-based anchor index. Fallback is Logical Zone 2 (second from left/top)."""
    if not face_boxes:
        return 1
    best, best_area = 0, -1
    for i, m in enumerate(masks):
        area = sum(mask_region_area(m, fb) for fb in face_boxes)
        if area > best_area:
            best, best_area = i, area
    return best


def assign_levels(anchor: int, levels: List[int]) -> Dict[int, int]:
    non_anchor = [i for i in range(4) if i != anchor]
    return {zone: level for zone, level in zip(non_anchor, levels)}


def crop_box_for(bbox: Box, width: int, height: int, margin: float) -> Box:
    x0, y0, x1, y1 = bbox
    mx = int(margin * (x1 - x0))
    my = int(margin * (y1 - y0))
    return (max(0, x0 - mx), max(0, y0 - my), min(width, x1 + mx), min(height, y1 + my))


# ---------------------------------------------------------------------------
# Modes
# ---------------------------------------------------------------------------

def cmd_prepare(args: argparse.Namespace) -> None:
    source = Path(args.source)
    if not source.is_file():
        raise SystemExit(f"Source not found: {source}")
    with Image.open(source) as im:
        width, height = im.size

    if args.boundary == "rect":
        masks = rect_masks(args.direction, width, height)
    elif args.boundary == "contour":
        edges, face = edge_and_face_images(source, width, height, args.face_boxes)
        masks = contour_masks(args.direction, width, height, edges, face,
                              args.face_boxes, args.band, args.min_zone)
    else:  # mask
        masks = load_masks_dir(args.masks_dir, width, height)
    check_tiling(masks, width, height)

    if args.anchor == "auto":
        anchor = pick_anchor(masks, args.face_boxes)
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
        for i, mask in enumerate(masks):
            bbox = mask.getbbox()
            if bbox is None:
                raise SystemExit(f"Zone mask {i + 1} is empty.")
            box = tuple(bbox)
            crop_box = crop_box_for(box, width, height, args.margin)
            crop = img.crop(crop_box)
            crop_path = crops_dir / f"zone{i}.png"
            crop.save(crop_path)
            mask_path = masks_dir / f"zone{i}.png"
            mask.save(mask_path)
            manifest_zones.append(
                {
                    "index": i,
                    "box": list(box),
                    "crop_box": list(crop_box),
                    "crop": str(crop_path),
                    "mask": str(mask_path),
                    "level": "anchor" if i == anchor else level_map[i],
                    "rendered": str(rendered_dir / f"zone{i}.png"),
                }
            )

    manifest = {
        "source": str(source),
        "direction": args.direction,
        "boundary": args.boundary,
        "size": [width, height],
        "anchor": anchor + 1,
        "margin": args.margin,
        "zones": manifest_zones,
    }
    manifest_path = workdir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))

    print(f"Prepared deterministic four-zone layout -> {manifest_path}")
    print(f"Direction={args.direction}  boundary={args.boundary}  "
          f"size={width}x{height}  anchor=Logical Zone {anchor + 1}")
    for z in manifest_zones:
        kind = "anchor" if z["level"] == "anchor" else f"{z['level']}% abstraction"
        print(
            f"  zone {z['index'] + 1}: {kind} | bbox={tuple(z['box'])} | "
            f"crop={z['crop']} | mask={z['mask']} | rendered={z['rendered']}"
        )
    print("Render each abstract zone crop with the per-zone prompt block, then run --mode compose.")


def load_masks_dir(masks_dir: Path, width: int, height: int) -> List[Image.Image]:
    if masks_dir is None:
        raise SystemExit("--masks-dir is required for --boundary mask.")
    masks_dir = Path(masks_dir)
    masks = []
    for i in range(4):
        p = masks_dir / f"zone{i}.png"
        if not p.is_file():
            raise SystemExit(f"Missing zone mask: {p}")
        with Image.open(p) as m:
            im = m.convert("L")
        if im.size != (width, height):
            raise SystemExit(f"Mask {p} size {im.size} does not match source {(width, height)}.")
        masks.append(im)
    return normalize_masks(masks, width, height)


def differs_masked(ref: Image.Image, out: Image.Image, mask_region: Image.Image) -> bool:
    """True when ref and out differ at any pixel where mask_region is non-zero."""
    diff = ImageChops.difference(ref.convert("RGB"), out.convert("RGB"))
    masked = ImageChops.multiply(diff, mask_region.convert("RGB"))
    return masked.getbbox() is not None


def enforce_anchor(canvas: Image.Image, source: Path, manifest: dict) -> Image.Image:
    anchor = manifest["anchor"] - 1
    zone = manifest["zones"][anchor]
    box = tuple(zone["box"])
    mask = Image.open(zone["mask"]).convert("L")
    with Image.open(source) as im:
        src = im.convert("RGBA")
    if src.size != canvas.size:
        raise SystemExit("Source/canvas size mismatch in anchor enforcement.")
    canvas = Image.composite(src, canvas, mask)
    if differs_masked(src.crop(box), canvas.crop(box), mask.crop(box)):
        raise SystemExit("Anchor pixel verification failed; output was not written.")
    return canvas


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
        box = tuple(z["box"])
        cw, ch = crop_box[2] - crop_box[0], crop_box[3] - crop_box[1]
        if rendered.size != (cw, ch):
            rendered = rendered.resize((cw, ch), Image.LANCZOS)
        rel = (
            box[0] - crop_box[0],
            box[1] - crop_box[1],
            box[2] - crop_box[0],
            box[3] - crop_box[1],
        )
        region = rendered.crop(rel)
        mask_region = Image.open(z["mask"]).convert("L").crop(box)
        if args.feather > 0:
            mask_region = mask_region.filter(ImageFilter.GaussianBlur(args.feather))
        canvas.paste(region, (box[0], box[1]), mask_region)
        print(f"Pasted zone {z['index'] + 1} at {box[:2]} level={z['level']}")

    canvas = enforce_anchor(canvas, source, manifest)
    save_output(canvas, Path(args.output))
    print(f"Composed one continuous poster -> {args.output}")


def cmd_enforce_anchor(args: argparse.Namespace) -> None:
    manifest = load_manifest(args.workdir)
    with Image.open(args.candidate) as im:
        canvas = im.convert("RGBA")
    if canvas.size != tuple(manifest["size"]):
        raise SystemExit(f"Candidate size {canvas.size} does not match {tuple(manifest['size'])}.")
    canvas = enforce_anchor(canvas, Path(manifest["source"]), manifest)
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
    masks = [Image.open(z["mask"]).convert("L") for z in zones]
    check_tiling(masks, width, height)

    anchor = manifest["anchor"] - 1
    box = tuple(zones[anchor]["box"])
    if differs_masked(src.crop(box), out.crop(box), masks[anchor].crop(box)):
        raise SystemExit("Anchor region differs from source; layout guarantee broken.")

    counts = [m.histogram()[255] for m in masks]
    ratio = max(counts) / max(1, min(counts))
    if ratio > BALANCE_RATIO:
        print(f"  warning: zone areas are unbalanced (max/min = {ratio:.1f}); "
              "keep the four regions roughly balanced.")

    for z in zones:
        if z["level"] == "anchor":
            continue
        b = tuple(z["box"])
        if not differs_masked(src.crop(b), out.crop(b), masks[z["index"]].crop(b)):
            print(f"  warning: zone {z['index'] + 1} is pixel-identical to its source slice; "
                  "no abstraction appears to have been applied.")

    print(
        f"Verified: one continuous {width}x{height} image, 4 exactly-tiled regions "
        f"(boundary={manifest['boundary']}), anchor (zone {anchor + 1}) == source, "
        "scene appears once."
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
        "--boundary",
        choices=("rect", "contour", "mask"),
        default="contour",
        help="Boundary style: contour-aware irregular edges (default), rect strips, or supplied masks",
    )
    parser.add_argument(
        "--anchor",
        default="auto",
        help="auto | 1..4 (1-based Logical Zone); auto = largest face overlap inside zone masks, else Logical Zone 2",
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
        help="Context margin around each zone crop, as a fraction of the zone's bounding box",
    )
    parser.add_argument(
        "--band",
        type=float,
        default=0.18,
        help="contour mode: max boundary deviation from the nominal equal edge, as a fraction of the slice axis",
    )
    parser.add_argument(
        "--min-zone",
        type=float,
        default=0.15,
        help="contour mode: minimum zone width/height, as a fraction of the slice axis",
    )
    parser.add_argument(
        "--masks-dir",
        type=Path,
        help="Directory with zone0.png..zone3.png grayscale masks (required for --boundary mask)",
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
    if args.band <= 0 or args.min_zone <= 0:
        raise SystemExit("--band and --min-zone must be positive.")
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
