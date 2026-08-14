---
name: four-slice-reality-poster
description: "Transform a user-supplied photograph into one coherent mixed-media poster made of exactly four equal slices: one source-preserved, non-generative photographic Reality Anchor and three source-derived slices at approximately 30%, 65%, and 90% structural abstraction. Use for four-panel reality-versus-virtual posters, progressive abstraction artworks, editorial photo/illustration hybrids, or requests to preserve the original subject identity while reinterpreting the other three regions. Protect primary-face source pixels through masking and deterministic compositing whenever available; do not use for unrelated four-image collages or simple filter variations."
---

# Four-Slice Reality / Abstraction Poster

Create one continuous editorial poster in which one equal slice remains photographic and three equal slices reinterpret the same source world at distinct, non-linear abstraction levels.

## Required reading

Before producing the artwork, read:

- [composition-and-anchor.md](references/composition-and-anchor.md) for slicing, anchor selection, level assignment, and continuity.
- [abstraction-language.md](references/abstraction-language.md) for the approved method library and level calibration.
- [cinematic-color-system.md](references/cinematic-color-system.md) for the default warm, nostalgic, Robot Dreams-inspired shared palette and level-specific color compression.
- [seamless-transitions.md](references/seamless-transitions.md) for soft, content-aware transitions across the three exact logical boundaries.
- [subjects-validation.md](references/subjects-validation.md) for people, architecture, hard constraints, and final validation.

## Face Identity Lock & Protected Source Region

Treat the Reality Anchor as a protected source region, never as content to regenerate. **The primary face is not content that should be faithfully regenerated. It is source content that should not be regenerated at all whenever source-preserving compositing is available.**

Use this execution model:

1. Determine the four exact logical slices and Reality Anchor before generation.
2. Exclude the entire Reality Anchor from generative editing through a hard protection mask when the tool supports masks.
3. Generate or reconstruct only the other three slices. Never ask the model to recreate a photographic-looking Anchor.
4. Composite the original Anchor pixels back after generation. Use `scripts/restore_protected_anchor.py` when local source and generated files are available.
5. Verify pixel equality between the source and final Anchor. If verification fails, restore it again and do not deliver.

If the Anchor contains the primary face, treat that face as the highest-priority non-generative region. Never redraw or infer the eyes, nose, mouth, eyebrows, face shape, jawline, facial proportions, feature placement, texture structure, or identity characteristics. Prefer an unchanged face and a more visible seam over any generative blending.

Default to exact source pixels for the full Anchor. Apply optional non-structural photographic grading only through a deterministic image-processing operation, never through image generation. If exact identity equality is required or a face-safe mask is unavailable, leave the Anchor—including its face—completely ungraded.

Required invariant:

```text
final primary face = original source face
final Reality Anchor = preserved source image + optional non-structural deterministic grading
```

Never accept:

```text
final primary face = AI reconstruction of original face
final Reality Anchor = regenerated photographic-looking image
```

## Workflow

1. Inspect the supplied photograph. Identify dimensions, orientation, semantic flow, primary people and faces, architecture, landmarks, important objects, dominant shapes, and palette.
2. Choose one semantic slicing direction: four equal vertical slices or four equal horizontal slices. Preserve the source aspect ratio and overall rectangular canvas. Never move boundaries afterward.
3. Select exactly one Reality Anchor. If a reliable primary face exists, use the slice containing the largest visible portion of that face. Otherwise use Slice 2.
4. Extract and protect the source Reality Anchor before any generative edit. If it contains the primary face, lock that face as the highest-priority non-generative source region.
5. Assign 30%, 65%, and 90% abstraction exactly once to the remaining slices. Choose a non-mechanical permutation based on balance, meaning, rhythm, and color—not distance from the anchor.
6. Establish one warm, nostalgic, emotionally gentle cinematic palette. Apply it generatively only to the three abstract slices; apply any Anchor grading deterministically and non-structurally, or leave the Anchor unchanged.
7. Select source-derived abstraction methods appropriate to each abstract slice. Treat abstraction as structural reinterpretation, never filter intensity.
8. Generate or reconstruct only the three abstract slices. Permit repositioning, rescaling, overlap, flattened depth, and changed layer order there while retaining source visual DNA. Compress local color variation more strongly as abstraction increases.
9. Treat boundaries as soft and content-aware on the generated side. Do not allow transition effects, palette harmonization, or mixed-media strokes to enter a protected face or overwrite protected Anchor pixels.
10. Deterministically composite the source Anchor back into the poster and verify it against the source. Accept a visible boundary when protection conflicts with seamlessness.
11. Art-direct the poster using shared palette, directional rhythm, repeated accents, lines, shape echoes, and visual weight without redrawing the Anchor.
12. Inspect source preservation, face identity, palette unity, and all three transitions, then validate every required condition in [subjects-validation.md](references/subjects-validation.md) before delivery.

## Decision priority

Resolve conflicts in this order:

1. Primary Face Identity Lock.
2. Reality Anchor Source Preservation.
3. Human Body Continuity.
4. Architectural Identity.
5. Abstraction Level Assignment.
6. Boundary Transition.
7. Global Color Styling.
8. Artistic Experimentation.

Never let a lower-priority rule modify a higher-priority protected region. Maintain four equal logical slices while applying this protection hierarchy.

## Core principles

- Preserve one source fragment exactly; generate only the other three.
- Simplify people before breaking them.
- Remove architectural detail before identity.
- Make abstraction a structural transformation, not a filter.
- Use one warm, nostalgic cinematic color world across all four states.
- Keep boundaries mathematically exact but visually soft.
- Deliver one coherent poster, never four independent images.
