#!/usr/bin/env python3
"""Deterministic four-zone slicing and compositing for the Four-Slice Reality Poster.

The image model never decides the slicing. This script:

- defines four regions that tile the source exactly (no gaps, no overlaps):
  * --boundary natural  -> ONE photo in four natural regions, each region
                           differing only by abstraction, with the boundary
                           expressed by a paper-material seam (default)
  * --boundary collage  -> optional layered torn-paper sheets with a full
                           paper finish
  * --boundary torn     -> legacy ordered torn-strip composition
  * --boundary contour  -> optional semantic + edge-aware contour boundaries
  * --boundary mask     -> four content-aware masks supplied by the agent,
                           normalized to exact tiling automatically
  * --boundary rect     -> four equal vertical/horizontal strips (fallback)
- writes one per-zone context crop for separate rendering (Scheme A) and the
  zone masks used for masked compositing and for full-canvas inpaint
  (Scheme B);
- composes the final poster by pasting rendered zones back at fixed
  coordinates, always keeping the Reality Anchor pasted from the source
  (--mode compose / --mode enforce-anchor); the paper material layer is drawn
  at the region boundaries for --boundary natural (paper seam) and through
  the full paper finish for --boundary collage;
- verifies that the output is one continuous source-ratio image whose scene
  appears exactly once, with the anchor region unchanged (--mode verify).

Any layout where the whole photograph is repeated (2x2 grid, strip, contact
sheet) is geometrically impossible in the output of this script.
"""

from __future__ import annotations

import argparse
import array
import json
import math
import random
import sys
import zlib
from collections import deque
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from PIL import Image, ImageChops, ImageDraw, ImageFilter

Box = Tuple[int, int, int, int]
LEVELS = (30, 65, 90)
# Non-sequential default permutations (everything except the identity
# 30,65,90): the script's default level assignment is staggered, never
# spatially sequential.
NON_SEQUENTIAL_PERMUTATIONS = [
    (30, 90, 65),
    (65, 30, 90),
    (65, 90, 30),
    (90, 30, 65),
    (90, 65, 30),
]
BIG = 10 ** 6        # face penalty weight
STEP = 6             # max column change per row in boundary path search
BALANCE_RATIO = 2.5  # warn when max/min zone area ratio exceeds this

# Torn-strip (legacy) parameters. Each seam is conceptually
#   nominal position + broad low-frequency drift + medium tear + micro fiber.
DEFAULT_SEED = 42          # deterministic generator seed (torn/natural/collage)
TORN_BAND_DEFAULT = 0.06   # typical torn deviation (~6% of the slice axis)
TORN_EXCURSION_MULT = 1.5  # local excursion cap = torn_band * this (9% at default)
TORN_MIN_SEP_FRAC = 0.04   # minimum seam separation (fraction of the slice axis)
TORN_MICRO = 1             # +/-1 px high-frequency fiber jitter

# Semantic + edge-aware weights. Boundary score per pixel =
#   w_edge * FIND_EDGES
#   + sum( w_class * class_boundary )          (person/architecture/road/sky outlines)
#   - inside_penalty(important classes)        (person, architecture)
#   - edge_suppress * FIND_EDGES               (road/sky interiors: quiet noise edges)
#   - BIG if inside a face box
DEFAULT_CLASS_WEIGHTS = {"person": 200, "architecture": 120, "road": 80, "sky": 60}
PERSON_PENALTY = 20_000
ARCH_PENALTY = 10_000
EDGE_SUPPRESS = 0.6


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


def _luminance_diffs(img: Image.Image) -> Tuple[float, float]:
    """Row-to-row and column-to-column mean luminance change on a thumbnail."""
    t = 96
    gray = img.convert("L").resize((t, t))
    data = list(gray.getdata())
    row_diff = 0.0
    for y in range(1, t):
        base = y * t
        prev = (y - 1) * t
        for x in range(t):
            row_diff += abs(data[base + x] - data[prev + x])
    row_diff /= max(1, t * (t - 1))
    col_diff = 0.0
    for y in range(t):
        base = y * t
        for x in range(1, t):
            col_diff += abs(data[base + x] - data[base + x - 1])
    col_diff /= max(1, t * (t - 1))
    return row_diff, col_diff


def suggest_direction(img: Image.Image, width: int, height: int) -> str:
    """Deterministic slicing-direction hint for `--direction auto`.

    Measures row-to-row vs column-to-column luminance change on a small
    thumbnail: strong horizontal banding (sky/ground layering) suggests
    horizontal slices; strong vertical structure (wide flow, columns) suggests
    vertical slices. When neither dominates, the aspect ratio breaks the tie
    (portrait/tall -> horizontal, wide -> vertical). The agent may still
    override with an explicit direction based on semantic flow.
    """
    row_diff, col_diff = _luminance_diffs(img)
    if row_diff > col_diff * 1.15:
        return "horizontal"
    if col_diff > row_diff * 1.15:
        return "vertical"
    return "horizontal" if height > width else "vertical"


def suggest_layout(img: Image.Image, width: int, height: int) -> str:
    """`--layout auto`: horizontal-layered is the collage default priority;
    portrait scenes with strong vertical structure (alleys, narrow streets,
    tall-building corridors) resolve to side-weighted."""
    if width >= height:
        return "horizontal-layered"
    row_diff, col_diff = _luminance_diffs(img)
    if col_diff > row_diff * 1.25:
        return "side-weighted"
    return "horizontal-layered"


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


def edge_and_face_images(img: Image.Image, width: int, height: int,
                         protect_boxes: List[Box]) -> Tuple[Image.Image, Image.Image]:
    gray = img.convert("L")
    edges = gray.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.GaussianBlur(5))
    face = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(face)
    for (x0, y0, x1, y1) in protect_boxes:
        pad = 10
        draw.rectangle(
            (max(0, x0 - pad), max(0, y0 - pad), min(width - 1, x1 + pad), min(height - 1, y1 + pad)),
            fill=255,
        )
    return edges, face


def rotated_face_boxes(face_boxes: List[Box], width: int, height: int) -> List[Box]:
    """Rotate 90 degrees counterclockwise: (x, y) -> (y, width - 1 - x)."""
    return [(y0, width - 1 - x1, y1, width - 1 - x0) for (x0, y0, x1, y1) in face_boxes]


# ---------------------------------------------------------------------------
# Semantic classes (importance-aware contour weights)
# ---------------------------------------------------------------------------

def detect_region_from_edge(img: Image.Image, width: int, height: int, edge: str,
                            seed_vmin: int, seed_vmax: int, seed_smax: int,
                            grow_vmin: int, grow_vmax: int, grow_smax: int,
                            hue_min: int = 0, hue_max: int = 255,
                            min_area_frac: float = 0.0) -> Optional[Image.Image]:
    """Flood-fill a region growing from the top or bottom edge.

    Built-in approximation for sky (bright, blue-ish, from the top) and
    ground/road (mid-tone desaturated, from the bottom). The optional hue
    window constrains the class (e.g. blue sky), and `min_area_frac` discards
    tiny misdetections. Returns None when nothing meaningful is found, so the
    caller can fall back to edge-only behavior.
    """
    with img.convert("HSV") as hsv:
        h_bytes = hsv.getchannel("H").tobytes()
        s_bytes = hsv.getchannel("S").tobytes()
        v_bytes = hsv.getchannel("V").tobytes()
    owned = bytearray(width * height)
    dq: deque = deque()

    def seed_ok(i: int) -> bool:
        return (seed_vmin <= v_bytes[i] <= seed_vmax and s_bytes[i] <= seed_smax
                and (hue_min <= h_bytes[i] <= hue_max or hue_min == 0 and hue_max == 255))

    def grow_ok(i: int) -> bool:
        return (grow_vmin <= v_bytes[i] <= grow_vmax and s_bytes[i] <= grow_smax
                and (hue_min <= h_bytes[i] <= hue_max or hue_min == 0 and hue_max == 255))

    if edge == "top":
        for x in range(width):
            i = x
            if seed_ok(i):
                owned[i] = 255
                dq.append(i)
    else:
        for x in range(width):
            i = (height - 1) * width + x
            if seed_ok(i):
                owned[i] = 255
                dq.append(i)
    while dq:
        i = dq.popleft()
        y, x = divmod(i, width)
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < width and 0 <= ny < height:
                j = ny * width + nx
                if owned[j] == 0 and grow_ok(j):
                    owned[j] = 255
                    dq.append(j)
    mask = Image.frombytes("L", (width, height), bytes(owned))
    count = mask.histogram()[255]
    if count < min_area_frac * width * height:
        return None
    return mask


def person_from_faces(face_boxes: List[Box], width: int, height: int) -> Image.Image:
    """Approximate person silhouettes by extending each face box downward.

    Faces are about 1/7 of a standing person's height and roughly half the
    shoulder width, so the body box extends ~5 face heights down and widens to
    ~2.5 face widths. Only a soft importance hint for the contour energy; the
    visible modules are still defined by the zone masks, and faces keep their
    own BIG penalty.
    """
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    for (x0, y0, x1, y1) in face_boxes:
        fw, fh = x1 - x0, y1 - y0
        body = (
            max(0, int(x0 + fw / 2 - fw * 1.25)),
            y1,
            min(width, int(x0 + fw / 2 + fw * 1.25)),
            min(height, y1 + int(fh * 5)),
        )
        draw.rectangle((body[0], body[1], body[2] - 1, body[3] - 1), fill=255)
    return mask


def head_boxes_from_faces(face_boxes: List[Box], width: int, height: int) -> List[Box]:
    """Expand each face box into a generous head region.

    A bare face box covers only the face; hair, jaw, and neck live outside it,
    so boundaries hugging the box would still cut the head. The head region
    extends ~0.5 face height upward (hair), ~0.7 face height downward (chin +
    neck), and ~0.3 face width on each side.
    """
    boxes: List[Box] = []
    for (x0, y0, x1, y1) in face_boxes:
        fw, fh = x1 - x0, y1 - y0
        boxes.append((
            max(0, int(x0 - 0.3 * fw)),
            max(0, int(y0 - 0.5 * fh)),
            min(width, int(x1 + 0.3 * fw)),
            min(height, int(y1 + 0.7 * fh)),
        ))
    return boxes


