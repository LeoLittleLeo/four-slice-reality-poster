---
name: four-slice-reality-poster
description: "Transform a user-supplied photograph into ONE designed editorial Layered Torn-Paper Collage poster: four composition-driven layered paper pieces (Reality + 30%, 65%, 90% source-derived abstraction states) sharing one editorial print/paper material language, with torn-paper geometry as region shape rather than a decorative line. The scene appears exactly once; only the primary head is hard-protected. Legacy Torn-Strip, optional Semantic Contour, Mask, and Rect boundary families are also available. Accept a visually coherent generated face when identity and anatomy are already sound; use source-face restoration only as a gated fallback that demonstrably improves the result."
---

# Four-Slice Reality / Abstraction Poster

Create one editorial poster composed of four layered paper pieces (Reality + 30%, 65%, 90% source-derived abstraction states) sharing a single editorial print / paper material language. By default this is a **Layered Torn-Paper Collage** — torn-paper geometry is the region shape itself, not a line drawn on top.

## Default visual objective

**Readable four-state editorial collage first; Layered Torn-Paper Collage by default.**

The final image should feel designed as **one physical editorial object**, not assembled from four unrelated rendering styles. Reality, 30%, 65% and 90% belong to the same visual system: shared editorial print / aged paper / torn paper / screen-print texture / paper grain / restrained distressed texture, inside the Robot Dreams-inspired warm cinematic palette.

Core principle:

```text
IRREGULAR EDGE SHOULD CREATE COLLAGE SHAPE,
NOT JUST WAVY STRIPS.

Keep the four-state composition controlled and readable.
Avoid arbitrary blob segmentation, islands, pockets, and random fragments.

However, do not force the visible regions to remain near-equal strips.
Allow broad layered paper shapes whose geometry is driven by composition,
depth, visual rhythm, and major scene masses.
```

Prefer:

```text
ONE COHERENT EDITORIAL POSTER
+
FOUR READABLE ABSTRACTION STATES
+
ONE SHARED MATERIAL LANGUAGE
+
COMPOSITION-DRIVEN LAYERED REGIONS
```

over:

```text
four independent filter/medium patches.
```

The four states must be immediately legible while keeping the poster system coherent. Do not require visible rectangular bands. Keep the four paper pieces roughly substantial; do not reduce them to one dominant image plus three scraps.

Default to **Hybrid Transition**: allow backgrounds and large color fields to change abruptly, preserve semantic continuity for important people and buildings, and never force every boundary to be fully seamless. Keep all four states clearly readable; make boundaries visibly present whenever that strengthens modularity or poster design.

## Final Output Layout — Hard Constraint

The deliverable is **one continuous image at the source aspect ratio**. The four states (Reality, 30%, 65%, 90%) are four **adjacent regions** of that one canvas: they tile the entire canvas, share edges with each other, and each region shows a different **slice** of the original photograph. The scene appears **exactly once**. Never deliver a 2×2 grid, a contact sheet, a strip of four full-image versions, four panels each containing the full scene, gutters, or panel gaps.

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

### Modular Color Principle

Keep the four visible modules inside the **same cinematic emotional universe**, but do not force them into nearly identical grading. Give each module a clearly different dominant color role when useful. For example:

```text
Slice A → terracotta / warm brown / sand
Slice B → cream / dusty peach / warm beige
Slice C → dusty blue / muted teal
Slice D → ochre / muted yellow / soft brick
```

Treat these as examples, not fixed assignments. Do not derive a fixed hue from abstraction level. Use color differences to strengthen four-module readability.

### Chromatic Separation

Allow deliberate color contrast to create a visible boundary. Prefer dominant hue change, warm/cool contrast, value contrast, large color-field change, or different accent emphasis over artificial divider lines. Accept a clear chromatic boundary when both sides remain inside the broader Robot Dreams-inspired palette family. Do not automatically smooth away intentional color differences.

### Color Character

Default toward medium-low to medium saturation, soft but alive color, gentle sunlight, open highlights, calm shadows, slightly faded cinematic color, warm/cool balance, and a small repeated accent set.

Avoid neon cyberpunk, purple-magenta sci-fi glow, random rainbow abstraction, aggressive HDR, crushed blacks, glossy commercial-advertising color, cold steel monochrome, lifeless gray, and excessive candy saturation unless the user explicitly requests them.

### Core Color Rule

```text
ONE ROBOT DREAMS-INSPIRED COLOR UNIVERSE
+
FOUR DISTINCT DOMINANT COLOR ROLES
=
ONE COHERENT BUT CLEARLY MODULAR POSTER
```

Do not achieve coherence by making all four slices color-identical. Follow [cinematic-color-system.md](references/cinematic-color-system.md) for detailed implementation.

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

