---
name: four-slice-reality-poster
description: "Transform a user-supplied photograph into ONE continuous poster: the same photo jointly composed of four natural regions, each region differing only in its abstraction treatment (Reality + 30%, 65%, 90% source-derived abstraction states), with the boundary between regions expressed by a paper-material seam — not four separate paper sheets. The scene appears exactly once; only the primary head is hard-protected. Optional Layered Torn-Paper Collage, legacy Torn-Strip, Semantic Contour, Mask, and Rect boundary families are also available. Accept a visually coherent generated face when identity and anatomy are already sound; use source-face restoration only as a gated fallback that demonstrably improves the result."
---

# Four-Slice Reality / Abstraction Poster

Create ONE continuous poster: the same photograph jointly composed of four **natural regions**, each region differing only in its abstraction treatment (Reality + 30%, 65%, 90% source-derived abstraction states). The boundary between regions is expressed by a **paper-material seam** — the regions are parts of one photo, NOT four separate paper sheets.

## Default visual objective

**One photo, four natural regions; each region differs only by abstraction.**

The final image should read as **one photograph** divided into four natural regions — each region just has a different abstraction treatment. The paper material layer is the **representation of the boundary** (a torn-paper seam where the abstraction changes), never a set of separate paper sheets.

Core principle:

```text
ONE PHOTO
+ FOUR NATURAL REGIONS
+ EACH REGION DIFFERS ONLY BY ABSTRACTION
+ BOUNDARY EXPRESSED BY A PAPER-MATERIAL SEAM
```

The four states must be immediately legible while the poster stays one coherent photograph. Do not require visible rectangular bands. Keep the four regions substantial; do not reduce them to one dominant image plus three scraps. Boundaries are natural (composition-driven, smooth organic or content-aware) and may be crossed by continuous objects that change rendering language at the seam (One-Scene / One-Object Ownership).

## Final Output Layout — Hard Constraint

The deliverable is **one continuous image at the source aspect ratio**. The four states (Reality, 30%, 65%, 90%) are four **adjacent regions** of that one canvas: they tile the entire canvas, share edges with each other, and **each region — Reality included — shows a different slice of the original photograph**. Reality is the photographic version of ITS slice only; it is never the full image. The scene appears **exactly once** across the four slices. Never deliver a 2×2 grid, a contact sheet, a strip of four full-image versions, four panels each containing the full scene, gutters, or panel gaps.

Prefer the deterministic path: define the four zones, render each abstract zone separately, and compose with `scripts/slice_and_compose.py` — the image model never decides the slicing. See [deterministic-layout.md](references/deterministic-layout.md) for the pipeline, CLI usage, and the verbatim prompt blocks.

When the image model receives a full-poster prompt, include this block **verbatim**:

```text
ONE single continuous image at the source aspect ratio. The four states
Reality, 30%, 65%, and 90% abstraction occupy four ADJACENT REGIONS of that
one canvas. The regions tile the entire canvas and share edges with each
other. Each region shows a different SLICE (part) of the original photograph,
never the whole photograph. The scene appears exactly once. NEVER output a
2x2 grid, a contact sheet, a strip of four full-image versions, four panels
each containing the full scene, gutters, or panel gaps.
```

## Default Color Identity — Robot Dreams-Inspired

Treat the Robot Dreams-inspired cinematic palette as a **default visual identity of this Skill**, not merely an optional grading suggestion.

Unless the user explicitly requests another color direction, make the final poster inhabit a warm, nostalgic, sunlit, slightly retro, emotionally gentle color world inspired by the broad visual feeling of *Robot Dreams*.

Build primarily from a controlled family of:

- cream and warm beige;
- dusty peach and muted coral;
- terracotta and warm brown;
- sunlit ochre and muted yellow;
- dusty sky blue and powder blue;
- muted teal and softened blue-green;
- sage and dusty olive;
- restrained tomato red, coral, navy, or warm denim accents.

Do not force every color into every image. Adapt the palette to the source while preserving this broad emotional identity.