def head_mask_from_boxes(head_boxes: List[Box], width: int, height: int) -> Image.Image:
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    for (x0, y0, x1, y1) in head_boxes:
        draw.rectangle((x0, y0, x1 - 1, y1 - 1), fill=255)
    return mask


def pick_primary_face(face_boxes: List[Box],
                      forced_index: Optional[int] = None) -> Optional[Box]:
    """The PRIMARY face = the largest face box by area (deterministic,
    first box wins ties), unless `--primary-face N` forces a specific box.

    Only the primary head is hard source-protected and used for anchor
    selection; secondary faces in multi-person photos are regular content.
    """
    if not face_boxes:
        return None
    if forced_index is not None:
        return face_boxes[forced_index - 1]
    return max(face_boxes, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))


def load_class_mask(path: Path, width: int, height: int, name: str) -> Image.Image:
    if not path.is_file():
        raise SystemExit(f"Missing class mask: {path}")
    with Image.open(path) as im:
        mask = im.convert("L")
    if mask.size != (width, height):
        raise SystemExit(f"Class mask {path} size {mask.size} does not match source {(width, height)}.")
    return mask


def build_semantic_images(img: Image.Image, width: int, height: int,
                          face_boxes: List[Box], auto_semantic: bool,
                          class_masks_dir: Optional[Path]) -> Dict[str, Image.Image]:
    """Built-in heuristics (person/sky/ground) overridden by supplied masks.

    `person` and `architecture` are important classes (inside = penalty);
    `road` and `sky` are low-importance classes (interior edges suppressed).
    """
    sem: Dict[str, Image.Image] = {}
    if class_masks_dir is not None:
        d = Path(class_masks_dir)
        for name in ("person", "architecture", "road", "sky"):
            p = d / f"{name}.png"
            if p.is_file():
                sem[name] = load_class_mask(p, width, height, name)
    if auto_semantic:
        if "person" not in sem and face_boxes:
            sem["person"] = person_from_faces(face_boxes, width, height)
        if "sky" not in sem:
            sky = detect_region_from_edge(
                img, width, height, "top",
                seed_vmin=120, seed_vmax=255, seed_smax=160,
                grow_vmin=100, grow_vmax=255, grow_smax=170,
                hue_min=115, hue_max=190,   # blue range (170-260 deg in 0-255 scale)
                min_area_frac=0.05,
            )
            if sky is not None:
                sem["sky"] = sky
        if "road" not in sem:
            road = detect_region_from_edge(
                img, width, height, "bottom",
                seed_vmin=40, seed_vmax=235, seed_smax=100,
                grow_vmin=30, grow_vmax=240, grow_smax=120,
                min_area_frac=0.08,
            )
            if road is not None:
                sem["road"] = road
    return sem


def build_score(edges: Image.Image, face: Image.Image,
                sem: Dict[str, Image.Image],
                weights: Dict[str, int]) -> array.array:
    """Combine edge energy, class-boundary rewards, and inside penalties into
    one int32 score field consumed by optimize_boundary."""
    width, height = edges.size
    n = width * height
    edge_bytes = edges.tobytes()
    face_bytes = face.tobytes()
    prep: Dict[str, Tuple[bytes, bytes]] = {}
    for name, mask in sem.items():
        dilated = mask.filter(ImageFilter.MaxFilter(3))
        boundary = ImageChops.subtract(dilated, mask).tobytes()
        prep[name] = (mask.tobytes(), boundary)
    scores = array.array("i", [0]) * n
    for i in range(n):
        e = edge_bytes[i]
        v = e
        if face_bytes[i]:
            v -= BIG
        if "person" in prep:
            inside, bnd = prep["person"]
            if inside[i]:
                v -= PERSON_PENALTY
            elif bnd[i]:
                v += weights.get("person", DEFAULT_CLASS_WEIGHTS["person"])
        if "architecture" in prep:
            inside, bnd = prep["architecture"]
            if inside[i]:
                v -= ARCH_PENALTY
            elif bnd[i]:
                v += weights.get("architecture", DEFAULT_CLASS_WEIGHTS["architecture"])
        if "road" in prep:
            inside, bnd = prep["road"]
            if inside[i]:
                v -= int(EDGE_SUPPRESS * e)
            elif bnd[i]:
                v += weights.get("road", DEFAULT_CLASS_WEIGHTS["road"])
        if "sky" in prep:
            inside, bnd = prep["sky"]
            if inside[i]:
                v -= int(EDGE_SUPPRESS * e)
            elif bnd[i]:
                v += weights.get("sky", DEFAULT_CLASS_WEIGHTS["sky"])
        scores[i] = v
    return scores


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


def optimize_boundary(score_data: array.array, stride: int,
                      lo: int, hi: int, step: int,
                      lb: Optional[List[int]]) -> List[int]:
    """Best top-to-bottom path within [lo, hi] maximizing the combined score.

    The score field already contains edge energy, semantic class-boundary
    rewards, inside penalties, and the face penalty; `lb` keeps a per-row
    lower bound so consecutive boundaries cannot cross or collapse.
    Returns one x value per row.
    """
    height = len(score_data) // stride
    ncols = hi - lo + 1
    NEG = float("-inf")
    prev = [NEG] * ncols
    back: List[List[int]] = [[0] * ncols for _ in range(height)]
    first = score_data[:stride]
    for c in range(ncols):
        prev[c] = first[lo + c]
    for r in range(1, height):
        row = score_data[r * stride:(r + 1) * stride]
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
            cur[c] = winmax[c] + row[x]
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


def snap_off_faces(path: List[int], protect_boxes: List[Box], lo: int, hi: int,
                   lb: Optional[List[int]]) -> List[int]:
    """Push boundary rows out of any protected box they cut through."""
    for (bx0, by0, bx1, by1) in protect_boxes:
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
                  protect_boxes: List[Box], band: float, min_zone: float,
                  sem: Dict[str, Image.Image],
                  weights: Dict[str, int]) -> List[Image.Image]:
    """Compute 3 irregular boundaries via semantic + edge-aware path search."""
    orig_w, orig_h = width, height
    if direction == "horizontal":
        edges = edges.rotate(90, expand=True)
        face = face.rotate(90, expand=True)
        protect_boxes = rotated_face_boxes(protect_boxes, width, height)
        sem = {name: m.rotate(90, expand=True) for name, m in sem.items()}
        width, height = height, width
    score_data = build_score(edges, face, sem, weights)
    stride = width
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
        path = optimize_boundary(score_data, stride, lo, hi, STEP, lb)
        path = snap_off_faces(path, protect_boxes, lo, hi, lb)
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


# ---------------------------------------------------------------------------
# Torn-strip boundaries (multi-scale, deterministic, legacy)
# ---------------------------------------------------------------------------

def moving_average(values: List[float], window: int) -> List[float]:
    """Box moving average via prefix sums (shortened at the edges)."""
    n = len(values)
    if n == 0:
        return []
    window = max(1, min(window, n))
    pref = [0.0] * (n + 1)
    for i, v in enumerate(values):
        pref[i + 1] = pref[i] + v
    out = [0.0] * n
    half = window // 2
    for i in range(n):
        lo = max(0, i - half)
        hi = min(n, i + half + 1)
        out[i] = (pref[hi] - pref[lo]) / (hi - lo)
    return out


def filtered_noise(rng: random.Random, length: int, amplitude: float,
                   window: int) -> List[float]:
    """Smooth, bounded, deterministic noise (3 box-filter passes).

    Produces medium-frequency tear variation with local continuity — never the
    per-pixel independent ECG jitter of bare `random.randint` noise.
    """
    if length <= 1:
        return [0.0] * length
    raw = [rng.uniform(-1.0, 1.0) for _ in range(length)]
    cur = raw
    for _ in range(3):
        cur = moving_average(cur, window)
    peak = max((abs(v) for v in cur), default=1.0) or 1.0
    scale = amplitude / peak
    return [v * scale for v in cur]


def avoid_head_boxes(seam: List[int], protect_boxes: List[Box], lo: int, hi: int,
                     direction: str) -> List[int]:
    """Locally push a seam out of protected head boxes (hard avoidance).

    Each crossing row is moved to the nearer side of the head box with a small
    gap and clamped to the seam's deviation band. A later light smoothing pass
    blends the pushed segment back into the original trajectory, so the detour
    stays short and never wraps around the subject. Body, buildings, roads,
    sky and other subjects are NOT avoided — the seam may cut straight through
    them.
    """
    if not protect_boxes:
        return seam
    gap = 2
    for (bx0, by0, bx1, by1) in protect_boxes:
        if direction == "vertical":
            r0, r1 = max(0, by0), min(len(seam), by1)
            for r in range(r0, r1):
                x = seam[r]
                if bx0 < x < bx1:
                    target = (bx0 - gap) if (x - bx0) <= (bx1 - x) else (bx1 + gap)
                    seam[r] = min(hi, max(lo, target))
        else:
            c0, c1 = max(0, bx0), min(len(seam), bx1)
            for c in range(c0, c1):
                y = seam[c]
                if by0 < y < by1:
                    target = (by0 - gap) if (y - by0) <= (by1 - y) else (by1 + gap)
                    seam[c] = min(hi, max(lo, target))
    return seam