### Face Restoration Gate

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
   `python scripts/slice_and_compose.py --mode prepare --source <photo> --boundary <collage|torn|contour|mask|rect> [--layout <auto|horizontal-layered|side-weighted|vertical-strip|horizontal-strip>] [--direction <auto|vertical|horizontal>] [--face-boxes "<x0,y0,x1,y1;...>"] --levels <permutation> --workdir work/ [--masks-dir <dir>]`.
   Boundary family: `collage` (default) builds **Layered Torn-Paper Collage** — four composition-driven layered paper pieces with independent torn silhouettes, z-ordered, one shared material language; the torn edge is region geometry, not a drawn line. `torn` (legacy) keeps ordered torn-strip composition. `contour` (optional) derives semantic + edge-aware contours. `mask` accepts four supplied masks normalized to exact tiling; `rect` falls back to equal strips. The script writes the four exact pixel regions (masks), the manifest, per-zone context crops, and the zone masks. Follow [deterministic-layout.md](references/deterministic-layout.md).
4. Select exactly one Reality Anchor. The script's `--anchor auto` implements: 1) primary-face ownership (largest face overlap inside the piece masks); 2) for `side-weighted` collage without a face, the central Reality corridor; 3) Logical Zone 2 fallback. Architecture/crowd anchors are NOT auto-detected by the script — choose them explicitly with `--anchor 1..4` when the scene's main subject is a building or crowd. Keep the hidden ownership boundaries fixed.
5. Identify the primary face and surrounding head/body continuity context before generation; do not pre-commit to source-pixel restoration. Pass accurate `--face-boxes` (or a `--head-mask`) so the script derives a generous head protection region covering hair and jaw/neck — the head is force-composited from the source regardless of which zone it falls in.
6. Assign 30%, 65%, and 90% abstraction exactly once to the remaining paper pieces via `--levels`. Choose a non-mechanical permutation based on balance, meaning, rhythm, and color—not distance from the anchor. As a default suggestion (not a hard rule), the strongest abstraction often works well at an outer paper layer (top, bottom, or side), while Reality benefits from a central or compositionally important region.
7. Establish the Robot Dreams-inspired default color identity before generating the abstract modules. Treat this palette direction as a core visual constraint, not optional finishing. Give the three abstract modules distinct but related dominant color roles while keeping them inside the same warm, nostalgic, sunlit, slightly retro cinematic universe. Apply any Reality Anchor grading only deterministically and non-structurally, or leave the Anchor unchanged.
8. Render each abstract zone **separately** (primary path). Select source-derived abstraction methods appropriate to each zone's level — in collage mode, share one editorial print / paper material language across the states and differentiate primarily by structural information density, component omission, shape merging, edge simplification, surface-detail reduction, spatial compression, and graphic massing; do NOT force three unrelated mediums just to prove the regions differ. Treat abstraction as structural reinterpretation, never filter intensity. Reduce, merge, group, or omit non-essential repeated components when this improves clarity, but preserve the primary person, identity-critical face, dominant crowd event, landmark architecture, and major scene-defining masses. Render each non-anchor context crop (`work/crops/zone{i}.png`) with the per-zone render prompt block from [deterministic-layout.md](references/deterministic-layout.md) (use the collage block when `--boundary collage`); the model never decides the poster layout and never receives a whole-poster slicing instruction. **Each zone render must show ONLY its own slice of the photograph, at the same aspect ratio and orientation as its crop — the model must never complete, reconstruct, or re-invent the rest of the scene inside a zone render.** Compose refuses to build the poster when a zone render has the wrong aspect (e.g. a landscape full scene for a portrait strip) or is a near-copy of the full scene; if either happens, reject it and re-render with the strict slice prompt block.
9. Compose deterministically: `python scripts/slice_and_compose.py --mode compose --workdir work/ --output <final>.png`. The script pastes the rendered zones back at fixed coordinates through their zone masks, always keeps the Reality Anchor composited from the source, and force-composites the head protection mask from the source on top — the primary face is the original photograph even when a face box straddles a zone boundary. For `collage` a subtle paper grain is blended over the pieces (Reality re-composited clean), each piece gets a deckled fiber edge along its torn silhouette, and one-sided paper shadows fall only from higher-z pieces onto lower ones (`--paper-*`, `--collage-overlap`). For `torn` the cuts are hard (`feather = 1`) with the torn-paper seam overlay (`--seam-style paper`); `contour`/`mask`/`rect` use a soft transition band. For Scheme B, inpaint the full canvas with `work/masks/zone{i}.png` and run `--mode enforce-anchor` instead. The four visible modules are the collage paper pieces (default), torn ordered regions, contour regions, supplied masks, or rect strips; they tile the canvas exactly with no gaps or overlaps. Keep them substantial and readable, and preserve the Skill's modular color and palette rules.
10. One-shot full-poster generation is a fallback only: if used, the model prompt MUST contain the Final Output Layout hard-constraint block verbatim, MUST keep the source aspect ratio and orientation (portrait stays portrait), and the result must pass `--mode verify`. Reject any grid, strip, contact sheet, or repeated-scene output.
11. Run the Face Restoration Gate on the final poster. If Candidate A is acceptable, skip restoration and retain A for the remaining poster-level workflow. Otherwise attempt a geometrically verified irregular-mask or aligned restoration to create Candidate B.
12. Let Candidate B replace Candidate A only when identity improves without unnatural anatomy, patch appearance, skin mismatch, or broken head/jaw/neck/body continuity.
13. Art-direct the poster using shared motifs, rhythm, limited palette relationships, or structural echoes without weakening face identity or human continuity.
14. Run `python scripts/slice_and_compose.py --mode verify --workdir work/ --output <final>.png`, then inspect face identity, head/body continuity, four-state readability, intentional boundary design, and poster-level coherence, and validate every required condition in [subjects-validation.md](references/subjects-validation.md) before delivery. Reject any output that repeats the scene (2×2 grid, strip, contact sheet) regardless of other qualities.

