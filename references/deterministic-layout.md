# Deterministic Layout: Slicing and Compositing Pipeline

## Contents

- Why deterministic slicing
- Boundary styles
- The two schemes
- CLI reference
- Verbatim prompt blocks
- Engineering rules
- Verification and rejection

## Why deterministic slicing

The image model decides **how to render**, never **where to cut**. Every slicing
decision in this Skill is a deterministic operation performed by
`scripts/slice_and_compose.py`, so the deliverable is geometrically guaranteed
to be one continuous image tiled by four adjacent regions of the source — never
a 2x2 grid, strip, or contact sheet of four full-image versions.

The four states remain the four hidden logical zones of
[composition-and-anchor.md](composition-and-anchor.md); the script simply turns
them into exact pixel regions.

## Boundary families

`--boundary` selects how the four regions are cut. All five families tile the
canvas exactly (no gaps, no overlaps) and keep the Reality Anchor and the
primary head protected.

### `collage` (DEFAULT) — Layered Torn-Paper Collage

The default boundary family is a **layered torn-paper collage**: one designed
editorial object, not four strips with lines between them. Four paper pieces
are layered (z-ordered) with composition-driven sizes and **angular deckled
torn silhouettes** — straight-ish runs with sudden direction changes and sharp
V-notches, NOT smooth sine waves. The paper body, deckled fiber edges and
one-sided shadows are **region geometry**, not a decorative line drawn on top.

```text
TORN EDGE IS REGION GEOMETRY,
NOT A DECORATIVE LINE DRAWN ON TOP.
```

Allowed: layered stacking, local side insets, larger paper pieces,
irregular torn silhouettes, paper overlap and visual depth.
Forbidden: arbitrary blob segmentation, scattered fragments, floating
islands, contact sheets, 2×2 grids, gutters, or four full-photo copies.
The scene still appears exactly once.

The layout is selected by `--layout` (default `auto`):

- `horizontal-layered` — broad layered paper bands with independent torn
  silhouettes (middle-heavy nominal profile, NOT quarter-based). Default
  priority template.
- `side-weighted` — a central Reality corridor flanked by broad left/right
  paper fields plus a top (or bottom) supplementary layer; for alleys and
  central-perspective streets.
- `vertical-strip` / `horizontal-strip` — strip modes reusing the legacy torn
  logic, only when a modular strip layout is wanted.
- `auto` — derives the layout deterministically: wide scenes and
  horizontal-banded scenes -> `horizontal-layered`; portrait scenes with
  strong vertical structure (alleys, narrow streets) -> `side-weighted`.

Collage parameters (all deterministic via `--seed`):

- `--collage-band 0.12` — max paper-boundary deviation from its nominal
  profile (fraction of the slice axis).
- `--collage-roughness 1.0` — medium tear amplitude multiplier.
- `--collage-overlap 5` — visual paper-overlap / one-sided shadow offset (px).
- `--paper-edge-width 9` — exposed deckled paper-fiber band width (px).
- `--paper-shadow 20` — one-sided paper shadow opacity (0..255, 0 disables).
- `--paper-texture subtle|none` — subtle deterministic paper grain overlay
  (default `subtle`; Reality is re-composited clean, so it reads
  photographic while the paper pieces read printed).

### `torn` (legacy) — ordered torn-strip composition

Kept intact as the legacy / optional ordered layout:

```text
four sequential strip-like states
+
three continuous irregular seams around 1/4, 1/2, 3/4
```

Each seam is multi-scale (`nominal + broad low-frequency drift + medium tear
+ micro fiber`), continuous edge-to-edge, ordered, separated, head-avoiding,
and deterministic via `--seed`. It does NOT follow semantic contours and may
cross buildings, roads, bodies and sky.

Uses `--torn-band`, `--torn-roughness`, `--torn-scale`, `--seed`,
`--seam-style`, `--seam-shadow`, `--seam-offset`, and draws the torn-paper
seam overlay via `draw_paper_seams`. Do not break its compatibility.

### `contour` (optional) — Semantic Contour Boundary