### Robot Dreams Shared Palette System

The four regions share **one shared limited palette** — the photograph's own
colors mapped through the uniform warm Robot Dreams-inspired grade. The
palette is ONE set of hues, accents, and relationships used by all four
regions; each abstraction region may **rebalance the proportions** of those
shared colors (30% stays close to the source's local color distribution, 65%
groups the shared colors into broader masses, 90% narrows the proportion set
toward the most essential shared hues) — but must never change WHICH colors
are available.

```text
SOURCE PHOTO
↓
GLOBAL ROBOT-DREAMS PALETTE MAPPING
↓
shared limited palette
↓
each abstraction region may rebalance
the proportions of those shared colors
↓
ONE coherent poster
```

Regions must NOT be separated by region-specific color roles, dominant hues,
warm/cool contrasts, or value roles: that would turn the poster back into
four differently-colored design modules instead of one photo.

In other words: a region's color is always derived from ITS OWN slice of the
source, transformed by that region's abstraction level (30% stays closest to
the photo's local color, 90% is most interpretive) — the shared palette
stays the same, only its proportions are rebalanced. Assigning clearly
different dominant color roles per region (e.g. Slice A → terracotta, Slice
B → cream, Slice C → dusty blue, Slice D → ochre) is an OPTIONAL artistic
choice only when the user explicitly requests it — never the default.

### Color Separation

The boundary between regions is expressed by the paper-material seam, not by
per-region color contrast. Do not rely on hue shifts, warm/cool breaks, or
value jumps between regions to make the states readable — the states differ
structurally (information density, method), and the seam marks the boundary.
Never intentionally shift one region's color away from the photograph to
create a divider.

### Color Character

Default toward medium-low to medium saturation, soft but alive color, gentle sunlight, open highlights, calm shadows, slightly faded cinematic color, warm/cool balance, and a small repeated accent set.

Avoid neon cyberpunk, purple-magenta sci-fi glow, random rainbow abstraction, aggressive HDR, crushed blacks, glossy commercial-advertising color, cold steel monochrome, lifeless gray, and excessive candy saturation unless the user explicitly requests them.

### Core Color Rule

```text
ONE PHOTO'S COLOR IDENTITY
+ UNIFORM WARM ROBOT DREAMS-INSPIRED GRADE
+ ABSTRACTION DIFFERS BY STRUCTURE, NOT BY REGION COLOR
=
ONE COHERENT POSTER THAT IS STILL ONE PHOTO
```

Do not separate regions by assigning them different dominant color roles. Follow [cinematic-color-system.md](references/cinematic-color-system.md) for detailed implementation.

## Required reading

Before producing the artwork, read:

- [composition-and-anchor.md](references/composition-and-anchor.md) for slicing, anchor selection, level assignment, and continuity.
- [abstraction-language.md](references/abstraction-language.md) for the approved method library and level calibration.
- [cinematic-color-system.md](references/cinematic-color-system.md) for the default warm, nostalgic, Robot Dreams-inspired shared palette and level-specific color compression.
- [intentional-modular-composition.md](references/intentional-modular-composition.md) for readable module boundaries, controlled contrast, and optional secondary transitions.
- [subjects-validation.md](references/subjects-validation.md) for people, architecture, hard constraints, and final validation.
- [deterministic-layout.md](references/deterministic-layout.md) for the deterministic slicing/compositing pipeline, CLI usage, and the verbatim render prompt blocks.

## Face Identity Lock & Protected Source Region

Preserve primary-face identity without assuming that pixel restoration is always necessary. Keep the strongest visually coherent candidate eligible for final delivery.

In the **deterministic pipeline** the primary head is source-protected, geometrically, by construction: the script derives a head protection mask and always force-composites it from the source after the anchor, and `--mode verify` rejects any output where the head region differs from the source. No Face Restoration Gate runs on this path.

The **Face Restoration Gate** below applies ONLY to one-shot / non-deterministic fallback cases where exact source-head compositing was not available. On that fallback path a generated face may be kept if identity and anatomy are already sound; the gate exists to decide when to attempt source restoration. There is no logical conflict: deterministic path = source head; fallback path = gate decides.