## Decision priority

Resolve conflicts in this order:

1. Primary Face Identity and Natural Facial Coherence.
2. Primary Head Identity and Continuity. (Body and building continuity are soft preferences; cross-state presence is allowed and encouraged.)
3. Reality Anchor Role and Local Source Preservation.
4. Architectural Identity.
5. Four-State Readability, Logical-Zone Ownership, Abstraction Assignment, and Composition Topology. In the default collage family: layered paper pieces, composition-driven sizes, no arbitrary blobs/islands/pockets; in the legacy torn family: ordered sequential regions.
6. Robot Dreams-Inspired Color Identity (combined with the shared editorial print/paper material language in collage mode).
7. Intentional Modular Boundary Design.
8. Artistic Experimentation.

The Final Output Layout hard constraint (one continuous image, four adjacent regions, scene appears exactly once) outranks every rule in this list: reject any grid, strip, or contact-sheet output no matter how well it satisfies lower-priority goals. In the legacy torn family, Ordered Strip Topology outranks artistic boundary play: seams may be irregular, but the four regions must stay sequential and topologically simple. In the default collage family, layered paper-piece topology outranks artistic boundary play: pieces may be large and layered, but never arbitrary blobs, islands, or fragments. Never let a lower-priority rule modify a higher-priority protected region. Maintain four equal hidden logical zones while allowing irregular visible modules. After face, source, human, architectural, and four-state protections are satisfied, make the Robot Dreams-inspired color identity and the shared paper material language outrank minor boundary smoothing and general artistic experimentation.

## Core principles

- Preserve primary-face identity and natural anatomy; never restore pixels merely for equality.
- Simplify people before breaking them.
- Only the primary head must remain in one state; bodies and buildings may intentionally span multiple abstraction states (cross-state coexistence, never accidental cloning).
- Remove architectural detail before identity.
- Reduce repeated components before weakening core semantic identity.
- Make 30%, 65%, and 90% differ in detail retention, component density, spatial fidelity, shape fidelity, and photographic surface retention.
- Make abstraction a structural transformation, not a filter.
- Treat the Robot Dreams-inspired warm, nostalgic, sunlit, slightly retro palette as the default visual identity of the Skill. Keep all four modules inside this shared emotional color universe while allowing strong, intentional slice-to-slice dominant color differences.
- Keep hidden logical ownership mathematically equal; make visible module edges irregular, designed, and readable.
- IRREGULAR EDGE SHOULD CREATE COLLAGE SHAPE, NOT JUST WAVY STRIPS: keep the four-state composition controlled and readable; avoid arbitrary blobs, islands, pockets and random fragments; but do not force the visible regions to remain near-equal strips — allow broad layered paper shapes driven by composition, depth, rhythm and scene masses.
- In the default collage family the four states share ONE editorial print / paper material language — LEVEL ≠ MEDIUM: differentiate abstraction by information density and structural reduction, not by forcing three unrelated mediums.
- Torn-paper geometry in collage is region shape (layered paper pieces with deckled edges and one-sided shadows), not a decorative line drawn on top.
- The four states are four adjacent regions of ONE continuous image; the scene appears exactly once — never four full-image versions, grids, strips, or contact sheets.
- Deliver one coherent poster, never four independent images.
