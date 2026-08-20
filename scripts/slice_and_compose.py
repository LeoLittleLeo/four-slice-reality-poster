#!/usr/bin/env python3
"""Deterministic four-zone slicing and compositing for the Four-Slice Reality Poster.

The image model never decides the slicing. This script:

- defines four regions that tile the source exactly (no gaps, no overlaps):
  * --boundary torn     -> ordered torn-paper seams: three continuous
                           edge-to-edge multi-scale irregular seams over four
                           sequential regions (default)
  * --boundary contour  -> optional semantic + edge-aware contour boundaries
                           that follow silhouettes, rooflines, horizons
  * --boundary mask     -> four content-aware masks supplied by the agent,
                           normalized to exact tiling automatically
  * --boundary rect     -> four equal vertical/horizontal strips (fallback)
- writes one per-zone context crop for separate rendering (Scheme A) and the
  zone masks used for masked compositing and for full-canvas inpaint
  (Scheme B);
- composes the final poster by pasting rendered zones back at fixed
  coordinates, always keeping the Reality Anchor pasted from the source
  (--mode compose / --mode enforce-anchor), and optionally overlays a warm
  torn-paper seam for --boundary torn;
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
from collections import deque
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from PIL import Image, ImageChops, ImageDraw, ImageFilter

Box = Tuple[int, int, int, int]
LEVELS = (30, 65, 90)
BIG = 10 ** 6        # face penalty weight
STEP = 6             # max column change per row in boundary path search
BALANCE_RATIO = 2.5  # warn when max/min zone area ratio exceeds this

# Torn-strip (default) parameters. Each seam is conceptually
#   nominal position + broad low-frequency drift + medium tear + micro fiber.
DEFAULT_SEED = 42          # deterministic torn generator seed
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
# Torn-strip boundaries (multi-scale, deterministic, DEFAULT)
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


def draw_paper_seams(canvas: Image.Image, seams: List[List[int]], direction: str,
                     fiber_width: int, seed: int,
                     shadow_alpha: int = 26, shadow_offset: int = 3) -> Image.Image:
    """Overlay variable-width warm paper-fiber seams (visual only).

    The four zone masks keep exact tiling underneath; this only paints a
    narrow warm ivory / aged-paper edge along each seam with a faint offset
    shadow, so the poster reads as a physical editorial torn-paper collage.
    The ivory is **adaptive**: on bright local backgrounds it blends toward a
    darker aged-beige tone so the paper edge stays visible on both light and
    dark photographs (no hard-coded pure white). Deterministic via `seed`.
    """
    fiber_width = max(1, fiber_width)
    rng = random.Random(seed + 777)
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    bright_ivory = (243, 237, 219)     # warm off-white / aged cream beige
    aged_ivory = (198, 184, 152)       # darker aged-paper beige for bright backgrounds
    shadow = (30, 24, 14, max(0, min(255, shadow_alpha)))
    shadow_offset = max(0, shadow_offset)
    canvas_rgb = canvas.convert("RGB")
    for path in seams:
        if direction == "vertical":
            pts = [(path[r], r) for r in range(len(path))]
        else:
            pts = [(c, path[c]) for c in range(len(path))]
        if not pts:
            continue
        widths = [rng.randint(2, fiber_width) for _ in pts]  # 2..N px variable width
        # adaptive ivory: bright local background -> blend toward aged beige
        ivories = []
        for (x, y) in pts:
            r, g, b = canvas_rgb.getpixel((x, y))
            lum = (r + g + b) / 3.0 / 255.0
            blend = lum * 0.45  # 0 on black bg, up to 45% toward aged on white bg
            ivories.append(tuple(int(bright_ivory[c] * (1.0 - blend) + aged_ivory[c] * blend)
                                 for c in range(3)) + (255,))
        # faint shadow first (offset perpendicular to the seam), then ivory tube
        for (x, y), w in zip(pts, widths):
            r = w + 1
            if direction == "vertical":
                od.ellipse((x + shadow_offset - r, y - r, x + shadow_offset + r, y + r), fill=shadow)
            else:
                od.ellipse((x - r, y + shadow_offset - r, x + r, y + shadow_offset + r), fill=shadow)
        for (x, y), w, col in zip(pts, widths, ivories):
            r = w
            od.ellipse((x - r, y - r, x + r, y + r), fill=col)
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
        img = im.convert("RGB")

    head_boxes = head_boxes_from_faces(args.face_boxes, width, height)
    head_mask = None
    if args.head_mask is not None:
        head_mask = load_class_mask(args.head_mask, width, height, "head")
    elif head_boxes:
        head_mask = head_mask_from_boxes(head_boxes, width, height)

    # seam-avoidance boxes: expanded head boxes, else the supplied head mask bbox
    avoid_boxes = head_boxes
    if not avoid_boxes and head_mask is not None:
        hb = head_mask.getbbox()
        if hb is not None:
            avoid_boxes = [tuple(hb)]

    seams = None
    if args.boundary == "rect":
        masks = rect_masks(args.direction, width, height)
    elif args.boundary == "torn":
        seams = torn_paths(args.direction, width, height, avoid_boxes,
                           args.torn_band, args.torn_roughness, args.torn_scale,
                           args.seed)
        masks = masks_from_paths(args.direction, width, height, seams)
    elif args.boundary == "contour":
        edges, face = edge_and_face_images(img, width, height, head_boxes)
        sem = build_semantic_images(img, width, height, args.face_boxes,
                                    args.auto_semantic, args.class_masks_dir)
        masks = contour_masks(args.direction, width, height, edges, face,
                              head_boxes, args.band, args.min_zone,
                              sem, args.class_weights)
    else:  # mask
        masks = load_masks_dir(args.masks_dir, width, height)
    check_tiling(masks, width, height)

    if args.anchor == "auto":
        anchor = pick_anchor(masks, head_boxes)
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

    # Per-mode feather strategy: torn is a hard physical tear (1px anti-alias),
    # the other modes keep the broad soft transition.
    if args.feather is not None:
        feather = args.feather
    elif args.boundary == "torn":
        feather = 1
    else:
        feather = max(4, int(0.02 * min(width, height)))
        feather = min(feather, max(2, min(width, height) // 8))

    manifest = {
        "source": str(source),
        "direction": args.direction,
        "boundary": args.boundary,
        "size": [width, height],
        "anchor": anchor + 1,
        "margin": args.margin,
        "feather": feather,
        "seams": seams if seams else None,
        "seam_style": args.seam_style if args.boundary == "torn" else "none",
        "fiber_width": args.fiber_width,
        "seam_shadow": args.seam_shadow,
        "seam_offset": args.seam_offset,
        "torn_band": args.torn_band,
        "torn_roughness": args.torn_roughness,
        "torn_scale": args.torn_scale,
        "seed": args.seed,
        "head_mask": str(head_mask_path) if head_mask_path else None,
        "face_boxes": [list(b) for b in args.face_boxes],
        "zones": manifest_zones,
    }
    manifest_path = workdir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))

    print(f"Prepared deterministic four-zone layout -> {manifest_path}")
    print(f"Direction={args.direction}  boundary={args.boundary}  "
          f"size={width}x{height}  anchor=Logical Zone {anchor + 1}")
    if args.boundary == "torn":
        print(f"Torn: band={args.torn_band} roughness={args.torn_roughness} "
              f"scale={args.torn_scale} seed={args.seed} seam_style={args.seam_style}")
    if head_mask is not None:
        print(f"Head protection: {head_mask_path} "
              f"({', '.join(str(tuple(b)) for b in head_boxes) or 'supplied mask'})")
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
    anchor = manifest["anchor"] - 1
    zone = manifest["zones"][anchor]
    box = tuple(zone["box"])
    mask = Image.open(zone["mask"]).convert("L")
    with Image.open(source) as im:
        src = im.convert("RGBA")
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
        mask_region = soft_mask(mask_region, manifest.get("feather", 0))
        canvas.paste(region, (box[0], box[1]), mask_region)
        print(f"Pasted zone {z['index'] + 1} at {box[:2]} level={z['level']}")

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

    Uses the same seeded width sequence as `draw_paper_seams` (shadow reach
    included), so verify can exclude the intentional paper fiber from the
    exact source-equality core — the fiber is a visual overlay, like the soft
    transition band, and must not break the anchor/head guarantee.
    """
    seams = manifest.get("seams") or []
    direction = manifest.get("direction", "vertical")
    fiber_width = max(1, manifest.get("fiber_width", 7))
    if not seams:
        return None
    rng = random.Random(int(manifest.get("seed", DEFAULT_SEED)) + 777)
    mask = Image.new("L", (width, height), 0)
    d = ImageDraw.Draw(mask)
    shadow_offset = max(0, int(manifest.get("seam_offset", 3)))
    for path in seams:
        if direction == "vertical":
            pts = [(path[r], r) for r in range(len(path))]
        else:
            pts = [(c, path[c]) for c in range(len(path))]
        if not pts:
            continue
        widths = [rng.randint(2, fiber_width) for _ in pts]
        for (x, y), w in zip(pts, widths):
            r = w + 1  # shadow reach (with its perpendicular offset)
            if direction == "vertical":
                d.ellipse((x + shadow_offset - r, y - r, x + shadow_offset + r, y + r), fill=255)
            else:
                d.ellipse((x - r, y + shadow_offset - r, x + r, y + shadow_offset + r), fill=255)
            r = w  # ivory tube
            d.ellipse((x - r, y - r, x + r, y + r), fill=255)
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

    zones = manifest["zones"]
    masks = [Image.open(z["mask"]).convert("L") for z in zones]
    check_tiling(masks, width, height)

    if manifest.get("boundary") == "torn":
        check_torn_topology(manifest, masks, width, height)

    feather = manifest.get("feather", 0)
    seam_band = None
    if (manifest.get("boundary") == "torn"
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

    for fb in manifest.get("face_boxes", []):
        fb_box = tuple(fb)
        owners = [i for i, m in enumerate(masks) if mask_region_area(m, fb_box) > 0]
        if len(owners) > 1:
            print(f"  warning: face box {fb_box} spans zones {[o + 1 for o in owners]}; "
                  "the head mask still protects identity, but a boundary cuts the head region.")

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
    parser.add_argument("--direction", choices=("vertical", "horizontal"), help="Slice direction (prepare)")
    parser.add_argument(
        "--boundary",
        choices=("torn", "contour", "mask", "rect"),
        default="torn",
        help="Boundary style: torn (default) ordered torn-paper seams, contour "
             "(optional) semantic + edge-aware contours, mask supplied masks, "
             "rect equal strips",
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
        "--head-mask",
        type=Path,
        help="Optional grayscale head mask (source size): the head region is always "
             "composited from the source regardless of which zone it falls in. "
             "Defaults to a generous expansion of --face-boxes covering hair and jaw/neck.",
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
    if args.fiber_width < 1:
        raise SystemExit("--fiber-width must be >= 1.")
    if not 0 <= args.seam_shadow <= 255:
        raise SystemExit("--seam-shadow must be in 0..255.")
    if args.seam_offset < 0:
        raise SystemExit("--seam-offset must be non-negative.")
    if args.mode == "prepare":
        if args.source is None or args.direction is None:
            raise SystemExit("--source and --direction are required for --mode prepare.")
        args.face_boxes = parse_face_boxes(args.face_boxes)
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
