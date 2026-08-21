# Composition, Slicing, and Reality Anchor

## Contents

* Canvas and equal logical zones
* Ordered Strip Topology
* Source ownership exclusivity
* Direction selection
* Reality Anchor
* Crowd Anchor fallback
* Architecture Anchor fallback
* Default Anchor fallback
* Abstraction assignment
* Spatial freedom and cohesion

## Canvas and equal logical zones

Preserve the source image's aspect ratio and use its dimensions as the compositional basis unless the user explicitly requests another format. Do not stretch, compress, or arbitrarily extend the canvas.

Ownership is defined directly by the four **state-ownership regions** — the
region masks produced by the boundary family. They tile the source-ratio
canvas exactly (every pixel has one owner). The "four hidden logical zones"
mentioned throughout this document are that ownership model: a conceptual
reference, NOT a separate geometric layer. "Four geometrically EQUAL hidden
logical zones" is literally true only in the `rect` family (the strips are
the quarters) and as the nominal band centers of the `contour` family. In the
default `natural` family (and `collage`/`torn`) the ownership regions are the
composition-driven masks themselves — they are NOT quarter-based. Never
re-shape an ownership region to protect content after it is created.

Translate the hidden ownership system into four visible modules governed by
the family-specific topology (see below). In the default natural family the
modules are four natural regions of ONE photograph (paper-material seam only
at the boundaries); in the optional collage family they are layered paper
pieces; in the legacy torn family they are four sequential regions with
irregular seam edges; in the optional contour family they may follow semantic
contours. In every family the visible modules must not duplicate or transfer
recognizable source content across logical owners, must tile the same
continuous canvas at source scale, share edges, and the scene must appear
exactly once. Never deliver a 2×2 grid, strip, or contact sheet of four
full-image versions.

## Ordered Strip Topology

Applies to the **legacy torn** family and the `vertical-strip` /
`horizontal-strip` collage layouts: the visible regions must preserve the
sequential four-region order of the hidden logical zones. Visible boundaries
may deviate locally, but every internal boundary must remain **one continuous
edge-to-edge seam**, and the global module topology must stay simple and
ordered.

For horizontal slicing:

```text
Zone 1 broadly remains above Zone 2.
Zone 2 broadly remains above Zone 3.
Zone 3 broadly remains above Zone 4.
```

For vertical slicing:

```text
Zone 1 broadly remains left of Zone 2.
Zone 2 broadly remains left of Zone 3.
Zone 3 broadly remains left of Zone 4.
```

Requirements:

```text
Visible boundaries may deviate locally, but every internal boundary must remain
one continuous edge-to-edge seam.

Do not convert the four zones into arbitrary blob-shaped territories.
```

Never:

- create isolated islands;
- create enclosed pockets;
- create contour loops;
- create U-shaped regions wrapping around subjects;
- create large peninsulas;
- create large wedges that destroy the ordered four-zone structure;
- snake a region around an entire person or building; or
- reverse a boundary's direction repeatedly.

Principle:

```text
Irregularity belongs to the seam geometry, not to the global module topology.
```

The script enforces this topology for `--boundary torn` and for the strip
collage layouts (`--mode verify` checks seam continuity, ordering, separation,
and the absence of islands/pockets), and `--boundary mask` may produce any
topology the supplied masks define.

## Natural Region Topology (default family)

The default `natural` family is NOT bound to quarter-based strips, but it is
still ONE photograph: four natural regions whose sizes are composition-driven
and whose boundaries are expressed by a paper-material seam. The topology
must be controlled and readable:

```text
ONE PHOTO
+ FOUR NATURAL REGIONS
+ EACH REGION DIFFERS ONLY BY ABSTRACTION
+ THE PAPER MATERIAL LAYER IS THE REPRESENTATION OF THE BOUNDARY

Allow composition-driven region sizes and smooth organic boundaries.

Avoid arbitrary blob segmentation, islands, pockets, random fragments,
contact sheets, 2x2 grids, and gutters.
```

`--mode verify` checks that each piece is substantial (>= ~6% of the canvas),
connected (no islands), and that the four pieces tile exactly.

## Source ownership exclusivity

Treat the four state-ownership regions (the region masks) as exclusive source-content ownership regions, not merely abstraction-assignment guides.

Every visible source-derived fragment must have one original spatial provenance in the source image and must remain owned by the logical zone containing that provenance.

Default invariant:

```text
one source region
→ one logical owner
→ one visible interpretation
```

Do not reproduce the same recognizable source region independently in multiple modules.

### One-Scene / One-Object Ownership

Every recognizable scene object has **one continuous spatial existence** on
the final canvas.

A mountain, building, road, vehicle, pole, tree, or person may cross multiple
abstraction regions, but it must **never** restart, repeat, reappear, or be
reconstructed as another copy inside another region.

```text
Cross-state coexistence MEANS:
one physical object crosses a boundary and changes rendering language.

Cross-state coexistence NEVER MEANS:
the same object is separately redrawn once inside each region.
```