`contour` is the **optional** semantic boundary family, NOT the default. It
derives irregular boundaries automatically from the source, using both
low-level edges and semantic importance:

1. Build an edge-energy image (`FIND_EDGES` + blur) and a face-penalty image
   from the supplied `--face-boxes`.
2. Build semantic class masks (importance weights) for `person`,
   `architecture`, `road`, and `sky`:
   - built-in heuristics (on by default, `--no-auto-semantic` to disable):
     `person` approximates silhouettes by extending each face box ~5 face
     heights down and ~2.5 face widths wide; `sky` flood-fills a bright
     blue-ish region from the top edge; `road` flood-fills a mid-tone
     desaturated region from the bottom edge. Heuristics are approximate and
     conservative; small misdetections are discarded by an area threshold.
   - supplied masks override per class: `--class-masks-dir` with optional
     `person.png`, `architecture.png`, `road.png`, `sky.png` (grayscale,
     source size). `architecture` has no built-in heuristic and comes only
     from supplied masks.
3. Combine into one per-pixel boundary score:
   `w_edge × FIND_EDGES + Σ w_class × class_boundary − inside_penalty(important) − edge_suppress × FIND_EDGES(low-importance) − BIG(face)`.
   Class boundaries (silhouettes, rooflines, the horizon, road lines) get a
   reward so boundaries align with them; important-class interiors (`person`,
   `architecture`) get a penalty so boundaries do not cut through them;
   low-importance interiors (`road`, `sky`) have their noise edges suppressed
   so boundaries are not dragged by clouds, texture, or road markings. Weights
   are soft preferences, tunable with `--class-weights`; faces keep their own
   hard penalty.
4. For each of the three internal boundaries, run a deterministic path search
   (sliding-window dynamic programming) from one canvas edge to the other,
   maximizing the combined score. Each boundary is constrained to a balance
   band around its nominal equal edge (`--band`, default 0.18 of the slice
   axis) and separated from its neighbors by at least `--min-zone` (default
   0.15), so the four regions stay roughly balanced in area.
5. A final pass snaps any boundary row that still cuts a face box off the face.

Semantic Contour is optional and is NOT the default boundary family. Choose
it explicitly (`--boundary contour`) when the composition genuinely benefits
from silhouette-, roofline-, architecture- or horizon-following boundaries.

### `mask` — supplied content-aware masks

The agent (or user) provides four grayscale masks `zone0.png` .. `zone3.png`
in `--masks-dir` (255 = region). The script:

- binarizes each mask;
- resolves overlaps deterministically (lower zone index wins);
- fills any gaps from the nearest owned pixel (multi-source BFS);
- validates that every zone is non-empty and that the four masks tile the
  canvas exactly.

Use this for hand-painted boundaries, semantic-segmentation masks, or
silhouette-aware regions. Keep the supplied masks roughly balanced in area;
the script warns when the max/min area ratio exceeds 2.5.

### `rect` — equal strips (fallback)

Four equal vertical or horizontal strips at exact integer coordinates
(`exact_edges` distributes any remainder so strips tile perfectly). Available
when a simple straight layout is the strongest design choice.

## The two schemes

### Scheme A — per-zone crop re-render (default)

1. `--mode prepare` defines the four regions (collage paper pieces, torn
   seams, contour boundaries, supplied masks or strips), selects the anchor,
   assigns 30%/65%/90%, writes one context crop per zone (region bounding box
   plus a small margin so the model can see its neighbors), and derives a
   **head protection mask** — a generous expansion of the `--face-boxes`
   covering hair and jaw/neck (or a supplied `--head-mask`).
2. The image model re-renders each **non-anchor** crop at its assigned level,
   using the per-zone render prompt block below. The model never sees a
   "four-slice poster" instruction; it only re-renders one slice.
3. `--mode compose` resizes each rendered crop back to the exact crop box,
   crops out the margin, and pastes the region back masked by its zone mask at
   fixed coordinates. The Reality Anchor is always composited from the source
   through its own zone mask, and the **head protection mask is then
   force-composited from the source on top** — so the primary head is the
   original photograph even when a face box straddles a zone boundary.

### Collage paper finish (compose, `--boundary collage`)

