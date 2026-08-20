# Deterministic Layout: Slicing and Compositing Pipeline

## Contents

- Why deterministic slicing
- The two schemes
- CLI reference
- Verbatim prompt blocks
- Engineering rules
- Verification and rejection

## Why deterministic slicing

The image model decides **how to render**, never **where to cut**. Every slicing
decision in this Skill is a deterministic integer operation performed by
`scripts/slice_and_compose.py`, so the deliverable is geometrically guaranteed
to be one continuous image tiled by four adjacent regions of the source — never
a 2x2 grid, strip, or contact sheet of four full-image versions.

The four states remain the four hidden logical zones of
[composition-and-anchor.md](composition-and-anchor.md); the script simply turns
them into exact pixel coordinates.

## The two schemes

### Scheme A — per-zone crop re-render (default)

1. `--mode prepare` cuts the source into four exact zones (vertical or
   horizontal), selects the anchor, assigns 30%/65%/90%, and writes one context
   crop per zone (zone rect plus a small margin so the model can see its
   neighbors).
2. The image model re-renders each **non-anchor** crop at its assigned level,
   using the per-zone render prompt block below. The model never sees a
   "four-slice poster" instruction; it only re-renders one slice.
3. `--mode compose` resizes each rendered crop back to the exact crop box,
   crops out the margin, pastes the region at its fixed integer coordinates,
   and force-pastes the Reality Anchor from the source.

### Scheme B — full-canvas mask inpaint

1. `--mode prepare --masks` additionally writes one full-canvas mask per
   non-anchor zone.
2. The image model inpaints the full canvas with the mask, keeping everything
   outside the mask unchanged.
3. `--mode enforce-anchor` force-pastes the source anchor back onto the
   inpainted canvas regardless of model behavior, then saves.

Scheme A is preferred: it is fully deterministic and never lets the model
modify more than one zone at a time.

## CLI reference

```text
# 1. Define the layout (deterministic)
python scripts/slice_and_compose.py --mode prepare \
    --source photo.png --direction vertical \
    --anchor auto --face-boxes "100,60,180,150;330,120,410,210" \
    --levels 65,90,30 --workdir work/ [--masks]

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

- `--direction vertical|horizontal` — four equal vertical or horizontal zones.
- `--anchor auto|1|2|3|4` — `auto` uses the largest face-box overlap per zone;
  when no face boxes are given, it falls back to Logical Zone 2 (second from
  left/top). `1..4` forces a zone (1-based, matching
  `restore_protected_anchor.py`).
- `--face-boxes "x0,y0,x1,y1;..."` — semicolon-separated face boxes used only
  for automatic anchor selection.
- `--levels 30,65,90` — a permutation of the three abstraction levels,
  assigned in spatial order to the three non-anchor zones. Choose a
  non-mechanical permutation based on balance, meaning, rhythm, and color.
- `--margin 0.12` — context margin around each zone crop, as a fraction of the
  zone's slice width/height. Give the model enough context to keep the scene
  semantically connected.
- `--masks` — also write full-canvas inpaint masks (Scheme B).
- `--feather N` — optional small blur ring (px) on pasted zone edges; keep it
  small or zero by default, since visible boundaries are desired.

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

- Never change the canvas size or zone aspect ratios: scaling zones is the
  source of seams, ghost edges, and double faces. All geometry is integer;
  the only resize allowed is the compose step's forced restore of a rendered
  crop to its exact crop box.
- The Reality Anchor is always pasted from the source; the anchor zone never
  goes through the model in Scheme A, and is force-restored in Scheme B.
- Append the same global color-identity sentence to every zone prompt so the
  four rendered slices stay inside one Robot Dreams-inspired universe.
- Do not feather boundaries by default; only a small optional `--feather` is
  permitted when it strengthens the composition.
- A one-shot full-poster generation must still pass `--mode verify`; any grid,
  strip, or contact-sheet output is rejected regardless of other qualities.

## Verification and rejection

`--mode verify` fails when:

- the output size differs from the source;
- the four zones do not tile the full canvas exactly (gaps or overlaps);
- the Reality Anchor region differs from the source;
- or the scene is structurally repeated (any layout where the full photograph
  appears more than once — grid, strip, contact sheet).

It warns (does not fail) when a non-anchor zone is pixel-identical to its
source slice, meaning no abstraction was applied.
