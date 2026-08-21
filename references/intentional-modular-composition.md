# Intentional Modular Slice Composition

## Contents

- Default hierarchy
- Boundary language
- Hybrid Transition
- Module differentiation
- Subject continuity
- Optional transitions
- Validation

## Default hierarchy

Prioritize a readable four-state modular poster over seamless cinematic blending. Make Reality, 30%, 65%, and 90% visually distinguishable at first inspection. Use the four state-ownership regions (the region masks) for ownership, but prefer natural, designed region shapes over rigid rectangular bands.

Use this hierarchy:

```text
four-state readability
→ intentional module contrast
→ poster-level coherence
→ optional local blending
```

## Boundary families

Boundary language is split into families. **Natural Regions is the DEFAULT**;
Layered Torn-Paper Collage and Semantic Contour are optional; Torn-Strip is
legacy.

The governing principle for the default family:

```text
ONE PHOTO
+ FOUR NATURAL REGIONS
+ EACH REGION DIFFERS ONLY BY ABSTRACTION
+ THE PAPER MATERIAL LAYER IS THE REPRESENTATION OF THE BOUNDARY
```

Keep the four-state composition controlled and readable. Avoid arbitrary
blob segmentation, islands, pockets, and random fragments. Do not force the
visible regions to remain near-equal strips — allow composition-driven
natural region shapes.

### A. Natural Regions — DEFAULT (`--boundary natural`)

**ONE photograph** jointly composed of four natural regions; each region is
just the photo re-rendered at its abstraction level:

- the paper material layer is drawn ONLY at the region boundaries as
  torn-paper seams (the boundary is the paper material's representation);
- no z-order, no sheet bodies, no sheet grain — the regions are parts of one
  photo, NOT four paper sheets;
- composition-driven layouts (`horizontal-layered` / `side-weighted` /
  strips) with smooth organic boundary paths;
- soft feather transitions by default; uniform warm grade shared by all four
  states (Reality/head composited from the graded source);
- the three abstract states MUST use three different Primary Abstraction
  Methods (LEVEL ≠ MEDIUM), all inside the same photograph;
- no blob segmentation, islands, pockets, contact sheets, 2×2 grids or
  gutters;
- the scene appears exactly once.

### B. Layered Torn-Paper Collage — OPTIONAL (`--boundary collage`)

The optional paper-sheet family: four layered paper pieces in z-order, each
with its own torn silhouette and composition-driven size, sharing ONE
editorial print / paper material language:

- TORN EDGE IS REGION GEOMETRY, NOT A DECORATIVE LINE DRAWN ON TOP;
- layered stacking, local side insets, larger paper pieces, irregular torn
  silhouettes, paper overlap and visual depth;
- each piece casts a one-sided paper shadow only onto the pieces below it in
  z-order;
- paper grain, deckled fiber edges and warm ivory are shared across all four
  states;
- Reality is photographic (source-composited clean); 30/65/90 differ by
  structural information density AND distinct Primary Abstraction Methods;
- no blob segmentation, islands, pockets, contact sheets, 2×2 grids or
  gutters;
- the scene appears exactly once.

### C. Torn-Strip — LEGACY (`--boundary torn`)

Kept intact: four sequential strip-like states with three continuous
irregular seams around 1/4, 1/2, 3/4; irregular but ordered; head-avoiding;
hard cuts with the optional torn-paper seam overlay.

### D. Semantic Contour Boundary — OPTIONAL (`--boundary contour`)

The optional family derives boundaries from semantic structure:

- silhouette;
- person contour;
- architecture edge;
- roofline;
- skyline;
- road;
- horizon;
- large color field.

Semantic Contour is optional and is NOT the default boundary family. Choose
it explicitly when a composition genuinely benefits from contour-following
regions (see [deterministic-layout.md](deterministic-layout.md) for the
algorithm).

Valid boundary sources and treatments available across the families include:

- a collage cut, brush edge, sketch stroke, or shape-defined mask;
- a clean straight crop edge when it is genuinely the strongest design;
- an abrupt but controlled medium change;
- a deliberate tonal or chromatic break;
- a narrow rule, gutter, or editorial separator when compositionally useful;
- a sharp transition from photograph to line, paint, color block, collage, or geometry;
- a limited contour or motif crossing that connects modules without hiding the division.

Do not soften a boundary merely because it is visible. Refine it only when it
resembles an error: white halos, ragged masking, double edges, offset copies,
mismatched anatomy, accidental gaps, muddy feathering, or uncontrolled
generation residue.

## Hybrid Transition

Use Hybrid Transition as the default boundary strategy:

- Allow backgrounds, skies, ground planes, low-information areas, and large color fields to change abruptly across a boundary.
- Preserve semantic continuity for important people through recognizable pose, silhouette, gesture, and head/body relationship.
- Preserve semantic continuity for important buildings through silhouette, roofline, perspective, primary massing, and landmark structure.
- Permit visible medium, color, value, texture, or abstraction changes across the same continuous subject.
- Keep transitions local and selective; do not force every boundary or every object to blend.

Semantic continuity does not require visual seamlessness. A person or building may remain readable while its rendering language changes sharply at the exact module boundary.

## Module differentiation

Give each visible module a stable visual core and make its assigned state readable across most of its area:

- Reality must remain unmistakably photographic, source-faithful, and identity-preserving; source-pixel equality is not mandatory.
- 30% must remain source-recognizable with visible artistic intervention.
- 65% must show substantial reconstruction and reduced photographic fidelity.
- 90% must be predominantly abstract while retaining source DNA.

Differentiate adjacent modules with at least two deliberate signals such as rendering medium, information density, edge language, palette emphasis, value structure, texture, geometry, or spatial reconstruction. Do not rely only on subtle filter strength.

For the 30%, 65%, and 90% modules, at least one differentiating signal between every pair must be structural information density: detail retention, component count, spatial fidelity, shape fidelity, or photographic surface retention. Palette, brush texture, and medium changes may reinforce the difference but cannot create it alone.

Keep all four modules roughly balanced in area and visual importance. Do not create one dominant main image with three tiny fragments, random collage scraps, or an unstructured montage. The Reality module may expand or contract around a protected subject, but rebalance the other modules so all four states remain substantial.

Allow obvious color differences between slices. Keep them related through a small number of shared hues, accents, or emotional temperature cues rather than identical global grading.

## Subject continuity

Preserve primary-face identity. Do not restore source pixels when the coherent candidate already has natural anatomy and recognizable identity. If restoration is needed, use an irregular semantic mask or verified aligned source face and reject any result that damages head, hair, jaw, neck, shoulder, clothing, or body continuity.

When a body or important building crosses abstract modules, continuous semantic form with a sharp rendering change is a good default, but an intentional editorial break is equally valid: body parts and buildings may exist across multiple abstraction states at once — only the primary head must remain continuously recognizable. Choose between:

- **continuous semantic form:** keep pose, silhouette, roofline, perspective, or massing aligned while changing medium at the boundary; or
- **intentional editorial break:** interrupt or shift the form in a controlled way that reads as designed abstraction.

Never create accidental duplicated limbs, double faces, ghost edges, cutout halos, or unrelated offset structures.

One-Scene / One-Object Ownership: every recognizable scene object has one
continuous spatial existence on the final canvas. It may cross regions and
change rendering language at the boundary — it never restarts, repeats, or is
redrawn as another copy inside another region. This is the semantic reading of
"the scene appears exactly once".

When important architecture owns the Reality Anchor, do not force the entire building into one photographic module. Keep the identity-critical portion photographic and, when compositionally useful, continue its bridge, roofline, tower, façade rhythm, skyline, massing, or perspective through neighboring abstract modules. Use the cross-state rendering change as deliberate contrast while preserving architectural identity and structural continuity.

## Optional transitions

Use transition effects only as secondary local devices. Limit them to small, content-aware areas when they improve composition without weakening module readability. Suitable devices include one continued contour, a repeated color accent, a short brush or line intrusion, or a shared horizon cue.

Feathering is per boundary family: `contour`/`mask`/`rect` use a modest soft
transition band (script `--feather`, ~2% of the smaller dimension), while
`torn` uses hard near-1px cuts plus the physical paper-seam overlay — its look
is a hard tear, not a soft blend. Broad 3%–8% feathered zones that blur states
together are still rejected in every family. Do not migrate texture
continuously across all boundaries. Do not turn the full canvas into a single
abstraction gradient or one common painterly surface.

## Validation

Inspect the poster at thumbnail size and ask:

- Are four readable states present inside ONE designed editorial collage?
- Is the output one continuous image tiled by four adjacent regions, or four full-image versions in a grid/strip/contact sheet? Reject any layout where the scene is repeated.
- Does it feel like one physical editorial object (shared paper/print material language) rather than four unrelated medium filters?
- Do the four states read as natural regions of ONE photograph, with torn-paper seams at the boundaries, not four wavy strips with lines between them?
- Are the pieces substantial and connected (no tiny scraps, islands, pockets or scattered fragments)?
- Does the seam/edge feel like torn paper (deckled fibers, uneven width) rather than a uniform white/cream stroke?
- In the default natural family: are the regions four parts of ONE photograph, with torn-paper seams only at the boundaries (not four separate paper sheets)?
- In the legacy torn family: do the four states still read as four broad sequential regions with three intentional torn-paper cuts?
- Do the seams/pieces remain approximately aligned with the intended slicing direction?
- Are there any islands, loops, U-shaped wraps or excessive excursions?
- Does the primary head remain untouched?
- Can Reality, 30%, 65%, and 90% be distinguished without explanation?
- Do 30%, 65%, and 90% differ in structural information density across detail, component density, spatial fidelity, shape fidelity, and photographic surface retention?
- In the default natural family: do the three abstract states use three DIFFERENT Primary Abstraction Methods (LEVEL ≠ MEDIUM) inside the same photograph?
- Do visible boundaries use meaningful contours, structures, fields, or strokes rather than default rectangular rigidity?
- Do at least two visual signals differentiate neighboring modules?
- Does the Reality Anchor remain the clearly photographic reality state without requiring unsafe full-block restoration?
- Does the primary face preserve recognizable identity and natural anatomy without a patch edge?
- If restoration was attempted, is it visibly better than the pre-restoration candidate?
- Are the head contour, hair silhouette, and face-to-neck connection coherent? (Body and building continuity across states may be soft or intentionally broken.)
- If important architecture owns the Anchor, does it preserve silhouette, massing, perspective, landmark identity, and structural rhythm while using cross-module state contrast effectively?
- Does any unifying treatment flatten the four states into one painting?
- Are color differences purposeful and poster-level relationships sufficient?

Reject the result if the four states merge into an almost continuous illustration, if 30%, 65%, and 90% are perceptually interchangeable or differ only by color or medium, if seamlessness hides the modular structure, or if any restoration creates facial patches, geometry mismatch, or human stitching errors. In the default natural family, also reject if the poster reads as four separate paper sheets, as four wavy strips with decorative lines, as arbitrary blob segmentation, or if the paper material is painted over whole regions instead of representing only the boundary. Accept visible boundaries and color breaks when they are clean, controlled, and compositionally intentional.
