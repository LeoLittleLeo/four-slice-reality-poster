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

Prioritize a readable four-state modular poster over seamless cinematic blending. Make Reality, 30%, 65%, and 90% visually distinguishable at first inspection. Use equal hidden logical zones for ownership, but prefer four designed irregular visible fragments over rigid rectangular bands.

Use this hierarchy:

```text
four-state readability
→ intentional module contrast
→ poster-level coherence
→ optional local blending
```

## Boundary families

Boundary language is split into two families. **Torn-Strip is the DEFAULT**;
**Semantic Contour is optional** and must be chosen explicitly.

The governing principle for the default family:

```text
IRREGULAR EDGE ≠ IRREGULAR TERRITORY

Make the seams irregular.
Keep the four regions topologically simple and sequential.

Torn boundaries are layout-defined seams, not semantic segmentation contours.
```

### A. Torn-Strip Boundary — DEFAULT

- three continuous edge-to-edge seams;
- approximately follows the logical slice direction;
- irregular but not strongly meandering;
- independent from most semantic object contours;
- may cut across buildings, roads, vegetation, sky, mountains, crowds and
  bodies;
- must avoid the protected primary head;
- retains ordered strip topology;
- uses hard or near-hard cuts (script `feather = 1`);
- may expose a narrow warm paper-fiber seam (`--seam-style paper`);
- must not use broad feathering.

Keep hidden logical boundaries exact. The three internal seams start near the
nominal 1/4, 1/2 and 3/4 boundaries, run edge-to-edge, and stay inside a
narrow deviation band (`--torn-band`, ~6%). Irregularity belongs to the seam
geometry, not to the global module topology.

### B. Semantic Contour Boundary — OPTIONAL

The optional family (`--boundary contour`) derives boundaries from semantic
structure:

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

Valid boundary sources and treatments common to both families include:

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

- Are four roughly balanced sequential regions immediately readable?
- Is the output one continuous image tiled by four adjacent regions, or four full-image versions in a grid/strip/contact sheet? Reject any layout where the scene is repeated.
- Do the four states still read as four broad sequential regions?
- Do the three seams read as intentional torn-paper cuts?
- Are the seams irregular without turning the regions into arbitrary blobs?
- Do the seams remain approximately aligned with the chosen slicing direction?
- Are there any islands, loops, U-shaped wraps or excessive excursions?
- Does the primary head remain untouched?
- Does the seam feel like a physical editorial collage cut rather than semantic segmentation?
- Can Reality, 30%, 65%, and 90% be distinguished without explanation?
- Do 30%, 65%, and 90% differ in structural information density across detail, component density, spatial fidelity, shape fidelity, and photographic surface retention?
- Do visible boundaries use meaningful contours, structures, fields, or strokes rather than default rectangular rigidity?
- Do at least two visual signals differentiate neighboring modules?
- Does the Reality Anchor remain the clearly photographic reality state without requiring unsafe full-block restoration?
- Does the primary face preserve recognizable identity and natural anatomy without a patch edge?
- If restoration was attempted, is it visibly better than the pre-restoration candidate?
- Are the head contour, hair silhouette, and face-to-neck connection coherent? (Body and building continuity across states may be soft or intentionally broken.)
- If important architecture owns the Anchor, does it preserve silhouette, massing, perspective, landmark identity, and structural rhythm while using cross-module state contrast effectively?
- Does any unifying treatment flatten the four states into one painting?
- Are color differences purposeful and poster-level relationships sufficient?

Reject the result if the four states merge into an almost continuous illustration, if 30%, 65%, and 90% are perceptually interchangeable or differ only by color or medium, if seamlessness hides the modular structure, or if any restoration creates facial patches, geometry mismatch, or human stitching errors. In the default torn family, also reject if the torn boundary repeatedly follows object contours, wraps around an entire person or building, creates blob-shaped territories, or destroys the ordered four-region structure. Accept visible boundaries and color breaks when they are clean, controlled, and compositionally intentional.