def torn_paths(direction: str, width: int, height: int,
               protect_boxes: List[Box], torn_band: float,
               roughness: float, scale: float, seed: int,
               min_sep_frac: float = TORN_MIN_SEP_FRAC) -> List[List[int]]:
    """Generate the 3 ordered torn-paper seams (deterministic).

    Each seam is a continuous edge-to-edge path built from three frequency
    scales:

        seam = nominal + broad low-frequency drift + medium tear + micro fiber

    and then:
    - clamped to a deviation band around its nominal 1/4, 1/2 or 3/4 edge
      (typical deviation ~ `torn_band`, local cap ~ `torn_band * 1.5`);
    - kept ordered and separated from its neighbours (`min_sep_frac`);
    - pushed around protected head boxes with smooth reconnection;
    - lightly smoothed so pushed segments reconnect without large detours.

    It does NOT use FIND_EDGES, semantic class weights, or the contour
    dynamic program, and it deliberately ignores building/silhouette/road/
    horizon contours — the seams may cut straight through ordinary objects.
    Identical source/direction/seed/params produce identical seams.
    Returns 3 paths in original image space (vertical: x per row;
    horizontal: y per column).
    """
    if direction == "vertical":
        npos = max(2, height)
        axis = width
    else:
        npos = max(2, width)
        axis = height
    axis = max(1, axis)
    nominal = [axis * k // 4 for k in (1, 2, 3)]
    exc = max(2, int(axis * torn_band * TORN_EXCURSION_MULT))
    min_sep = max(4, int(axis * min_sep_frac))
    paths: List[List[int]] = []
    prev = None
    for k, nom in enumerate(nominal):
        rng = random.Random(seed + k * 101)
        # 1) broad low-frequency drift (sine sum, correlated over the canvas)
        broad = [0.0] * npos
        amp_broad = axis * torn_band * 0.55
        n_sines = 2 + (k % 2)
        for _ in range(n_sines):
            freq = rng.uniform(0.5, 2.5) * (2.0 * math.pi / max(1, npos)) * (1.0 / max(0.25, scale))
            phase = rng.uniform(0.0, 2.0 * math.pi)
            a = amp_broad * rng.uniform(0.4, 1.0)
            for i in range(npos):
                broad[i] += a * math.sin(freq * i + phase)
        # 2) medium-frequency tear (smoothed noise)
        window = max(3, int(npos * 0.04 / max(0.25, scale)))
        amp_tear = axis * torn_band * 0.5 * max(0.0, roughness)
        tear = filtered_noise(rng, npos, amp_tear, window)
        # 3) high-frequency micro fiber jaggedness (±1 px, continuous)
        micro = [rng.randint(-TORN_MICRO, TORN_MICRO) for _ in range(npos)]
        seam = [nom + broad[i] + tear[i] + micro[i] for i in range(npos)]
        lo = max(0, nom - exc)
        hi = min(axis - 1, nom + exc)
        seam = [min(hi, max(lo, int(round(v)))) for v in seam]
        if prev is not None:
            seam = [max(seam[i], prev[i] + min_sep) for i in range(npos)]
            seam = [min(hi, max(lo, v)) for v in seam]
        seam = avoid_head_boxes(seam, protect_boxes, lo, hi, direction)
        if prev is not None:
            seam = [max(seam[i], prev[i] + min_sep) for i in range(npos)]
            seam = [min(hi, max(lo, v)) for v in seam]
        # smooth reconnection of pushed head segments (and general seam softness)
        smooth_w = max(3, int(npos * 0.02))
        seam = [int(round(v)) for v in moving_average([float(v) for v in seam], smooth_w)]
        seam = [min(hi, max(lo, v)) for v in seam]
        if prev is not None:
            seam = [max(seam[i], prev[i] + min_sep) for i in range(npos)]
            seam = [min(hi, max(lo, v)) for v in seam]
        paths.append(seam)
        prev = seam
    return paths


def seam_paper_geometry(seams: List[List[int]], direction: str, fiber_width: int,
                        seed: int) -> List[dict]:
    """Deterministic per-seam geometry for the torn-paper overlay.

    ALL randomness is consumed here, so the colored overlay and the verify
    exemption mask always describe the exact same pixels. Returns per-seam
    dicts with points, perpendiculars, ribbon widths, jaggedness, fiber
    lengths and core-line jitter.
    """
    rng = random.Random(seed + 777)
    fiber_width = max(1, fiber_width)
    geom: List[dict] = []
    for path in seams:
        if direction == "vertical":
            pts = [(path[r], r) for r in range(len(path))]
        else:
            pts = [(c, path[c]) for c in range(len(path))]
        n = len(pts)
        if n < 2:
            continue
        perps = []
        for i in range(n):
            x0, y0 = pts[max(0, i - 1)]
            x1, y1 = pts[min(n - 1, i + 1)]
            dx, dy = x1 - x0, y1 - y0
            length = math.hypot(dx, dy) or 1.0
            perps.append((-dy / length, dx / length))
        hi_w = max(2, fiber_width)  # guard: randint(2, 1) would raise
        widths = [rng.randint(2, hi_w) for _ in range(n)]
        jitter = [rng.randint(-2, 2) for _ in range(n)]
        fibers = [rng.randint(2, fiber_width + 2) for _ in range(n)]
        core_jit = [rng.randint(-1, 1) for _ in range(n)]
        geom.append({"pts": pts, "perps": perps, "widths": widths,
                     "jitter": jitter, "fibers": fibers, "core_jit": core_jit})
    return geom


def paper_shapes(g: dict, shadow_offset: int, with_shadow: bool) -> List[Tuple[str, object]]:
    """Deterministic shape list for one seam, in paint order.

    (kind, coords): "poly" = filled polygon, "line" = stroked polyline/segment.
    Both the colored overlay and the exemption mask iterate the SAME shapes,
    so the verify exemption always covers exactly what was painted.
    """
    pts = g["pts"]
    perps = g["perps"]
    widths = g["widths"]
    jit = g["jitter"]
    fibers = g["fibers"]
    cj = g["core_jit"]
    n = len(pts)
    shapes: List[Tuple[str, object]] = []
    if with_shadow:
        sh_top = [(pts[i][0] + perps[i][0] * (shadow_offset + widths[i] * 0.9),
                   pts[i][1] + perps[i][1] * (shadow_offset + widths[i] * 0.9)) for i in range(n)]
        sh_bot = [(pts[i][0] - perps[i][0] * (shadow_offset + widths[i] * 0.9),
                   pts[i][1] - perps[i][1] * (shadow_offset + widths[i] * 0.9)) for i in range(n)]
        shapes.append(("poly", sh_top + sh_bot[::-1]))
    # fiber strands: short perpendicular strokes across the cut, variable length
    for i in range(n):
        px, py = pts[i]
        ux, uy = perps[i]
        w = widths[i] + jit[i]
        fl = fibers[i]
        shapes.append(("line", (px - ux * (w + fl), py - uy * (w + fl),
                                px + ux * (w + fl), py + uy * (w + fl))))
    # jagged ivory ribbon: per-point random half-width and perpendicular jitter
    top = [(pts[i][0] + perps[i][0] * (widths[i] + jit[i]) * 0.7,
            pts[i][1] + perps[i][1] * (widths[i] + jit[i]) * 0.7) for i in range(n)]
    bot = [(pts[i][0] - perps[i][0] * (widths[i] + jit[i]) * 0.7,
            pts[i][1] - perps[i][1] * (widths[i] + jit[i]) * 0.7) for i in range(n)]
    shapes.append(("poly", top + bot[::-1]))
    # jagged aged core line: the actual torn cut
    core = [(pts[i][0] + perps[i][0] * cj[i], pts[i][1] + perps[i][1] * cj[i]) for i in range(n)]
    shapes.append(("line", core))
    return shapes


def paper_seam_color(canvas_rgb: Image.Image, pts: List[Tuple[int, int]],
                     bright_ivory: Tuple[int, int, int],
                     aged_ivory: Tuple[int, int, int]) -> Tuple[int, int, int, int]:
    """Adaptive warm ivory for a seam: brighter local background -> aged beige."""
    n = max(1, len(pts))
    lum = 0.0
    step = max(1, n // 24)
    count = 0
    for i in range(0, n, step):
        x, y = pts[i]
        r, g, b = canvas_rgb.getpixel((x, y))
        lum += (r + g + b) / 3.0
        count += 1
    lum = (lum / count) / 255.0 if count else 0.0
    blend = lum * 0.45
    return tuple(int(bright_ivory[c] * (1.0 - blend) + aged_ivory[c] * blend)
                 for c in range(3)) + (255,)


def draw_paper_seams(canvas: Image.Image, seams: List[List[int]], direction: str,
                     fiber_width: int, seed: int,
                     shadow_alpha: int = 26, shadow_offset: int = 3) -> Image.Image:
    """Overlay torn-paper seams (visual only).

    Paints a jagged warm-ivory paper ribbon along each seam with perpendicular
    fiber strands, a dark aged cut line, and a faint offset shadow. The ivory
    adapts to the local background brightness. The four zone masks keep exact
    tiling underneath; the overlay is purely cosmetic. Deterministic via
    `seed` (geometry shared with `paper_seam_mask`).
    """
    geom = seam_paper_geometry(seams, direction, fiber_width, seed)
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    canvas_rgb = canvas.convert("RGB")
    bright_ivory = (243, 237, 219)
    aged_ivory = (198, 184, 152)
    shadow_alpha = max(0, min(255, shadow_alpha))
    shadow_offset = max(0, shadow_offset)
    for g in geom:
        shapes = paper_shapes(g, shadow_offset, with_shadow=shadow_alpha > 0)
        col = paper_seam_color(canvas_rgb, g["pts"], bright_ivory, aged_ivory)
        idx = 0
        if shadow_alpha > 0:
            od.polygon(shapes[0][1], fill=(30, 24, 14, shadow_alpha))
            idx = 1
        for kind, coords in shapes[idx:]:
            if kind == "poly":
                od.polygon(coords, fill=col)
            else:
                od.line(coords, fill=col, width=1)
        # dark aged cut line on top (slightly varied per seam, deterministic)
        core = shapes[-1][1]
        od.line(core, fill=(140, 122, 96, 200), width=1)
    canvas.alpha_composite(overlay)
    return canvas


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
# Collage: layered torn-paper sheets (optional)
#
# TORN EDGE IS REGION GEOMETRY, NOT A DECORATIVE LINE DRAWN ON TOP.
# Pieces are layered paper shapes (not 1/4-based strips) that tile exactly
# underneath; the paper body / deckled fiber edge / one-sided shadow are the
# compositing finish of those pieces.
# ---------------------------------------------------------------------------

def collage_z_order(layout: str) -> List[int]:
    """Piece z-order, low -> high. Shadows fall only from higher onto lower."""
    if layout == "side-weighted":
        return [2, 0, 1, 3]   # right field, left field, Reality corridor, top band
    return [0, 1, 2, 3]       # horizontal-layered: bottom layer -> top layer


def _broad_curve(npos: int, kind: str, amplitude: float) -> List[float]:
    """Deprecated smooth-curve helper kept only for signature compatibility."""
    return [0.0] * npos


def collage_torn_path(npos: int, axis: int, nominal_frac: float, band_frac: float,
                      curve_kind: str, rng: random.Random,
                      roughness: float, scale: float = 1.0) -> List[int]:
    """One torn paper boundary — ANGULAR, not wavy.

    Torn paper tears along runs and jumps; it does not undulate like a wave.
    The edge is therefore dominated by:
    - gentle piecewise-linear wander with MODEST amplitude (~1% of the axis),
      so there is no large low-frequency undulation;
    - sharp localized V-notches (torn jumps, up to ~5% of the axis);
    - a +/-1 px micro jag with a tiny 2px de-alias only (corners stay sharp).

    Boundaries generated from different seeds are independent — never
    parallel copies. Deterministic via `rng`.
    """
    band_px = max(2, int(axis * band_frac))
    nom = nominal_frac * axis
    wander = max(2, int(axis * 0.01))                # modest overall drift
    n_ctrl = max(6, npos // 14)                      # straight runs of ~12-20px
    xs = [round(i * (npos - 1) / max(1, n_ctrl - 1)) for i in range(n_ctrl)]
    ys = [nom + rng.uniform(-1.0, 1.0) * wander for _ in range(n_ctrl)]
    path = [0.0] * npos
    for k in range(n_ctrl - 1):
        x0, x1 = xs[k], xs[k + 1]
        y0, y1 = ys[k], ys[k + 1]
        span = max(1, x1 - x0)
        for i in range(x0, x1 + 1):
            t = (i - x0) / span
            path[i] = y0 + (y1 - y0) * t
    # sharp localized V-notches: the character of a torn jump
    n_notch = max(3, npos // 45)
    notch_amp = max(2, int(axis * 0.05))
    for _ in range(n_notch):
        pos = rng.randrange(0, npos)
        width = rng.randint(4, 14)
        depth = rng.uniform(0.5, 1.1) * notch_amp * max(0.5, roughness)
        sign = 1.0 if rng.random() < 0.5 else -1.0
        for i in range(max(0, pos - width), min(npos, pos + width + 1)):
            t = 1.0 - abs(i - pos) / max(1, width)
            path[i] += sign * depth * (t * t)
    # micro jag + tiny 2px de-alias (keeps corners sharp, kills ECG aliasing)
    path = [path[i] + rng.randint(-1, 1) for i in range(npos)]
    path = moving_average(path, 2)
    lo = max(0, int(nom - band_px))
    hi = min(axis - 1, int(nom + band_px))
    return [min(hi, max(lo, int(round(v)))) for v in path]


def natural_path(npos: int, axis: int, nominal_frac: float, band_frac: float,
                 rng: random.Random, roughness: float) -> List[int]:
    """Smooth organic boundary for the `natural` default family.

    ONE photo divided into four natural regions: boundaries are gentle,
    organic curves — irregular but not torn-jagged and not a regular wave
    (incommensurate low-frequency drift + smooth medium irregularity + a
    +/-1px micro), with modest amplitude (~2-3% of the axis). Deterministic
    via `rng`.
    """
    exc = max(2, int(axis * band_frac))
    nom = nominal_frac * axis
    amp_drift = max(2, int(axis * 0.02))
    drift = [0.0] * npos
    for _ in range(3):
        freq = rng.uniform(0.6, 3.0) * 2.0 * math.pi / max(1, npos) * rng.choice((1.0, 1.7, 2.3))
        phase = rng.uniform(0.0, 2.0 * math.pi)
        a = amp_drift * rng.uniform(0.4, 1.0)
        for i in range(npos):
            drift[i] += a * math.sin(freq * i + phase)
    window = max(4, int(npos * 0.05))
    amp_tear = axis * band_frac * 0.35 * max(0.3, roughness)
    tear = filtered_noise(rng, npos, amp_tear, window)
    micro = [rng.randint(-1, 1) for _ in range(npos)]
    path = [nom + drift[i] + tear[i] + micro[i] for i in range(npos)]
    path = moving_average(path, 5)
    lo = max(0, int(nom - exc))
    hi = min(axis - 1, int(nom + exc))
    return [min(hi, max(lo, int(round(v)))) for v in path]


def horizontal_layered_masks(width: int, height: int, protect_boxes: List[Box],
                             band: float, roughness: float,
                             seed: int, style: str = "torn") -> Tuple[List[Image.Image], List[List[int]]]:
    """Four broad layered paper pieces (portrait default template).

    Layers stack vertically but are NOT quarter-strips: a middle-heavy,
    composition-driven nominal profile (about 20/24/28/28) and each boundary
    gets its OWN independent silhouette (torn deckled or smooth organic
    depending on `style`), so neighbouring edges are not parallel copies.
    """
    npos = width
    axis = height
    rng = random.Random(seed + 500)
    nominals = [0.20, 0.44, 0.72]          # middle-heavy, not 0.25/0.5/0.75
    kinds = ["arc-up", "arc-down", "s"]    # independent global shapes
    min_sep = max(4, int(axis * 0.08))
    paths: List[List[int]] = []
    prev = None
    for nom, kind in zip(nominals, kinds):
        if style == "natural":
            path = natural_path(npos, axis, nom, band, rng, roughness)
        else:
            path = collage_torn_path(npos, axis, nom, band, kind, rng, roughness)
        if prev is not None:
            path = [max(path[i], prev[i] + min_sep) for i in range(npos)]
        path = avoid_head_boxes(path, protect_boxes, 0, axis - 1, "horizontal")
        if prev is not None:
            path = [max(path[i], prev[i] + min_sep) for i in range(npos)]
        smooth_w = max(3, int(npos * 0.02))
        path = [int(round(v)) for v in moving_average([float(v) for v in path], smooth_w)]
        if prev is not None:
            path = [max(path[i], prev[i] + min_sep) for i in range(npos)]
        paths.append(path)
        prev = path
    paths = [[min(axis - 1, max(0, v)) for v in p] for p in paths]
    return masks_from_paths("horizontal", width, height, paths), paths


def side_weighted_masks(width: int, height: int, protect_boxes: List[Box],
                        band: float, roughness: float,
                        seed: int, style: str = "torn") -> Tuple[List[Image.Image], dict]:
    """Alley / central-perspective template.

    piece 4 = a top paper band; below it, piece 2 = a central Reality
    corridor (variable width), piece 1 = broad left field, piece 3 = broad
    right field. NOT four vertical bands: the corridor is central and the
    side fields are wide paper masses.
    """
    rng = random.Random(seed + 700)
    if style == "natural":
        t4 = natural_path(width, height, 0.18, band, rng, roughness)
        c_left = natural_path(height, width, 0.34, band, rng, roughness)
        c_right = natural_path(height, width, 0.66, band, rng, roughness)
    else:
        t4 = collage_torn_path(width, height, 0.18, band, "arc-down", rng, roughness)      # top band bottom edge y(x)
        c_left = collage_torn_path(height, width, 0.34, band, "s", rng, roughness)         # corridor left x(y)
        c_right = collage_torn_path(height, width, 0.66, band, "arc-up", rng, roughness)   # corridor right x(y)
    min_sep = max(6, int(width * 0.12))

    def clamp_corridor():
        nonlocal_none = None
        for y in range(height):
            if c_right[y] < c_left[y] + min_sep:
                c_right[y] = min(width - 1, c_left[y] + min_sep)
            c_right[y] = min(width - 1, max(0, c_right[y]))
            c_left[y] = min(width - 1, max(0, c_left[y]))

    clamp_corridor()
    c_left = avoid_head_boxes(c_left, protect_boxes, 0, width - 1, "vertical")
    c_right = avoid_head_boxes(c_right, protect_boxes, 0, width - 1, "vertical")
    t4 = avoid_head_boxes(t4, protect_boxes, 0, height - 1, "horizontal")
    # smooth reconnection of head pushes
    sw = max(3, int(width * 0.02))
    t4 = [int(round(v)) for v in moving_average([float(v) for v in t4], sw)]
    sw2 = max(3, int(height * 0.02))
    c_left = [int(round(v)) for v in moving_average([float(v) for v in c_left], sw2)]
    c_right = [int(round(v)) for v in moving_average([float(v) for v in c_right], sw2)]
    t4 = [min(height - 1, max(0, v)) for v in t4]
    clamp_corridor()

    masks = [Image.new("L", (width, height), 0) for _ in range(4)]
    for y in range(height):
        cl = min(width - 1, max(0, c_left[y]))
        cr = min(width - 1, max(0, c_right[y]))
        x = 0
        while x < width:
            if t4[x] > y:
                x0 = x
                while x < width and t4[x] > y:
                    x += 1
                ImageDraw.Draw(masks[3]).line((x0, y, x - 1, y), fill=255)
            else:
                x0 = x
                while x < width and t4[x] <= y:
                    x += 1
                a, b = x0, x - 1
                if a <= min(b, cl - 1):
                    ImageDraw.Draw(masks[0]).line((a, y, min(b, cl - 1), y), fill=255)
                if max(a, cl) <= min(b, cr - 1):
                    ImageDraw.Draw(masks[1]).line((max(a, cl), y, min(b, cr - 1), y), fill=255)
                if max(a, cr) <= b:
                    ImageDraw.Draw(masks[2]).line((max(a, cr), y, b, y), fill=255)
    return masks, {"top": t4, "left": c_left, "right": c_right}


def collage_masks(layout: str, width: int, height: int, protect_boxes: List[Box],
                  band: float, roughness: float,
                  seed: int, style: str = "torn") -> Tuple[List[Image.Image], dict]:
    """Generate four region masks for the given layout.

    `style` selects the boundary character: "torn" (deckled paper, for the
    `collage` family) or "natural" (smooth organic, for the `natural`
    family). `vertical-strip` / `horizontal-strip` reuse the legacy torn
    logic. Returns `(masks, geometry)`.
    """
    if layout in ("vertical-strip", "horizontal-strip"):
        direction = "vertical" if layout == "vertical-strip" else "horizontal"
        paths = torn_paths(direction, width, height, protect_boxes,
                           TORN_BAND_DEFAULT, roughness, 1.0, seed)
        return masks_from_paths(direction, width, height, paths), {"paths": paths}
    if layout == "side-weighted":
        return side_weighted_masks(width, height, protect_boxes, band, roughness, seed, style)
    return horizontal_layered_masks(width, height, protect_boxes, band, roughness, seed, style)


def collage_fiber_masks(masks: List[Image.Image], width: int, height: int,
                        edge_width: int, seed: int) -> List[Image.Image]:
    """Deckled exposed-paper fiber band per piece (a broken, uneven ring just
    inside each piece's torn edge). Deterministic via `seed`."""
    edge_width = max(1, edge_width)
    rng = random.Random(seed + 800)
    bands: List[Image.Image] = []
    for mask in masks:
        eroded = mask.filter(ImageFilter.MinFilter(2 * edge_width + 1))
        band = ImageChops.subtract(mask, eroded).point(lambda v: 255 if v else 0)
        bdata = band.tobytes()
        n = len(bdata)
        keep = bytearray(n)
        for i in range(n):
            if bdata[i] and rng.random() < 0.55:   # broken micro sections (sparse)
                keep[i] = 255
        bands.append(Image.frombytes("L", (width, height), bytes(keep)))
    return bands


def collage_shadow_mask(masks: List[Image.Image], z_order: List[int],
                        width: int, height: int, offset: int) -> Image.Image:
    """One-sided paper shadows.

    Each piece (except the z-lowest) casts a faint shadow ring only onto the
    pieces BELOW it in z-order — an upper paper covers lower papers, so the
    shadow never appears on both sides of an edge like a stroke.
    """
    offset = max(1, offset)
    shadow = Image.new("L", (width, height), 0)
    lower_union = Image.new("L", (width, height), 0)
    for idx in z_order:  # low -> high z
        mask = masks[idx]
        dilated = mask.filter(ImageFilter.MaxFilter(2 * offset + 1))
        ring = ImageChops.subtract(dilated, mask)
        ring = ImageChops.multiply(ring, lower_union)
        shadow = ImageChops.lighter(shadow, ring)
        lower_union = ImageChops.lighter(lower_union, mask)
    return shadow


def draw_collage_paper(canvas: Image.Image, masks: List[Image.Image],
                       z_order: List[int], width: int, height: int,
                       edge_width: int, shadow_alpha: int, shadow_offset: int,
                       seed: int) -> Image.Image:
    """Paper body finish for collage: deckled fiber bands + one-sided shadows.

    Visual only — the four piece masks still tile the canvas exactly, and the
    verify exemption mask uses the same deterministic fiber/shadow masks.
    """
    canvas_rgb = canvas.convert("RGB")
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    ov = overlay.load()
    bright_ivory = (243, 237, 219)
    aged_ivory = (198, 184, 152)
    bands = collage_fiber_masks(masks, width, height, edge_width, seed)
    for idx, band in enumerate(bands):
        bp = band.load()
        pts = []
        for y in range(0, height, max(1, height // 40)):
            for x in range(width):
                if bp[x, y]:
                    pts.append((x, y))
        lum = 0.0
        for (x, y) in pts:
            r, g, b = canvas_rgb.getpixel((x, y))
            lum += (r + g + b) / 3.0
        lum = (lum / max(1, len(pts))) / 255.0
        blend = lum * 0.45
        base = tuple(int(bright_ivory[c] * (1.0 - blend) + aged_ivory[c] * blend) for c in range(3))
        rng = random.Random(seed + 811 + idx)
        for y in range(height):
            for x in range(width):
                if bp[x, y]:
                    v = rng.randint(-7, 7)
                    ov[x, y] = (max(0, min(255, base[0] + v)),
                                max(0, min(255, base[1] + v)),
                                max(0, min(255, base[2] + v)), 255)
    if shadow_alpha > 0:
        shadow = collage_shadow_mask(masks, z_order, width, height, shadow_offset)
        sp = shadow.load()
        for y in range(height):
            for x in range(width):
                if sp[x, y] and ov[x, y][3] == 0:
                    ov[x, y] = (30, 24, 14, shadow_alpha)
    canvas.alpha_composite(overlay)
    return canvas


def paper_texture(canvas: Image.Image, seed: int, strength: int = 26) -> Image.Image:
    """Subtle deterministic paper grain (image-first, not a vintage filter)."""
    if strength <= 0:
        return canvas
    w, h = canvas.size
    rng = random.Random(seed + 909)
    data = bytearray(w * h)
    for i in range(w * h):
        data[i] = rng.getrandbits(8)
    grain = Image.frombytes("L", (w, h), bytes(data)).point(lambda v: int(v * 0.4) + 60)
    overlay = Image.merge("RGBA", (grain, grain, grain, Image.new("L", (w, h), strength)))
    canvas.alpha_composite(overlay)
    return canvas


def robot_dreams_grade(canvas: Image.Image) -> Image.Image:
    """Subtle warm, nostalgic, sunlit, slightly retro cinematic grade.

    Lifts blacks (gentle fade), warms the midtones and rolls off highlights —
    the deterministic counterpart of the Robot Dreams-inspired palette that
    the per-zone render prompts request. Applied to the collage pieces; the
    Reality anchor and head are re-composited clean from the source
    afterwards, so they keep the untouched photograph.
    """
    rgb = canvas.convert("RGB")
    r, g, b = rgb.split()
    r = r.point(lambda v: min(255, max(0, int(v * 0.96) + 12)))
    g = g.point(lambda v: min(255, max(0, int(v * 0.98) + 8)))
    b = b.point(lambda v: min(255, max(0, int(v * 1.00) + 2)))
    return Image.merge("RGB", (r, g, b)).convert("RGBA")


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


def auto_levels(source: Path, seed: int) -> List[int]:
    """Deterministic staggered default level permutation.

    Picks one of the non-sequential permutations (30/65/90 never in spatial
    order) from a stable hash of `source` and `seed`, so different photos get
    different staggers while the same source + seed always repeats exactly.
    """
    idx = (zlib.crc32(str(source).encode()) ^ seed) % len(NON_SEQUENTIAL_PERMUTATIONS)
    return list(NON_SEQUENTIAL_PERMUTATIONS[idx])


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
        img = im.convert("RGB")

    # All face boxes (expanded heads) are used ONLY for seam/contour avoidance
    # (a seam should not cut any face); the hard source-lock and the anchor
    # selection use ONLY the PRIMARY head.
    all_head_boxes = head_boxes_from_faces(args.face_boxes, width, height)
    primary_face = pick_primary_face(args.face_boxes, args.primary_face)
    if primary_face is not None:
        who = f"forced box {args.primary_face}" if args.primary_face is not None else "auto (largest)"
        print(f"Primary face ({who}): {tuple(primary_face)}")
    primary_head_boxes = head_boxes_from_faces([primary_face], width, height) if primary_face else []
    head_mask = None
    if args.head_mask is not None:
        head_mask = load_class_mask(args.head_mask, width, height, "head")
    elif primary_head_boxes:
        head_mask = head_mask_from_boxes(primary_head_boxes, width, height)

    # seam-avoidance boxes: ALL faces (visual quality), else the head mask bbox
    avoid_boxes = all_head_boxes
    if not avoid_boxes and head_mask is not None:
        hb = head_mask.getbbox()
        if hb is not None:
            avoid_boxes = [tuple(hb)]

    # Layout / direction resolution. Layout-based families (natural, collage)
    # define their own structure; --direction only drives legacy torn, contour
    # and the strip layouts.
    layout = args.layout
    if args.boundary in ("natural", "collage"):
        if layout == "auto":
            layout = suggest_layout(img, width, height)
            print(f"Auto layout -> {layout}")
        if layout in ("vertical-strip", "horizontal-strip"):
            direction = "vertical" if layout == "vertical-strip" else "horizontal"
        elif layout == "side-weighted":
            direction = "vertical"
        else:
            direction = "horizontal"
    else:
        if args.direction == "auto":
            direction = suggest_direction(img, width, height)
            print(f"Auto direction -> {direction}")
        else:
            direction = args.direction

    seams = None
    collage_geom = None
    boundaries = None
    if args.boundary in ("natural", "collage"):
        style = "torn" if args.boundary == "collage" else "natural"
        masks, collage_geom = collage_masks(layout, width, height, avoid_boxes,
                                            args.collage_band, args.collage_roughness,
                                            args.seed, style)
        # boundary paths for the paper-material seam at the region edges
        if isinstance(collage_geom, dict):
            if "top" in collage_geom:
                boundaries = [
                    {"path": collage_geom["top"], "dir": "horizontal"},
                    {"path": collage_geom["left"], "dir": "vertical"},
                    {"path": collage_geom["right"], "dir": "vertical"},
                ]
            elif "paths" in collage_geom:
                d = "vertical" if layout == "vertical-strip" else "horizontal"
                boundaries = [{"path": p, "dir": d} for p in collage_geom["paths"]]
        elif isinstance(collage_geom, list):
            boundaries = [{"path": p, "dir": "horizontal"} for p in collage_geom]
    elif args.boundary == "rect":
        masks = rect_masks(direction, width, height)
    elif args.boundary == "torn":
        seams = torn_paths(direction, width, height, avoid_boxes,
                           args.torn_band, args.torn_roughness, args.torn_scale,
                           args.seed)
        masks = masks_from_paths(direction, width, height, seams)
    elif args.boundary == "contour":
        edges, face = edge_and_face_images(img, width, height, all_head_boxes)
        sem = build_semantic_images(img, width, height, args.face_boxes,
                                    args.auto_semantic, args.class_masks_dir)
        masks = contour_masks(direction, width, height, edges, face,
                              all_head_boxes, args.band, args.min_zone,
                              sem, args.class_weights)
    else:  # mask
        masks = load_masks_dir(args.masks_dir, width, height)
    check_tiling(masks, width, height)

    if args.anchor == "auto":
        anchor = pick_anchor(masks, primary_head_boxes)
        # no primary face: side-weighted layout prefers the central Reality
        # corridor; otherwise fall back to Logical Zone 2 (a middle layer)
        if not primary_head_boxes and args.boundary in ("natural", "collage") and layout == "side-weighted":
            anchor = 1  # central corridor region
    else:
        anchor = int(args.anchor) - 1  # CLI is 1-based like restore_protected_anchor.py

    if args.levels is None:
        levels = auto_levels(source, args.seed)
        print(f"Auto staggered levels -> {','.join(str(v) for v in levels)}")
    else:
        levels = args.levels
    if sorted(levels) != sorted(LEVELS):
        raise SystemExit(f"--levels must be a permutation of {list(LEVELS)}; got {levels}")
    level_map = assign_levels(anchor, levels)

    workdir = Path(args.workdir)
    crops_dir = workdir / "crops"
    masks_dir = workdir / "masks"
    rendered_dir = workdir / "rendered"
    for d in (crops_dir, masks_dir, rendered_dir):
        d.mkdir(parents=True, exist_ok=True)

    head_mask_path = None
    if head_mask is not None:
        head_mask_path = masks_dir / "head.png"
        head_mask.save(head_mask_path)

    manifest_zones = []
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

    # Per-mode feather strategy: collage and torn are hard paper cuts (1px
    # anti-alias), the other modes keep the broad soft transition.
    if args.feather is not None:
        feather = args.feather
    elif args.boundary in ("collage", "torn"):
        feather = 1
    else:
        feather = max(4, int(0.02 * min(width, height)))
        feather = min(feather, max(2, min(width, height) // 8))

    manifest = {
        "source": str(source),
        "direction": direction,
        "boundary": args.boundary,
        "layout": layout if args.boundary in ("natural", "collage") else "horizontal-layered",
        "z_order": collage_z_order(layout) if args.boundary == "collage" else None,
        "size": [width, height],
        "anchor": anchor + 1,
        "margin": args.margin,
        "feather": feather,
        "seams": seams if seams else None,
        "seam_style": args.seam_style if args.boundary in ("torn", "natural") else "none",
        "collage_boundaries": boundaries if args.boundary == "natural" else None,
        "fiber_width": args.fiber_width,
        "seam_shadow": args.seam_shadow,
        "seam_offset": args.seam_offset,
        "torn_band": args.torn_band,
        "torn_roughness": args.torn_roughness,
        "torn_scale": args.torn_scale,
        "collage_band": args.collage_band,
        "collage_roughness": args.collage_roughness,
        "collage_overlap": args.collage_overlap,
        "paper_edge_width": args.paper_edge_width,
        "paper_shadow": args.paper_shadow if args.boundary == "collage" else 0,
        "paper_texture": args.paper_texture if args.boundary == "collage" else "none",
        "paper_grade": args.paper_grade if args.boundary in ("natural", "collage") else "none",
        "seed": args.seed,
        "head_mask": str(head_mask_path) if head_mask_path else None,
        "primary_face": list(primary_face) if primary_face else None,
        "face_boxes": [list(b) for b in args.face_boxes],
        "zones": manifest_zones,
    }
    manifest_path = workdir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))

    print(f"Prepared deterministic four-zone layout -> {manifest_path}")
    print(f"Direction={direction}  boundary={args.boundary}  "
          f"size={width}x{height}  anchor=Logical Zone {anchor + 1}")
    if args.boundary == "natural":
        print(f"Natural: layout={layout} band={args.collage_band} "
              f"roughness={args.collage_roughness} grade={args.paper_grade} seed={args.seed}")
    if args.boundary == "collage":
        print(f"Collage: layout={layout} band={args.collage_band} "
              f"roughness={args.collage_roughness} overlap={args.collage_overlap} "
              f"paper_edge={args.paper_edge_width} paper_shadow={args.paper_shadow} "
              f"texture={args.paper_texture} seed={args.seed}")
    if args.boundary == "torn":
        print(f"Torn: band={args.torn_band} roughness={args.torn_roughness} "
              f"scale={args.torn_scale} seed={args.seed} seam_style={args.seam_style}")
    if head_mask is not None:
        print(f"Head protection (PRIMARY head only): {head_mask_path} "
              f"({', '.join(str(tuple(b)) for b in primary_head_boxes) or 'supplied mask'})")
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


def soft_mask(mask: Image.Image, feather: int) -> Image.Image:
    """Blur a binary mask so compositing produces a soft transition band."""
    if feather <= 0:
        return mask
    return mask.filter(ImageFilter.GaussianBlur(feather))


def opaque_core(mask: Image.Image, feather: int) -> Image.Image:
    """Pixels where the softened mask is fully opaque (value == 255).

    Image.composite is exact wherever the mask is 255, so the anchor/head
    source-equality guarantee holds exactly on this core; the soft transition
    band around it is intentionally blended and exempt from the check.
    """
    if feather <= 0:
        return mask
    blurred = mask.filter(ImageFilter.GaussianBlur(feather))
    return blurred.point(lambda v: 255 if v >= 255 else 0)


def enforce_anchor(canvas: Image.Image, source: Path, manifest: dict) -> Image.Image:
    feather = manifest.get("feather", 0)
    grade_on = (manifest.get("boundary") in ("natural", "collage")
                and manifest.get("paper_grade", "subtle") != "none")
    anchor = manifest["anchor"] - 1
    zone = manifest["zones"][anchor]
    box = tuple(zone["box"])
    mask = Image.open(zone["mask"]).convert("L")
    with Image.open(source) as im:
        src = im.convert("RGBA")
    if grade_on:
        # Reality receives the SAME warm grade as the pieces (color only — no
        # grain, no structure change), so the whole poster shares one palette.
        src = robot_dreams_grade(src)
    if src.size != canvas.size:
        raise SystemExit("Source/canvas size mismatch in anchor enforcement.")
    canvas = Image.composite(src, canvas, soft_mask(mask, feather))
    core = opaque_core(mask, feather)
    if differs_masked(src.crop(box), canvas.crop(box), core.crop(box)):
        raise SystemExit("Anchor pixel verification failed; output was not written.")
    head_path = manifest.get("head_mask")
    if head_path:
        head = Image.open(head_path).convert("L")
        hb = head.getbbox()
        if hb is not None:
            head_feather = min(feather, 8)
            canvas = Image.composite(src, canvas, soft_mask(head, head_feather))
            core_head = opaque_core(head, head_feather)
            if differs_masked(src.crop(hb), canvas.crop(hb), core_head.crop(hb)):
                raise SystemExit("Head pixel verification failed; output was not written.")
    return canvas


def cmd_compose(args: argparse.Namespace) -> None:
    manifest = load_manifest(args.workdir)
    source = Path(manifest["source"])
    with Image.open(source) as im:
        canvas = im.convert("RGBA")
    if canvas.size != tuple(manifest["size"]):
        raise SystemExit("Source changed since prepare; re-run --mode prepare.")
    width, height = canvas.size

    rendered_dir = Path(args.rendered_dir)
    src_rgb = canvas.convert("RGB")
    render_warnings: List[str] = []
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
        crop_path = Path(z["crop"])
        if crop_path.is_file():
            with Image.open(crop_path) as ci:
                crop = ci.convert("RGB")
            reason, warns = rendered_zone_sanity(rendered, crop, src_rgb, z["index"])
            if reason:
                raise SystemExit(reason)
            render_warnings.extend(warns)
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
        mask_region = soft_mask(mask_region, manifest.get("feather", 0))
        canvas.paste(region, (box[0], box[1]), mask_region)
        print(f"Pasted zone {z['index'] + 1} at {box[:2]} level={z['level']}")

    for wmsg in render_warnings:
        print(f"  warning: {wmsg}")

    if manifest.get("boundary") == "natural":
        # ONE photo, four natural regions: uniform warm grade over everything
        # (Reality/head re-composited from the graded source), then the paper
        # material layer is drawn ONLY at the region boundaries as torn-paper
        # seams — no z-order, no per-piece sheet bodies, no sheet grain.
        if manifest.get("paper_grade", "subtle") != "none":
            canvas = robot_dreams_grade(canvas)
        canvas = enforce_anchor(canvas, source, manifest)
        if (manifest.get("seam_style", "paper") == "paper"
                and manifest.get("collage_boundaries")):
            for direction in ("vertical", "horizontal"):
                paths = [b["path"] for b in manifest["collage_boundaries"] if b["dir"] == direction]
                if paths:
                    canvas = draw_paper_seams(canvas, paths, direction,
                                              manifest.get("fiber_width", 7),
                                              manifest.get("seed", DEFAULT_SEED),
                                              manifest.get("seam_shadow", 26),
                                              manifest.get("seam_offset", 3))
    elif manifest.get("boundary") == "collage":
        # subtle Robot Dreams-inspired warm grade over the abstract pieces,
        # then shared paper grain; the anchor and head are re-composited
        # clean from the source afterwards, so Reality reads photographic.
        if manifest.get("paper_grade", "subtle") != "none":
            canvas = robot_dreams_grade(canvas)
        if manifest.get("paper_texture", "subtle") != "none":
            canvas = paper_texture(canvas, manifest.get("seed", DEFAULT_SEED))
        canvas = enforce_anchor(canvas, source, manifest)
        masks = [Image.open(z["mask"]).convert("L") for z in manifest["zones"]]
        z_order = manifest.get("z_order") or collage_z_order(manifest.get("layout", "horizontal-layered"))
        canvas = draw_collage_paper(canvas, masks, z_order, width, height,
                                    manifest.get("paper_edge_width", 6),
                                    manifest.get("paper_shadow", 20),
                                    manifest.get("collage_overlap", 5),
                                    manifest.get("seed", DEFAULT_SEED))
    else:
        canvas = enforce_anchor(canvas, source, manifest)
        if (manifest.get("boundary") == "torn"
                and manifest.get("seam_style") == "paper"
                and manifest.get("seams")):
            canvas = draw_paper_seams(canvas, manifest["seams"], manifest["direction"],
                                      manifest.get("fiber_width", 7),
                                      manifest.get("seed", DEFAULT_SEED),
                                      manifest.get("seam_shadow", 26),
                                      manifest.get("seam_offset", 3))
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


def paper_seam_mask(manifest: dict, width: int, height: int) -> Optional[Image.Image]:
    """Binary mask of every pixel the torn paper-seam overlay paints.

    Uses the SAME `seam_paper_geometry` + `paper_shapes` as `draw_paper_seams`
    (same seed, same shadow switch), so verify can exempt the intentional
    paper fiber from the exact source-equality core — the fiber is a visual
    overlay, like the soft transition band, and must not break the
    anchor/head guarantee.
    """
    seams = manifest.get("seams") or []
    direction = manifest.get("direction", "vertical")
    fiber_width = max(1, manifest.get("fiber_width", 7))
    if not seams:
        return None
    geom = seam_paper_geometry(seams, direction, fiber_width,
                               int(manifest.get("seed", DEFAULT_SEED)))
    shadow_offset = max(0, int(manifest.get("seam_offset", 3)))
    with_shadow = int(manifest.get("seam_shadow", 26)) > 0
    mask = Image.new("L", (width, height), 0)
    d = ImageDraw.Draw(mask)
    for g in geom:
        for kind, coords in paper_shapes(g, shadow_offset, with_shadow):
            if kind == "poly":
                d.polygon(coords, fill=255)
            else:
                d.line(coords, fill=255, width=1)
    return mask


def mean_abs_diff(a: Image.Image, b: Image.Image) -> float:
    """Mean per-channel absolute difference in 0..1 on a small thumbnail."""
    t = 48
    a = a.resize((t, t))
    b = b.resize((t, t))
    total = 0.0
    for ch in ImageChops.difference(a.convert("RGB"), b.convert("RGB")).split():
        hist = ch.histogram()  # clean 256-bin L histogram: count per value
        total += sum(v * hist[v] for v in range(256))
    return total / (3.0 * t * t * 255.0)


def rendered_zone_sanity(rendered: Image.Image, crop: Image.Image,
                         src_rgb: Image.Image, zone_index: int) -> Tuple[Optional[str], List[str]]:
    """Sanity-check one rendered zone before it is allowed into the poster.

    Returns `(fail_reason, warnings)`. A fail means the render is unusable and
    the zone must be re-rendered:

    - aspect mismatch: the model produced a different orientation/format than
      the crop (e.g. a landscape full scene for a portrait strip) — pasting it
      would show a stretched horizontal image inside a vertical zone;
    - gross full-scene completion: the render matches the full source scene
      squished into the crop aspect much better than it matches its own slice
      (the symptom of "four repeated images at different abstraction levels").
    """
    warns: List[str] = []
    cw, ch = crop.size
    if cw <= 0 or ch <= 0:
        return ("zone crop has zero size.", warns)
    ar_r = rendered.width / max(1, rendered.height)
    ar_c = cw / max(1, ch)
    if max(ar_r, ar_c) > 0 and min(ar_r, ar_c) / max(ar_r, ar_c) < 0.8:
        return (f"rendered zone {zone_index + 1} aspect {rendered.width}x{rendered.height} "
                f"does not match its crop {cw}x{ch} — the model likely completed the "
                "scene at a different orientation; re-render it with the strict per-zone "
                "render block (keep the crop's aspect and orientation).", warns)
    rend = rendered.convert("RGB").resize(crop.size)
    own = mean_abs_diff(rend, crop.convert("RGB"))
    full = mean_abs_diff(rend, src_rgb.resize(crop.size))
    if own > 0.08:
        if full < own * 0.4:
            return (f"rendered zone {zone_index + 1} is a near-copy of the full source "
                    "scene — the model completed the photograph instead of the slice; "
                    "re-render it with the strict per-zone render block.", warns)
        if full < own * 0.55:
            warns.append(f"zone {zone_index + 1} render resembles the full source scene; "
                         "double-check it shows only its own slice.")
    return (None, warns)


def check_zone_renders(manifest: dict, src: Image.Image, workdir: Path) -> None:
    """Guard against the model completing the photograph inside a zone render.

    A correct abstract-zone render shows only its own slice, so it differs
    strongly from the full source scene squished into the crop's aspect. When
    the model instead re-rendered the FULL scene (or a wrong orientation),
    the render is unusable: fail so the agent must re-render the zone.
    """
    src_rgb = src.convert("RGB")
    for z in manifest["zones"]:
        if z["level"] == "anchor":
            continue
        rendered = Path(z["rendered"])
        crop_path = Path(z["crop"])
        if not rendered.is_file() or not crop_path.is_file():
            continue
        with Image.open(rendered) as ri, Image.open(crop_path) as ci:
            rend = ri.convert("RGB")
            crop = ci.convert("RGB")
        reason, warns = rendered_zone_sanity(rend, crop, src_rgb, z["index"])
        if reason:
            raise SystemExit(reason)
        for wmsg in warns:
            print(f"  warning: {wmsg}")


def count_components(mask: Image.Image, width: int, height: int) -> int:
    """Number of 4-connected components in a binary mask."""
    px = mask.load()
    seen = bytearray(width * height)
    comps = 0
    dq: deque = deque()
    for y in range(height):
        for x in range(width):
            i = y * width + x
            if px[x, y] > 127 and not seen[i]:
                comps += 1
                seen[i] = 1
                dq.append((x, y))
                while dq:
                    cx, cy = dq.popleft()
                    for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                        if 0 <= nx < width and 0 <= ny < height:
                            j = ny * width + nx
                            if px[nx, ny] > 127 and not seen[j]:
                                seen[j] = 1
                                dq.append((nx, ny))
    return comps


def check_collage_regions(masks: List[Image.Image], width: int, height: int) -> None:
    """Collage region sanity: every paper piece is substantial (no tiny
    scraps), connected (no islands), and exactly four owners tile the canvas.
    Visible areas are deliberately allowed to differ — no quarter-based
    balance requirement."""
    total = width * height
    for i, m in enumerate(masks):
        count = m.histogram()[255]
        frac = count / total
        if frac < 0.06:
            raise SystemExit(f"collage region {i + 1} is too small "
                             f"({frac * 100:.1f}% of canvas).")
        if frac < 0.10:
            print(f"  warning: collage region {i + 1} is small ({frac * 100:.1f}% of canvas).")
        comps = count_components(m, width, height)
        if comps != 1:
            raise SystemExit(f"collage region {i + 1} has {comps} disconnected "
                             "pieces (islands); collage topology broken.")


def collage_overlay_mask(manifest: dict, masks: List[Image.Image],
                         width: int, height: int) -> Optional[Image.Image]:
    """Union of every pixel the collage paper finish paints (deckled fiber
    bands + one-sided shadows). Used to exempt the intentional paper body from
    the anchor/head source-equality core, exactly like torn's paper seam."""
    if manifest.get("boundary") != "collage":
        return None
    seed = int(manifest.get("seed", DEFAULT_SEED))
    bands = collage_fiber_masks(masks, width, height,
                                manifest.get("paper_edge_width", 6), seed)
    union = bands[0].copy()
    for b in bands[1:]:
        union = ImageChops.lighter(union, b)
    if int(manifest.get("paper_shadow", 20)) > 0:
        z_order = manifest.get("z_order") or collage_z_order(manifest.get("layout", "horizontal-layered"))
        shadow = collage_shadow_mask(masks, z_order, width, height,
                                     manifest.get("collage_overlap", 5))
        union = ImageChops.lighter(union, shadow)
    return union


def boundary_seam_mask(manifest: dict, width: int, height: int) -> Optional[Image.Image]:
    """Exemption mask for the `natural` family: the paper-material seams drawn
    along the region boundaries (same geometry as `draw_paper_seams`, same
    seed/shadow switch), so the intentional paper pixels do not break the
    anchor/head source-equality core."""
    boundaries = manifest.get("collage_boundaries") or []
    if not boundaries:
        return None
    fiber_width = max(1, manifest.get("fiber_width", 7))
    seed = int(manifest.get("seed", DEFAULT_SEED))
    shadow_offset = max(0, int(manifest.get("seam_offset", 3)))
    with_shadow = int(manifest.get("seam_shadow", 26)) > 0
    mask = Image.new("L", (width, height), 0)
    d = ImageDraw.Draw(mask)
    for direction in ("vertical", "horizontal"):
        paths = [b["path"] for b in boundaries if b["dir"] == direction]
        if not paths:
            continue
        for g in seam_paper_geometry(paths, direction, fiber_width, seed):
            for kind, coords in paper_shapes(g, shadow_offset, with_shadow):
                if kind == "poly":
                    d.polygon(coords, fill=255)
                else:
                    d.line(coords, fill=255, width=1)
    return mask


def check_torn_topology(manifest: dict, masks: List[Image.Image],
                        width: int, height: int) -> None:
    """Torn-strip topology validation for --boundary torn.

    Fails when seams are missing, do not span the canvas, cross or collapse,
    or break the ordered four-region structure (islands, pockets, loops).
    Warns on large excursions from the nominal boundaries.
    """
    seams = manifest.get("seams")
    direction = manifest["direction"]
    axis = width if direction == "vertical" else height
    npos = height if direction == "vertical" else width
    if not seams or len(seams) != 3:
        raise SystemExit("torn layout requires exactly 3 internal seams.")
    for s in seams:
        if len(s) != npos:
            raise SystemExit("torn seam does not span the full canvas.")
        worst = max((abs(s[i] - s[i - 1]) for i in range(1, len(s))), default=0)
        if worst > max(12, int(0.02 * axis)):
            print(f"  warning: torn seam has a large local jump ({worst}px); "
                  "it may look jagged.")
    min_sep = max(4, int(axis * TORN_MIN_SEP_FRAC))
    for i in range(npos):
        if not (seams[0][i] + min_sep <= seams[1][i] and seams[1][i] + min_sep <= seams[2][i]):
            raise SystemExit("torn seams cross or collapse; ordered topology broken.")
    for k, s in enumerate(seams):
        nom = axis * (k + 1) / 4.0
        dev = max((abs(v - nom) for v in s), default=0)
        if dev > 0.2 * axis:
            raise SystemExit(f"torn seam {k + 1} deviates {dev:.0f}px from its nominal "
                             "boundary; ordered strip topology is destroyed.")
        if dev > 0.12 * axis:
            print(f"  warning: torn seam {k + 1} deviates up to {dev:.0f}px from its "
                  "nominal boundary.")
    # no islands / pockets / loops: every zone is one interval per row/column
    if direction == "vertical":
        for zi, m in enumerate(masks):
            px = m.load()
            for y in range(height):
                runs = 0
                prev_on = False
                for x in range(width):
                    on = px[x, y] > 127
                    if on and not prev_on:
                        runs += 1
                    prev_on = on
                if runs > 1:
                    raise SystemExit(f"Zone {zi + 1} has islands/pockets at row {y}; "
                                     "torn topology broken.")
    else:
        for zi, m in enumerate(masks):
            px = m.load()
            for x in range(width):
                runs = 0
                prev_on = False
                for y in range(height):
                    on = px[x, y] > 127
                    if on and not prev_on:
                        runs += 1
                    prev_on = on
                if runs > 1:
                    raise SystemExit(f"Zone {zi + 1} has islands/pockets at column {x}; "
                                     "torn topology broken.")
    print("  torn topology OK: 3 continuous ordered seams, no islands or pockets.")


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
    # natural/collage with the warm grade: Reality/head are composited from
    # the GRADED source, so the source-equality checks compare against it too.
    if (manifest.get("boundary") in ("natural", "collage")
            and manifest.get("paper_grade", "subtle") != "none"):
        src = robot_dreams_grade(src)

    zones = manifest["zones"]
    masks = [Image.open(z["mask"]).convert("L") for z in zones]
    check_tiling(masks, width, height)

    if manifest.get("boundary") == "torn":
        check_torn_topology(manifest, masks, width, height)
    elif manifest.get("boundary") in ("natural", "collage"):
        check_collage_regions(masks, width, height)
    check_zone_renders(manifest, src, args.workdir)

    feather = manifest.get("feather", 0)
    seam_band = None
    if manifest.get("boundary") == "collage":
        seam_band = collage_overlay_mask(manifest, masks, width, height)
    elif (manifest.get("boundary") == "natural"
            and manifest.get("seam_style", "paper") == "paper"
            and manifest.get("collage_boundaries")):
        seam_band = boundary_seam_mask(manifest, width, height)
    elif (manifest.get("boundary") == "torn"
            and manifest.get("seam_style") == "paper"
            and manifest.get("seams")):
        seam_band = paper_seam_mask(manifest, width, height)
    anchor = manifest["anchor"] - 1
    box = tuple(zones[anchor]["box"])
    anchor_core = opaque_core(masks[anchor], feather)
    if seam_band is not None:
        anchor_core = ImageChops.subtract(anchor_core, seam_band)
    if differs_masked(src.crop(box), out.crop(box), anchor_core.crop(box)):
        raise SystemExit("Anchor region differs from source; layout guarantee broken.")

    head_path = manifest.get("head_mask")
    if head_path:
        head = Image.open(head_path).convert("L")
        hb = head.getbbox()
        if hb is not None:
            head_core = opaque_core(head, min(feather, 8))
            if seam_band is not None:
                head_core = ImageChops.subtract(head_core, seam_band)
            if differs_masked(src.crop(hb), out.crop(hb), head_core.crop(hb)):
                raise SystemExit("Head region differs from source; head protection broken.")

    pf = manifest.get("primary_face")
    if pf:
        fb_box = tuple(pf)
        owners = [i for i, m in enumerate(masks) if mask_region_area(m, fb_box) > 0]
        if len(owners) > 1:
            print(f"  warning: PRIMARY face box {fb_box} spans zones {[o + 1 for o in owners]}; "
                  "the primary head is still source-protected, but a boundary cuts its region.")

    counts = [m.histogram()[255] for m in masks]
    if manifest.get("boundary") != "collage":
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
        f"head {'protected' if manifest.get('head_mask') else 'unprotected (no face boxes)'}, "
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
    parser.add_argument(
        "--direction",
        choices=("auto", "vertical", "horizontal"),
        default="auto",
        help="Slice direction: auto (default) derives it deterministically from "
             "image structure and aspect, vertical or horizontal override",
    )
    parser.add_argument(
        "--boundary",
        choices=("natural", "collage", "torn", "contour", "mask", "rect"),
        default="natural",
        help="Boundary family: natural (default) ONE photo in four natural "
             "regions, each a different abstraction, with the boundary "
             "expressed by a paper-material seam; collage layered torn-paper "
             "sheets; torn legacy ordered torn-strip; contour optional "
             "semantic contours; mask supplied masks; rect equal strips",
    )
    parser.add_argument(
        "--layout",
        choices=("auto", "horizontal-layered", "side-weighted", "vertical-strip", "horizontal-strip"),
        default="auto",
        help="collage mode layout: auto (default) derives it from the image, "
             "horizontal-layered layered paper layers, side-weighted central "
             "corridor with broad side fields, vertical/horizontal-strip reuse "
             "the legacy torn logic",
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
        "--primary-face",
        type=int,
        default=None,
        help="1-based index of the PRIMARY face box in --face-boxes — the only "
             "head that is hard source-protected and used for anchor selection. "
             "Default: auto = the largest face box (multi-person photos: only "
             "the primary head is locked to the source)",
    )
    parser.add_argument(
        "--head-mask",
        type=Path,
        help="Optional grayscale head mask (source size): the head region is always "
             "composited from the source regardless of which zone it falls in. "
             "Defaults to a generous expansion of --face-boxes covering hair and jaw/neck.",
    )
    parser.add_argument(
        "--levels",
        default=None,
        help="Permutation of 30,65,90 assigned in spatial order to the three "
             "non-anchor zones; default: auto-staggered seed/source-derived "
             "permutation (never the sequential 30,65,90)",
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
        help="contour mode only: max boundary deviation from the nominal equal edge, as a fraction of the slice axis",
    )
    parser.add_argument(
        "--torn-band",
        type=float,
        default=TORN_BAND_DEFAULT,
        help="torn mode: typical global seam deviation as a fraction of the slice axis "
             "(default 0.06 = ~6%%; local tears may reach ~9%%)",
    )
    parser.add_argument(
        "--torn-roughness",
        type=float,
        default=1.0,
        help="torn mode: multiplier for medium/high-frequency tear amplitude (0 = smoother)",
    )
    parser.add_argument(
        "--collage-band",
        type=float,
        default=0.12,
        help="collage mode: max paper-boundary deviation from its nominal profile, "
             "as a fraction of the slice axis",
    )
    parser.add_argument(
        "--collage-roughness",
        type=float,
        default=1.0,
        help="collage mode: multiplier for the medium tear irregularity (0 = smoother)",
    )
    parser.add_argument(
        "--collage-overlap",
        type=int,
        default=5,
        help="collage mode: visual paper-overlap / one-sided shadow offset in px",
    )
    parser.add_argument(
        "--paper-edge-width",
        type=int,
        default=6,
        help="collage mode: exposed deckled paper-fiber band width in px",
    )
    parser.add_argument(
        "--paper-shadow",
        type=int,
        default=20,
        help="collage mode: one-sided paper shadow opacity 0..255 (0 disables)",
    )
    parser.add_argument(
        "--paper-texture",
        choices=("subtle", "none"),
        default="subtle",
        help="collage mode: subtle deterministic paper grain overlay (default subtle)",
    )
    parser.add_argument(
        "--paper-grade",
        choices=("subtle", "none"),
        default="subtle",
        help="collage mode: subtle warm Robot Dreams-inspired cinematic grade "
             "over the abstract pieces (default subtle; Reality stays untouched)",
    )
    parser.add_argument(
        "--torn-scale",
        type=float,
        default=1.0,
        help="torn mode: multiplier for tear wavelength (larger = longer, broader tears)",
    )
    parser.add_argument(
        "--fiber-width",
        type=int,
        default=7,
        help="torn mode: max paper-fiber seam width in px (variable 2..N)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SEED,
        help="Deterministic random seed for the torn generator (same inputs -> same seams)",
    )
    parser.add_argument(
        "--seam-style",
        choices=("none", "paper"),
        default="paper",
        help="torn mode: overlay a warm torn-paper seam on the composed poster (paper) or leave hard cuts (none)",
    )
    parser.add_argument(
        "--seam-shadow",
        type=int,
        default=26,
        help="torn mode: paper shadow opacity 0..255 (0 disables the faint offset shadow; default 26)",
    )
    parser.add_argument(
        "--seam-offset",
        type=int,
        default=3,
        help="torn mode: paper shadow offset in px perpendicular to the seam (default 3)",
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
        "--auto-semantic",
        action="store_true",
        default=True,
        help="Use built-in semantic heuristics (person/sky/ground) in contour mode (default)",
    )
    parser.add_argument(
        "--no-auto-semantic",
        action="store_false",
        dest="auto_semantic",
        help="Disable built-in semantic heuristics in contour mode",
    )
    parser.add_argument(
        "--class-masks-dir",
        type=Path,
        help="Optional dir with person.png/architecture.png/road.png/sky.png class masks; "
             "supplied masks replace the built-in heuristic for that class in contour mode",
    )
    parser.add_argument(
        "--class-weights",
        default="",
        help="Optional per-class boundary weights, e.g. person=300,architecture=120,road=80,sky=60 "
             "(contour mode)",
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
        default=None,
        help="Soft transition width in px for zone boundaries (default: auto, "
             "~2%% of the smaller dimension, capped at 12.5%%; 0 = hard edges)",
    )
    return parser.parse_args()


def parse_class_weights(raw: str) -> Dict[str, int]:
    weights = dict(DEFAULT_CLASS_WEIGHTS)
    if not raw:
        return weights
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        if "=" not in part:
            raise SystemExit(f"Invalid class weight {part!r}; expected name=value.")
        name, value = part.split("=", 1)
        name = name.strip()
        if name not in weights:
            raise SystemExit(f"Unknown class {name!r}; choose from {sorted(weights)}.")
        weights[name] = int(value)
    return weights


def main() -> None:
    args = parse_args()
    if args.feather is not None and args.feather < 0:
        raise SystemExit("--feather must be non-negative.")
    if args.band <= 0 or args.min_zone <= 0:
        raise SystemExit("--band and --min-zone must be positive.")
    if args.torn_band <= 0 or args.torn_roughness < 0 or args.torn_scale <= 0:
        raise SystemExit("--torn-band/--torn-roughness/--torn-scale must be positive.")
    if args.collage_band <= 0 or args.collage_roughness < 0:
        raise SystemExit("--collage-band/--collage-roughness must be positive.")
    if args.collage_overlap < 0 or args.paper_edge_width < 1:
        raise SystemExit("--collage-overlap must be >= 0 and --paper-edge-width >= 1.")
    if not 0 <= args.paper_shadow <= 255:
        raise SystemExit("--paper-shadow must be in 0..255.")
    if not 0 <= args.seam_shadow <= 255:
        raise SystemExit("--seam-shadow must be in 0..255.")
    if args.seam_offset < 0:
        raise SystemExit("--seam-offset must be non-negative.")
    if args.fiber_width < 1:
        raise SystemExit("--fiber-width must be >= 1.")
    if args.mode == "prepare":
        if args.source is None or args.direction is None:
            raise SystemExit("--source and --direction are required for --mode prepare.")
        args.face_boxes = parse_face_boxes(args.face_boxes)
        if args.primary_face is not None and (args.primary_face < 1 or args.primary_face > len(args.face_boxes)):
            raise SystemExit(f"--primary-face must be 1..{len(args.face_boxes)} "
                             f"(index into --face-boxes); got {args.primary_face}.")
        if args.levels is not None:
            args.levels = [int(x) for x in args.levels.split(",")]
        args.class_weights = parse_class_weights(args.class_weights)
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