A module may reinterpret, simplify, fragment, repaint, redraw, geometrize, or locally rearrange the source content it owns, but it must not import and re-render substantial recognizable source content owned by another logical zone.

### No cross-module cloning

Never create multiple visible copies of the same source-derived:

* person;
* face;
* body;
* building section;
* landmark feature;
* tree or vegetation cluster;
* vehicle;
* object;
* skyline segment;
* roofline segment;
* façade section;
* crowd cluster;
* road section; or
* other recognizable source region

across different modules merely to strengthen collage, fragmentation, rhythm, or abstraction diversity.

Do not use repetition as a shortcut for making modules visually distinct.

Non-semantic decorative repetition is allowed only when it does not create a second readable copy of a source object or scene-defining structure. Repeated micro-motifs, strokes, textures, marks, or tiny fragments may be used as local editorial devices.

### Continuous subjects are not duplicates

A person, building, crowd, road, skyline, tree canopy, or other large subject may naturally cross multiple hidden logical zones.

When this occurs, each module may render only the portion of that continuous subject that spatially belongs to its own logical zone.

For example:

```text
source building spans Zone 1 + Zone 2 + Zone 3

Zone 1 → render the Zone-1 portion
Zone 2 → render the Zone-2 portion
Zone 3 → render the Zone-3 portion
```

This is one continuous subject rendered through multiple abstraction states, not three copies of the building.

Alignment, silhouette continuity, perspective continuity, structural rhythm, or pose continuity are preferred but not required: a subject may also read as intentional fragments living at different abstraction levels simultaneously, which is often more impactful. Only the primary head must remain continuously recognizable in the Reality state.

Never restart the full subject inside each module.

### Visible-boundary freedom does not transfer ownership

Irregular visible module boundaries may expand or contract around contours for composition, but this does not transfer source ownership.

Visible-boundary flexibility may change which treatment visually occupies a small boundary area, but it must not cause an entire source object or recognizable source region to be duplicated into another module.

Use boundary overlap only as a narrow transition device, not as permission to repeat source content.

When a visible module crosses a hidden ownership boundary for contour-aware design, treat the crossing as a local rendering transition only. Do not use it to introduce a second copy of content whose source provenance belongs elsewhere.


## Direction selection

Choose vertical slices when the semantic composition, subjects, architecture, landscape, or visual flow develops primarily across the width. Choose horizontal slices when foreground, middle ground, background, sky, buildings, people, or ground create strong top-to-bottom layering.

Base the decision primarily on semantic composition, subject distribution, visual flow, and dominant structure. Treat portrait or landscape orientation only as a secondary clue; do not map orientation mechanically to slice direction.

## Reality Anchor

Use exactly one photographic Reality Anchor. Reality may be a central band, a
central street corridor, a mid-scene opening, or a broad middle paper layer —
it does not have to be a rectangular strip. It must remain clearly visible and
read as an intentional anchor.

### What the script actually auto-selects

`scripts/slice_and_compose.py --anchor auto` implements exactly this:

```text
1. primary face ownership  (largest face overlap inside the region masks)
2. side-weighted collage without a face -> the central Reality corridor
3. Logical Zone 2 fallback (a middle layer)
```

The script does NOT auto-detect crowds or architecture. The following sections
are **agent guidance for choosing an explicit `--anchor 1..4`** when the
scene's main subject is a crowd or an important building; they are not
promises of automatic behavior. Documentation matches implementation.

If a face crosses hidden logical boundaries, keep them fixed and use largest-area ownership. The visible Reality module may expand around the protected face or follow its contour while logical ownership remains unchanged. For multiple people, use only the primary visual subject to determine the single anchor.

Expansion of the visible Reality module around a protected face is a local treatment exception, not a transfer of source ownership. Do not duplicate the face, head, body, or surrounding scene into neighboring modules.

## Crowd Anchor fallback

When no reliable single primary face exists, check for a crowd-dominant semantic region before evaluating architecture or defaulting to Logical Zone 2.

Select a slice as the Reality Anchor when:

* no clear single primary-subject face exists;
* a group of people forms the image's main semantic focus;
* the group is visually concentrated mostly within one slice; and
* that slice carries the strongest crowd presence, human activity density, or event significance.

Determine crowd ownership by combining visible-people concentration, density of human activity, semantic importance of the group, and whether the crowd reads as one coherent event or focal cluster. Do not use raw person count alone when another slice contains the more important human event.

Keep all four hidden equal boundaries fixed. Do not move or resize logical zones to accommodate a crowd. If a crowd spans multiple zones, select the zone with the strongest combined concentration and semantic importance. Allow the visible Reality module to follow the crowd grouping when the overall module system remains balanced, but do not reproduce the entire crowd event in neighboring modules.

## Architecture Anchor fallback

When neither a reliable primary face nor a crowd-dominant semantic region determines the Anchor, check for an important architectural subject before using the default fallback.

Treat architecture as important when it is visually prominent, carries landmark identity, strongly supports scene recognition, functions as a major compositional mass, or acts as the main non-human subject. Select the building-dominant logical zone by evaluating:

* recognizable silhouette;
* primary massing;
* landmark features;
* perspective-defining structure; and
* semantic importance to the scene.

Require genuine subject importance, not mere presence or background area. Ordinary background buildings, generic streetscape façades, incidental urban fabric, distant structures, and buildings that only fill space must not automatically trigger architecture-anchor selection. Large visible area alone is insufficient when the architecture does not carry scene recognition, landmark identity, compositional dominance, or main-subject status.

Do not determine ownership from minor façade detail alone. If the building spans multiple logical zones, choose the zone containing the most identity-critical and semantically important share. Keep all hidden logical boundaries fixed.

When an important building becomes the Reality Anchor, keep its most identity-critical portion in the photographic Reality module whenever compositionally possible. Allow other portions of the same building to continue through neighboring abstract modules to create stronger reality-versus-abstraction contrast, especially along a bridge, roofline, tower, façade rhythm, or skyline.

This continuation must follow source provenance. Each neighboring module may reinterpret only the building portion that originally lies within its own logical zone. Do not regenerate the entire building in each module.

Across those modules, preserve silhouette, primary massing, perspective, landmark identity, and major structural rhythm. Allow abstract portions to simplify surface detail, windows, texture, decoration, and minor structures. Design visible module boundaries around the architecture when useful, but never move hidden ownership boundaries to contain the building.

## Default Anchor fallback

The script's `--anchor auto` falls back to Logical Zone 2 — second from the
left for vertical ownership or second from the top for horizontal ownership —
only when no primary face determines ownership (and no side-weighted corridor
applies).

For crowd-dominant or important-architecture scenes, the agent decides the
anchor and passes it explicitly:

```text
Primary face anchor (script auto)
→ side-weighted central corridor (script auto, no face)
→ agent-decided: crowd-dominant anchor / important-architecture anchor
→ Logical Zone 2 fallback (script auto)
```

When choosing an explicit anchor, use the guidance in the Crowd Anchor
fallback and Architecture Anchor fallback sections above.

For scenes without an important person, source-preserve the visible Reality module through an irregular source mask when useful. For important-person scenes, keep the coherent candidate final when the face already passes the Face Restoration Gate.

When restoration is genuinely needed, prefer `../scripts/restore_protected_anchor.py --mode face-mask --face-gate-failed --alignment-verified --mask MASK.png`. Supply `--aligned-source ALIGNED.png` when a registered source has been prepared. Use `--mode face-core --face-gate-failed --alignment-verified --face-box X0 Y0 X1 Y1` only as a last fallback. Use `--mode source-mask --mask-excludes-primary-face` only for a non-face irregular Reality module. Use full-anchor restoration only for scenes confirmed to have no primary face.

## Abstraction assignment

Assign exactly one 30%, one 65%, and one 90% abstraction treatment to the three non-anchor slices. Do not arrange the levels automatically as a gradient or make abstraction increase with distance from the anchor. Permutations such as `65 | Reality | 90 | 30` are valid. Choose by visual balance, semantic importance, subject placement, rhythm, palette, and contrast.

Default suggestion (not a hard rule): the strongest abstraction often works well at an **outer region** (top, bottom, or side), while Reality usually benefits from a central or compositionally important region.

Interpret percentage as departure from photographic representation—not opacity, modified pixel count, blur, saturation, or filter strength.

Abstraction assignment changes how a logical zone is represented; it does not change which source content that zone owns.

## Spatial freedom and cohesion

Inside each abstract module, permit deliberate changes to position, scale, overlap, depth, layer order, perspective emphasis, hierarchy, occlusion, merging, separation, and flattened depth **only for source content owned by that module**.

Spatial reconstruction must remain locally derived from the module's own source region.

Do not duplicate recognizable source fragments across modules.

Do not import a complete person, building, landmark, crowd cluster, skyline section, road section, or other recognizable source structure from another logical zone merely because it improves composition.

Local displacement is permitted, but displacement should normally remain within or near the source fragment's owning visible module. Do not displace a recognizable object so far that it reads as a second independent instance or appears to belong to another logical owner.

When a subject physically crosses multiple logical zones in the source, preserve it as one continuous cross-module subject. Each module should reinterpret its corresponding portion rather than independently regenerating the whole subject.

Exact pixel alignment with the source or neighboring modules is not required, but semantic provenance must remain clear. Cross-boundary reconstruction may alter rendering language while preserving the source order and continuity of major forms.

Make the four-state structure clearly perceptible through each visible module's dominant treatment and boundary design. In the optional **semantic contour** family, derive edges from human silhouettes, crowd groupings, building contours, rooflines, skylines, tree canopies, roads or rails, shadow masses, large color fields, or painterly and sketch strokes. In the **default torn** family, do NOT derive seams from semantic contours: seams are layout-defined multi-scale torn-paper cuts that may cross any ordinary subject, and the only hard avoidance is the protected primary head.

Preserve face identity and avoid accidental human or architectural mismatch, repeated source regions, cloned objects, restarted structures, or duplicated scene-defining forms. Follow [intentional-modular-composition.md](intentional-modular-composition.md).