**Only the primary head is hard-locked to the Reality state.** Everything else — the rest of the person's body, buildings, crowds, and all other subjects — may deliberately exist across multiple abstraction states at the same time. A building whose roof stays photographic while its façade lives at 65% and its silhouette at 90% is a feature, not an error. Cross-state coexistence of body parts and architecture is allowed and encouraged when it strengthens the poster; the only hard invariances are head identity/continuity and the absence of accidental duplication (clones, double faces, ghost edges).

In the deterministic pipeline the head lock is geometric, not just a prompt instruction: the script derives a head protection mask (generous expansion of `--face-boxes`, or a supplied `--head-mask`) and always force-composites it from the source after the anchor — so the primary face is the original photograph even when a face box straddles a zone boundary, and `--mode verify` rejects any output where the head region differs from the source.

### Face Restoration Gate (one-shot / non-deterministic fallback ONLY)

**This gate does NOT run on the deterministic pipeline.** On the deterministic path the primary head is source-composited by construction and checked by `--mode verify`; there is nothing to gate. The gate below applies ONLY when a one-shot / non-deterministic generation produced the poster and exact source-head compositing was not available.

After producing the strongest visually coherent candidate, inspect the primary face before performing any source restoration. When it already meets the following conditions, accept it as the selected face candidate, skip restoration, and continue to poster-level art direction and validation:

- recognizable identity;
- correct facial proportions;
- natural eye, nose, and mouth placement;
- coherent jaw and cheek contour;
- coherent hairline;
- coherent face-to-neck connection; and
- no obvious facial generation artifact.

Do not composite source pixels merely to increase pixel equality. Attempt restoration only when the coherent candidate has a meaningful identity or facial-structure failure.

Use this decision flow:

```text
coherent candidate
→ Face Restoration Gate
    ├─ face acceptable → skip restoration → poster-level validation
    └─ face unacceptable → attempt restoration
                              ↓
                         validate restoration
                              ↓
                    select only if visually better
                              ↓
                    poster-level validation
```

Prefer restoration methods in this order:

1. no restoration when the face is acceptable;
2. irregular semantic face mask;
3. aligned or registered source-face restoration;
4. rectangular face-box restoration only as a last fallback.

Do not perform pixel-level restoration when source and candidate face geometry cannot be verified as aligned.

Use this execution model:

1. Determine the four logical zones, Reality Anchor, primary face, head contour, hairline, jaw, neck, shoulders, clothing edge, and cross-boundary body connections.
2. Preserve the strongest visually coherent generated candidate before any restoration.
3. Run the Face Restoration Gate. Skip restoration when identity, facial anatomy, hairline, and face-to-neck continuity are acceptable, then continue to poster-level validation.
4. If restoration is necessary, create Candidate B with an irregular semantic face mask or verified aligned source face. Use a rectangular face box only as a last fallback.
5. Compare Candidate A, the pre-restoration coherent candidate, with Candidate B. Select B only when identity improves and anatomy, head/jaw/neck continuity, skin tone, and compositing quality remain natural.
6. Reject B and return to A whenever restoration introduces a facial patch, geometry mismatch, hairline mismatch, skin-tone discontinuity, or unnatural proportions.

Never replace a visually coherent face with a source-restored face when restoration makes the person less natural. A restoration candidate must demonstrate actual visual improvement before it may become final.

Exact source pixels are preferred only when they can be restored without damaging visual coherence. Identity preservation—not mandatory pixel identity—is the final goal.

Required invariant:

```text
final primary face identity = preserved
final head continuity = coherent head contour + face-to-neck connection (hard)
final body/building presence = optional across abstraction states;
                               prefer readable fragments, never accidental clones
```

Never accept:

```text
final candidate = restoration with a facial patch, geometry mismatch, or broken head/body continuity
```

**A visually coherent candidate with preserved face identity is preferable to a source-restored candidate that introduces facial or human stitching errors.**