For collage the compose step adds the paper body:

1. after pasting the abstract pieces, a subtle warm Robot Dreams-inspired
   cinematic grade and a subtle deterministic paper grain are blended over
   them (`--paper-grade subtle`, `--paper-texture subtle`); the anchor and
   head are then re-composited from the **graded source** — Reality and the
   head receive the same warm grade (color only, no grain, no structure
   change), so the whole poster shares one warm palette while Reality still
   reads photographic;
2. each piece receives a deckled exposed-paper fiber band along its torn edge
   (`--paper-edge-width`, adaptive warm ivory, broken micro sections);
3. one-sided paper shadows fall only from higher-z pieces onto lower-z pieces
   (`--paper-shadow`, `--collage-overlap`), never on both sides of an edge.

All of it is visual only — the piece masks tile exactly underneath, and
`--mode verify` exempts only the intentional paper pixels from the
anchor/head source-equality core.

### Scheme B — full-canvas mask inpaint

1. `--mode prepare` always writes the zone masks to `workdir/masks/zone{i}.png`.
2. The image model inpaints the full canvas with one zone mask at a time,
   keeping everything outside the mask unchanged.
3. `--mode enforce-anchor` force-composites the source anchor back onto the
   inpainted canvas through the anchor mask regardless of model behavior.

Scheme A is preferred: it is fully deterministic and never lets the model
modify more than one zone at a time.

## CLI reference

```text
# 1. Define the layout (deterministic)
#    Layered Torn-Paper Collage (default); layout auto-derives
python scripts/slice_and_compose.py --mode prepare \
    --source photo.png --boundary collage --layout auto \
    --anchor auto --face-boxes "100,60,180,150;330,120,410,210" \
    --levels 65,90,30 --workdir work/

#    explicit side-weighted collage (alley / central corridor)
python scripts/slice_and_compose.py --mode prepare \
    --source alley.png --boundary collage --layout side-weighted \
    --anchor auto --face-boxes "300,120,380,210" \
    --levels 65,90,30 --workdir work/

#    legacy ordered torn-strip composition
python scripts/slice_and_compose.py --mode prepare \
    --source photo.png --boundary torn --direction vertical \
    --anchor auto --face-boxes "100,60,180,150" \
    --levels 65,90,30 --workdir work/

#    optional semantic contour boundaries
python scripts/slice_and_compose.py --mode prepare \
    --source photo.png --boundary contour --direction vertical \
    --anchor auto --face-boxes "100,60,180,150" \
    --levels 65,90,30 --workdir work/

#    supplied content-aware masks
python scripts/slice_and_compose.py --mode prepare \
    --source photo.png --boundary mask \
    --masks-dir my_masks/ --anchor auto --levels 65,90,30 --workdir work/

#    equal strips (fallback)
python scripts/slice_and_compose.py --mode prepare \
    --source photo.png --boundary rect --direction vertical \
    --anchor auto --levels 65,90,30 --workdir work/

# 2a. Render each non-anchor crop in work/crops/zone{i}.png with the
#     per-zone render prompt block, save to work/rendered/zone{i}.png

# 2b. Compose the poster (collage: paper grain + fiber edges + shadows)
python scripts/slice_and_compose.py --mode compose \
    --workdir work/ --output poster.png

# 2c. Scheme B: after inpainting the full canvas, enforce the anchor
python scripts/slice_and_compose.py --mode enforce-anchor \
    --workdir work/ --candidate inpainted.png --output poster.png

# 3. Verify the layout guarantee
python scripts/slice_and_compose.py --mode verify \
    --workdir work/ --output poster.png
```

Options:

- `--direction auto|vertical|horizontal` — slice direction for legacy torn /
  contour / rect (collage layouts define their own orientation). `auto`
  (default) derives it deterministically from image structure and aspect.
- `--boundary collage|torn|contour|mask|rect` — boundary family (default
  `collage`).
- `--layout auto|horizontal-layered|side-weighted|vertical-strip|horizontal-strip`
  — collage layout (default `auto`). `vertical-strip`/`horizontal-strip`
  reuse the legacy torn logic.
