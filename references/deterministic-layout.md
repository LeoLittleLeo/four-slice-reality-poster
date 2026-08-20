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

## Boundary styles

`--boundary` selects how the four regions are cut. All three styles tile the
canvas exactly (no gaps, no overlaps) and keep the Reality Anchor protected.

### `contour` (default) — irregular, semantic + edge-aware boundaries

The script derives irregular boundaries automatically from the source, using
both low-level edges and semantic importance:

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

This is the recommended default: fully automatic, deterministic, irregular,
semantic-aware, and content-following.

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

1. `--mode prepare` defines the four regions, selects the anchor, assigns
   30%/65%/90%, writes one context crop per zone (region bounding box plus a
   small margin so the model can see its neighbors), and derives a **head
   protection mask** — a generous expansion of the `--face-boxes` covering
   hair and jaw/neck (or a supplied `--head-mask`).
2. The image model re-renders each **non-anchor** crop at its assigned level,
   using the per-zone render prompt block below. The model never sees a
   "four-slice poster" instruction; it only re-renders one slice.
3. `--mode compose` resizes each rendered crop back to the exact crop box,
   crops out the margin, and pastes the region back masked by its zone mask at
   fixed coordinates. The Reality Anchor is always composited from the source
   through its own zone mask, and the **head protection mask is then
   force-composited from the source on top** — so the primary head is the
   original photograph even when a face box straddles a zone boundary.

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
#    contour-aware irregular boundaries (default)
python scripts/slice_and_compose.py --mode prepare \
    --source photo.png --direction vertical --boundary contour \
    --anchor auto --face-boxes "100,60,180,150;330,120,410,210" \
    --levels 65,90,30 --workdir work/

#    supplied content-aware masks
python scripts/slice_and_compose.py --mode prepare \
    --source photo.png --direction vertical --boundary mask \
    --masks-dir my_masks/ --anchor auto --levels 65,90,30 --workdir work/

#    equal strips (fallback)
python scripts/slice_and_compose.py --mode prepare \
    --source photo.png --direction vertical --boundary rect \
    --anchor auto --levels 65,90,30 --workdir work/

# 2a. Render each non-anchor crop in work/crops/zone{i}.png with the
#     per-zone render prompt block, save to work/rendered/zone{i}.png

# 2b. Compose the poster
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

- `--direction vertical|horizontal` — slice direction.
- `--boundary contour|mask|rect` — boundary style (default `contour`).
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
  assigned in spatial order to the three non-anchor zones. Choose a
  non-mechanical permutation based on balance, meaning, rhythm, and color.
- `--margin 0.12` — context margin around each zone crop, as a fraction of the
  zone's bounding box. Give the model enough context to keep the scene
  semantically connected.
- `--band 0.18` — contour mode: max boundary deviation from the nominal equal
  edge, as a fraction of the slice axis.
- `--min-zone 0.15` — contour mode: minimum zone width/height, as a fraction
  of the slice axis.
- `--masks-dir DIR` — required for `--boundary mask`; four grayscale masks
  `zone0.png`..`zone3.png` (255 = region).
- `--feather N` — soft transition width in px for zone boundaries. Defaults to
  ~2% of the smaller image dimension (capped at 12.5%); `0` restores hard
  edges. Wider values soften boundaries further but shrink the exact-source
  core and can blur the four states together.

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
Re-render ONLY this image at {LEVEL}% abstraction from the original
photograph. Keep the exact same composition, framing, camera angle, subject
placement, and aspect ratio as the input. Keep it as ONE continuous slice
with no frames, borders, gutters, labels, or additional panels. Do not crop,
pad, or add margins of your own. Keep the warm, nostalgic, sunlit, slightly
retro Robot Dreams-inspired palette. The slice must remain clearly traceable
to this exact photograph while departing in structural information density as
instructed.
```

### Scheme B inpaint block

```text
Re-render ONLY the masked region at {LEVEL}% abstraction from the original
photograph. Keep every pixel outside the mask unchanged. Keep the masked
region's composition, framing, and subject placement identical to the source.
Do not add frames, borders, gutters, labels, or panels. Keep the warm,
nostalgic, sunlit, slightly retro Robot Dreams-inspired palette.
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
  mask; the anchor region never comes from the model in Scheme A, and is
  force-restored in Scheme B.
- The head protection mask is force-composited from the source on top of the
  anchor, so the primary head is the original photograph even when a face box
  straddles a zone boundary (e.g. in rect or mask mode, which have no
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
- Soft transitions are the default: every zone (including the Reality Anchor
  and the head) is composited through a softened mask, so boundaries blend
  smoothly instead of cutting at one razor pixel. Pass `--feather 0` for hard
  editorial edges, and avoid very wide feathers that blur the four states
  together.
- A one-shot full-poster generation must still pass `--mode verify`; any grid,
  strip, or contact-sheet output is rejected regardless of other qualities.

## Verification and rejection

`--mode verify` fails when:

- the output size differs from the source;
- the four zone masks do not tile the canvas exactly (any gap or overlap);
- the Reality Anchor core or head core differs from the source (the
  fully-opaque interior of the softened mask must equal the source; the soft
  transition band around it is intentionally blended and exempt); or
- the scene is structurally repeated (any layout where the full photograph
  appears more than once — grid, strip, contact sheet).

It warns (does not fail) when:

- the zone areas are unbalanced (max/min ratio above 2.5), or
- a non-anchor zone is pixel-identical to its source slice, meaning no
  abstraction was applied.