## Workflow

1. Inspect the supplied photograph. Identify dimensions, orientation, semantic flow, primary people and faces, architecture, landmarks, important objects, dominant shapes, and palette.
2. Choose the collage layout (and slicing direction for non-collage modes). Use the script's deterministic `--layout auto` (default): wide or horizontally-layered scenes -> `horizontal-layered`; portrait alleys / central-perspective streets -> `side-weighted`; strip modes only when a modular strip layout is wanted. Override only when the semantic composition clearly favors another layout. Preserve the source aspect ratio and overall rectangular canvas.
3. Define the slicing deterministically with the script — never by the image model:
   `python scripts/slice_and_compose.py --mode prepare --source <photo> --boundary <natural|collage|torn|contour|mask|rect> [--layout <auto|horizontal-layered|side-weighted|vertical-strip|horizontal-strip>] [--direction <auto|vertical|horizontal>] [--face-boxes "<x0,y0,x1,y1;...>"] --levels <permutation> --workdir work/ [--masks-dir <dir>]`.
   Run it with `--boundary natural` (the default — it is also what happens when the flag is omitted) unless you explicitly want another family.
   Boundary family: `natural` (default) — ONE photo in four natural regions (composition-driven layouts), each region a different abstraction, with the boundary expressed by a paper-material seam; no z-order, no sheet bodies, no sheet grain. `collage` (optional) builds layered torn-paper sheets with a full paper finish. `torn` (legacy) keeps ordered torn-strip composition. `contour` (optional) derives semantic + edge-aware contours. `mask` accepts four supplied masks normalized to exact tiling; `rect` falls back to equal strips. The script writes the four exact pixel regions (masks), the manifest, per-zone context crops, and the zone masks. Follow [deterministic-layout.md](references/deterministic-layout.md).