- `--collage-band 0.12` — collage: max paper-boundary deviation from its
  nominal profile (fraction of the slice axis).
- `--collage-roughness 1.0` — collage: medium tear amplitude multiplier.
- `--collage-overlap 5` — collage: visual paper-overlap / one-sided shadow
  offset in px.
- `--paper-edge-width 9` — collage: exposed deckled paper-fiber band width in
  px.
- `--paper-shadow 20` — collage: one-sided paper shadow opacity 0..255
  (`0` disables).
- `--paper-texture subtle|none` — collage: subtle deterministic paper grain
  (default `subtle`).
- `--paper-grade subtle|none` — collage: subtle warm Robot Dreams-inspired
  cinematic grade over the abstract pieces (default `subtle`; Reality and the
  head stay untouched).
- `--torn-band 0.06` — torn mode: typical global seam deviation as a fraction
  of the slice axis (local tears reach ~`torn_band * 1.5`).
- `--torn-roughness 1.0` — torn mode: multiplier for medium/high-frequency
  tear amplitude (`0` = smoother).
- `--torn-scale 1.0` — torn mode: multiplier for tear wavelength (larger =
  longer, broader tears).
- `--fiber-width 7` — torn mode: max paper-fiber seam width in px (variable
  2..N).
- `--seed 42` — deterministic seed for the torn generator (same inputs ->
  same seams).
- `--seam-style paper|none` — torn mode: overlay a warm torn-paper seam
  (default `paper`) or leave hard cuts (`none`).
- `--seam-shadow 0..255` — torn mode: paper shadow opacity (default 26; `0`
  disables the faint offset shadow).
- `--seam-offset px` — torn mode: paper shadow offset perpendicular to the
  seam (default 3).
- `--anchor auto|1|2|3|4` — `auto` uses the largest face overlap inside the
  zone masks; when no face boxes are given, it falls back to Logical Zone 2
  (second from left/top). `1..4` forces a zone (1-based, matching
  `restore_protected_anchor.py`).
- `--face-boxes "x0,y0,x1,y1;..."` — semicolon-separated face boxes used for
  automatic anchor selection, contour face avoidance, boundary snapping, the
  built-in `person` silhouette heuristic, and the default head protection mask.
- `--head-mask DIR/path` — optional grayscale head mask (source size). The head
  region is always composited from the source regardless of which zone it
  falls in, so the primary face can never be reconstructed. Defaults to a
  generous expansion of `--face-boxes` (hair + jaw/neck).
- `--auto-semantic` / `--no-auto-semantic` — built-in semantic heuristics for
  `person`/`sky`/`road` in contour mode (on by default).
- `--class-masks-dir DIR` — optional dir with `person.png`,
  `architecture.png`, `road.png`, `sky.png` class masks (grayscale, source
  size); a supplied mask replaces the built-in heuristic for that class.
- `--class-weights person=200,architecture=120,road=80,sky=60` — optional
  per-class boundary-reward weights in contour mode.
- `--levels 30,65,90` — a permutation of the three abstraction levels,
  assigned in spatial order to the three non-anchor zones. Default: an
  **auto-staggered** seed/source-derived permutation (never the sequential
  `30,65,90`), so the three abstract states are always non-linearly arranged.
  Pass an explicit permutation for composition-driven choices.
- `--margin 0.12` — context margin around each zone crop, as a fraction of the
  zone's bounding box. Give the model enough context to keep the scene
  semantically connected.
- `--band 0.18` — contour mode: max boundary deviation from the nominal equal
  edge, as a fraction of the slice axis.
- `--min-zone 0.15` — contour mode: minimum zone width/height, as a fraction
  of the slice axis.
- `--masks-dir DIR` — required for `--boundary mask`; four grayscale masks
  `zone0.png`..`zone3.png` (255 = region).
- `--feather N` — soft transition width in px for zone boundaries. Per-mode
  default: `collage` and `torn` use `1` px (hard paper cut, anti-aliased);
  `contour`, `mask` and `rect` use ~2% of the smaller image dimension (capped
  at 12.5%). Explicit `0` restores fully hard edges.

## Verbatim prompt blocks

### Full-poster one-shot block (fallback only)

Use only when per-zone rendering is impossible, and include it **verbatim**:

```text
ONE single continuous image at the source aspect ratio. The four states
Reality, 30%, 65%, and 90% abstraction occupy four ADJACENT REGIONS of that
one canvas. The regions tile the entire canvas and share edges with each
other. Each region shows a different SLICE (part) of the original photograph,
never the whole photograph. The scene appears exactly once. NEVER output a
2x2 grid, a contact sheet, a strip of four full-image versions, four panels
each containing the full scene, gutters, or panel gaps.
```

### Per-zone render block (primary path)

Render `work/crops/zone{i}.png` with the assigned level filled into `{LEVEL}`:

```text
This image is a CROP — a slice of a larger photograph, NOT the whole picture.
Re-render ONLY the content visible inside this crop at {LEVEL}% abstraction
from the original photograph. The rest of the photograph does not exist for
you: do NOT reconstruct, complete, extrapolate, or invent content outside
this crop, and do NOT show the full scene. The output must contain exactly
the same slice, the same framing, the same camera angle, the same subject
placement, and the same aspect ratio as the input crop — nothing new may
enter the frame. The output image must keep the SAME aspect ratio and
orientation as the input crop: a portrait crop stays portrait, a landscape
crop stays landscape — never rotate, never change the output format. Keep it
as ONE continuous slice with no frames, borders, gutters, labels, dividers,
or additional panels — never a grid, a contact sheet, or multiple versions
of the scene. Do not crop, pad, or add margins of your own. Keep the warm,
nostalgic, sunlit, slightly retro Robot Dreams-inspired palette. The slice
must remain clearly traceable to this exact photograph while departing in
structural information density as instructed.
```

### Collage per-zone render block (`--boundary collage`)

Use instead of the generic block when the boundary family is collage:

```text
This crop belongs to ONE Layered Torn-Paper Collage poster.

Keep the same editorial print / paper material language as the other zones.
Do not invent an unrelated artistic medium just to make this region different.

Differentiate this abstraction level primarily by:
- structural simplification,
- information density,
- shape merging,
- detail omission,
- graphic massing.

Preserve scene identity and major spatial relationships.

Do not output a self-contained poster or a full-image reinterpretation.
Render only this source-derived crop.
```

### Scheme B inpaint block

```text
Re-render ONLY the masked region at {LEVEL}% abstraction from the original
photograph. The mask marks the ONLY region you may change. Keep every pixel
outside the mask EXACTLY unchanged — do not redraw, complete, reformat, or
recompose content outside the mask. The output is the SAME single canvas at
the SAME aspect ratio, never a new image, a grid, a contact sheet, or
multiple versions of the scene. Keep the masked region's composition,
framing, and subject placement identical to the source. Do not add frames,
borders, gutters, labels, or panels. Keep the warm, nostalgic, sunlit,
slightly retro Robot Dreams-inspired palette.
```

## Engineering rules

- Never change the canvas size or region aspect ratios: scaling regions is the
  source of seams, ghost edges, and double faces. All geometry is integer; the
  only resize allowed is the compose step's forced restore of a rendered crop
  to its exact crop box.
- The four zone masks always tile the canvas exactly: overlaps are resolved,
  gaps are filled, and every zone is non-empty. The script refuses to prepare
  or verify a layout that leaves gaps or overlaps.
- The Reality Anchor is always composited from the source through its own zone
  mask (from the GRADED source in collage mode, so Reality shares the warm
  palette); the anchor region never comes from the model in Scheme A, and is
  force-restored in Scheme B.
- The head protection mask is force-composited from the source on top of the
  anchor (graded in collage mode — grading is color only, identity and pixels
  are preserved), so the primary head is the original photograph even when a
  face box straddles a zone boundary (e.g. in rect or mask mode, which have no
  automatic face avoidance). Give accurate `--face-boxes` or supply a
  `--head-mask` whenever a scene contains a primary person.