4. Select exactly one Reality Anchor. The script's `--anchor auto` implements: 1) primary-face ownership (largest face overlap inside the region masks); 2) for `side-weighted` layout without a face, the central Reality corridor; 3) Logical Zone 2 fallback. Architecture/crowd anchors are NOT auto-detected by the script — choose them explicitly with `--anchor 1..4` when the scene's main subject is a building or crowd. Keep the state-ownership regions fixed (never re-shape them to protect content).
5. Identify the primary face and surrounding head/body continuity context before generation; do not pre-commit to source-pixel restoration. Pass accurate `--face-boxes` (or a `--head-mask`) so the script derives a generous head protection region covering hair and jaw/neck — the PRIMARY head is force-composited from the source regardless of which zone it falls in. In multi-person photos only the primary head is source-protected: the script picks the largest face box by default, or `--primary-face N` forces a specific box; secondary faces are regular content.
6. Assign 30%, 65%, and 90% abstraction exactly once to the remaining regions. The script's default is an **auto-staggered permutation** (seed/source-derived, never the sequential `30,65,90` — e.g. `90,65,30`, `65,30,90`, `30,90,65`), so the three abstract states are always non-linearly arranged. Pass an explicit `--levels` (any permutation) for composition-driven choices. Choose based on balance, meaning, rhythm, and color—not distance from the anchor. As a default suggestion (not a hard rule), the strongest abstraction often works well at an outer region (top, bottom, or side), while Reality benefits from a central or compositionally important region.
7. Establish the Robot Dreams-inspired default color identity before generating the abstract modules. Treat this palette direction as a core visual constraint, not optional finishing. The four regions share ONE shared limited palette under the uniform warm grade (Robot Dreams Shared Palette System) — each region shows its own slice of the photo's color passed through that region's abstraction method, rebalancing the proportions of the shared colors; never assign distinct dominant color roles, hue shifts, or palette identities per region. Apply any Reality Anchor grading only deterministically and non-structurally, or leave the Anchor unchanged.
8. Render each abstract zone **separately** (primary path). The Primary Abstraction Method is routed **deterministically by the script** through the **Level-Gated system** in two levels: the **AUTO ROUTER** (default) measures each ACTUAL region via its zone mask (saturation, hue variance, warmth, edge density, detail — color + structure, no semantics) and picks the best-fitting method inside that level's pool; the **AGENT OVERRIDE** (`--methods "30:...,65:...,90:..."`) is semantic routing (subject + structure + color) on top — the script **refuses** any method from another level's pool or Color Blocking (Supporting-only), so the pools stay pairwise disjoint and `30% ≠ 65% ≠ 90%` is guaranteed by construction. `--mode prepare` writes every zone's `primary_method` into the manifest. Treat abstraction as structural reinterpretation, never filter intensity. Enforce perceptual separation across 30%, 65%, and 90% through structural information density—not merely rendering style, palette, brush texture, or medium. Reduce, merge, group, or omit non-essential repeated components when this improves clarity, but preserve the primary person, identity-critical face, dominant crowd event, landmark architecture, and major scene-defining masses. Render each non-anchor context crop (`work/crops/zone{i}.png`) with the per-zone render prompt block from [deterministic-layout.md](references/deterministic-layout.md) (use the collage block when `--boundary collage`), filling `{LEVEL}` with the manifest's zone level, `{PRIMARY_METHOD}` with the manifest's routed `primary_method`, and `{SUPPORTING_METHODS}` with any supporting methods or `none`; the model never decides the poster layout and never receives a whole-poster slicing instruction. **Each zone render must show ONLY its own slice of the photograph, at the same aspect ratio and orientation as its crop — the model must never complete, reconstruct, or re-invent the rest of the scene inside a zone render.** Subject placement inside the slice stays fixed for every method EXCEPT Fragmentation and Collage Abstraction, which may displace, offset, crop, or re-layer the slice's own elements (that IS the method) while still never importing content from outside the crop and never duplicating a recognizable subject. Compose refuses to build the poster when a zone render has the wrong aspect (e.g. a landscape full scene for a portrait strip) or is a near-copy of the full scene; if either happens, reject it and re-render with the strict slice prompt block.
9. Compose deterministically: `python scripts/slice_and_compose.py --mode compose --workdir work/ --output <final>.png`. The script pastes the rendered zones back at fixed coordinates through their zone masks, always keeps the Reality Anchor composited from the source, and force-composites the head protection mask from the source on top — the primary face is the original photograph even when a face box straddles a zone boundary. For `natural` (default) a subtle warm Robot Dreams-inspired grade is applied uniformly (`--paper-grade`), Reality/head re-composited from the graded source, and the **paper material layer is drawn ONLY at the region boundaries as torn-paper seams** (`--seam-style paper`) — no z-order, no sheet bodies, no sheet grain; each region is just the photo re-rendered at its abstraction level. For `collage` the full paper finish (fiber edges, one-sided shadows, grain) is applied. For `torn` the cuts are hard (`feather = 1`) with the torn-paper seam overlay. `contour`/`mask`/`rect` use a soft transition band. For Scheme B, inpaint the full canvas with `work/masks/zone{i}.png` and run `--mode enforce-anchor` instead. The four visible modules are the natural regions (default), collage paper pieces, torn ordered regions, contour regions, supplied masks, or rect strips; they tile the canvas exactly with no gaps or overlaps. Keep them substantial and readable, and preserve the Skill's modular color and palette rules.
10. One-shot full-poster generation is a fallback only: if used, the model prompt MUST contain the Final Output Layout hard-constraint block verbatim, MUST keep the source aspect ratio and orientation (portrait stays portrait), and the result must pass `--mode verify`. Reject any grid, strip, contact sheet, or repeated-scene output.
11. (One-shot fallback path ONLY — SKIP on the deterministic pipeline, whose primary head is already source-composited by compose and checked by `--mode verify`.) On the fallback poster, run the Face Restoration Gate. If Candidate A is acceptable, skip restoration and retain A. Otherwise attempt a geometrically verified irregular-mask or aligned restoration to create Candidate B.
12. (One-shot fallback path ONLY.) Let Candidate B replace Candidate A only when identity improves without unnatural anatomy, patch appearance, skin mismatch, or broken head/jaw/neck/body continuity.
13. Art-direct the poster using shared motifs, rhythm, limited palette relationships, or structural echoes without weakening face identity or human continuity.
14. Run `python scripts/slice_and_compose.py --mode verify --workdir work/ --output <final>.png`, then inspect face identity, head/body continuity, four-state readability, intentional boundary design, and poster-level coherence, and validate every required condition in [subjects-validation.md](references/subjects-validation.md) before delivery. Reject any output that repeats the scene (2×2 grid, strip, contact sheet) regardless of other qualities.

## Decision priority

Resolve conflicts in this order:

1. Primary Face Identity and Natural Facial Coherence.
2. Primary Head Identity and Continuity. (Body and building continuity are soft preferences; cross-state presence is allowed and encouraged.)
3. Reality Anchor Role and Local Source Preservation.
4. Architectural Identity.
5. Four-State Readability, Logical-Zone Ownership, Abstraction Assignment, and Composition Topology. In the default natural family: one photo, four natural regions, no arbitrary blobs/islands/pockets and no separate paper sheets; in the optional collage family: layered paper pieces, composition-driven sizes; in the legacy torn family: ordered sequential regions.
6. Robot Dreams-Inspired Color Identity (combined with the shared editorial print/paper material language in collage mode).
7. Intentional Modular Boundary Design.
8. Artistic Experimentation.

The Final Output Layout hard constraint (one continuous image, four adjacent regions, scene appears exactly once) outranks every rule in this list: reject any grid, strip, or contact-sheet output no matter how well it satisfies lower-priority goals. In the legacy torn family, Ordered Strip Topology outranks artistic boundary play: seams may be irregular, but the four regions must stay sequential and topologically simple. In the default natural family, one-photo topology outranks artistic boundary play: regions may be composition-driven, but never arbitrary blobs, islands, fragments, or separate paper sheets. Never let a lower-priority rule modify a higher-priority protected region. Maintain four disjoint state-ownership regions (the exact masks the script writes) while allowing natural visible modules. After face, source, human, architectural, and four-state protections are satisfied, make the Robot Dreams-inspired color identity and the paper-material boundary outrank minor boundary smoothing and general artistic experimentation.

## Core principles

- Preserve primary-face identity and natural anatomy; never restore pixels merely for equality.
- Simplify people before breaking them.
- Only the primary head must remain in one state; bodies and buildings may intentionally span multiple abstraction states (cross-state coexistence, never accidental cloning).
- Remove architectural detail before identity.
- Reduce repeated components before weakening core semantic identity.
- Make 30%, 65%, and 90% differ in detail retention, component density, spatial fidelity, shape fidelity, and photographic surface retention.
- Make abstraction a structural transformation, not a filter.
- Treat the Robot Dreams-inspired warm, nostalgic, sunlit, slightly retro palette as the default visual identity of the Skill. Keep all four modules inside this ONE shared limited palette — regions differ by abstraction only, rebalancing the proportions of the shared colors, never by slice-to-slice dominant color roles.
- Keep ownership exact and disjoint — the four state-ownership regions tile the canvas, every pixel has one owner; make visible module edges natural, designed, and readable.
- ONE PHOTO, FOUR NATURAL REGIONS: each region differs only by its abstraction; the paper material layer is the representation of the boundary (a seam where the abstraction changes), never separate paper sheets.
- In the default natural family the regions share the same photograph — LEVEL ≠ MEDIUM: differentiate abstraction by information density and structural reduction, and the three abstract states MUST use three different Primary Abstraction Methods (never three intensities of the same method).
- The four states are four adjacent regions of ONE continuous image; the scene appears exactly once — never four full-image versions, grids, strips, or contact sheets.
- One-Scene / One-Object Ownership: every recognizable scene object has one continuous spatial existence on the final canvas — it may cross regions and change rendering language, but never restarts, repeats, or is redrawn as another copy inside another region.
- Deliver one coherent poster, never four independent images.