- Contour boundaries are semantic + edge-aware: they follow strong edges and
  class boundaries (silhouettes, rooflines, horizon, road lines), avoid
  important interiors (people, architecture) and faces. Built-in `sky`/`road`
  heuristics are approximate; when they misdetect a scene, supply
  `sky.png`/`road.png`/`person.png`/`architecture.png` in `--class-masks-dir`
  or disable them with `--no-auto-semantic`. If a boundary still cuts a face,
  re-run with a wider `--band`, a forced anchor, or supplied masks.
- Append the same global color-identity sentence to every zone prompt so the
  four rendered slices stay inside one Robot Dreams-inspired universe.
- Compose sanity-checks every rendered zone before pasting and **refuses to
  build the poster** when a render is unusable: an aspect/orientation
  mismatch with its crop (a landscape full scene for a portrait strip) or a
  near-copy of the full source scene (the model completed the photograph).
  Re-render the offending zone with the strict per-zone render block.
- A one-shot full-poster generation is a fallback only: it must keep the
  source aspect ratio and orientation (portrait stays portrait), must still
  pass `--mode verify`, and any grid, strip, contact sheet, or repeated-scene
  output is rejected regardless of other qualities.
- Soft transitions are the default for `contour`, `mask` and `rect`: every
  zone (including the Reality Anchor and the head) is composited through a
  softened mask, so boundaries blend smoothly. `torn` is the opposite — it
  uses hard/near-hard cuts (`feather = 1`) and paints a physical torn-paper
  seam overlay, because its look is a hard tear, not a soft blend. Pass an
  explicit `--feather` to override either way, and avoid very wide feathers
  that blur the four states together.
- The torn paper-seam overlay is visual only: the four zone masks underneath
  still tile the canvas exactly, and `--mode verify` exempts only the
  intentional paper-fiber pixels (like the soft transition band) from the
  exact source-equality check of the anchor/head core.
- The `collage` and `torn` algorithms are fully isolated: `collage` never
  calls `build_score()`/`optimize_boundary()` (those belong to `contour`),
  and `contour` never uses the torn/collage noise generators.
- Collage paper finish is z-ordered: each piece casts a one-sided shadow only
  onto the pieces below it (an upper paper covers lower papers), and the
  deckled fiber bands follow each piece's own torn silhouette — never a
  continuous ivory tube or a white stroke along a straight seam.
- Old manifests (e.g. torn manifests without `layout` / collage fields) keep
  working: compose/verify read every new field through `manifest.get(...)`
  defaults, and the collage finish only applies when `boundary == "collage"`.
- A one-shot full-poster generation must still pass `--mode verify`; any grid,
  strip, or contact-sheet output is rejected regardless of other qualities.

## Verification and rejection

`--mode verify` fails when:

- the output size differs from the source;
- the four zone masks do not tile the canvas exactly (any gap or overlap);
- the Reality Anchor core or head core differs from the source (in collage
  mode the source reference is the GRADED source; the fully-opaque interior
  of the softened mask must equal it exactly, while the soft transition band,
  the torn paper-fiber pixels, and the collage paper finish are exempt);
- for `collage`: a paper piece is too small (< ~6% of the canvas), or a piece
  has disconnected islands; pieces may have very different areas — no
  quarter-based balance check is applied;
- for `torn`: the three seams are missing, do not span the full canvas, cross
  or collapse, or the zones contain islands/pockets/loops (ordered strip
  topology broken); a seam deviating more than ~20% of the slice axis from
  its nominal boundary is also rejected; or
- the scene is structurally repeated (any layout where the full photograph
  appears more than once — grid, strip, contact sheet).

It warns (does not fail) when:

- a non-anchor zone is pixel-identical to its source slice (no abstraction
  applied),
- a collage piece is small (< ~10% of the canvas),
- a torn seam deviates far from its nominal boundary (warns above ~12% of the
  slice axis) or has a large local jump, or
- a rendered abstract zone resembles the FULL source scene instead of its own
  slice — the symptom of "four repeated images at different abstraction
  levels", caused by the image model completing the photograph inside a zone
  render.

Compose and verify both fail when a rendered zone is a gross full-scene copy
or has a wrong aspect/orientation; re-render that zone with the strict
per-zone render block.
