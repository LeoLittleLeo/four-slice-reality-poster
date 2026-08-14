---
name: four-slice-reality-poster
description: "Transform a user-supplied photograph into one readable four-state modular mixed-media poster made of exactly four equal slices: one source-preserved, non-generative photographic Reality Anchor and three visibly distinct source-derived slices at approximately 30%, 65%, and 90% structural abstraction. Use for modular reality-versus-virtual posters, progressive abstraction artworks, editorial photo/illustration hybrids, or requests to preserve the original subject identity while juxtaposing four visual states. Prioritize clear slice identity over seamless blending and protect primary-face source pixels through deterministic compositing whenever available; do not use for unrelated four-image collages or simple filter variations."
---

# Four-Slice Reality / Abstraction Poster

Create one editorial poster that visibly juxtaposes four equal modules: one photographic source region and three clearly distinct, non-linear abstraction states.

## Default visual objective

**Readable four-state modular poster first, seamless cinematic blending second.**

Make the four equal slices immediately legible as intentional modules while keeping them inside one poster system. Allow clear boundaries, decisive rendering changes, and noticeable color differences. Do not dissolve the entire image into one uniformly painted scene. A boundary may be straight, sharp, tonal, chromatic, textural, or medium-based; it must look art-directed rather than accidental.

Default to **Hybrid Transition**: allow backgrounds and large color fields to change abruptly, preserve semantic continuity for important people and buildings, and never force every boundary to be fully seamless. Keep all four states clearly readable; make boundaries visibly present whenever that strengthens modularity or poster design.

## Required reading

Before producing the artwork, read:

- [composition-and-anchor.md](references/composition-and-anchor.md) for slicing, anchor selection, level assignment, and continuity.
- [abstraction-language.md](references/abstraction-language.md) for the approved method library and level calibration.
- [cinematic-color-system.md](references/cinematic-color-system.md) for the default warm, nostalgic, Robot Dreams-inspired shared palette and level-specific color compression.
- [intentional-modular-composition.md](references/intentional-modular-composition.md) for readable module boundaries, controlled contrast, and optional secondary transitions.
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
9. Art-direct the three exact boundaries as visible module relationships. Allow sharp or obvious changes in medium, value, palette, texture, or abstraction, but eliminate halos, misalignment, duplicate forms, and other accidental compositing artifacts. Do not overwrite protected Anchor pixels.
10. Deterministically composite the source Anchor back into the poster and verify it against the source. Accept a visible boundary when protection conflicts with seamlessness.
11. Art-direct the poster using shared motifs, rhythm, limited palette relationships, or structural echoes without forcing every slice into one painting language.
12. Inspect source preservation, face identity, four-state readability, intentional boundary design, and poster-level coherence, then validate every required condition in [subjects-validation.md](references/subjects-validation.md) before delivery.

## Decision priority

Resolve conflicts in this order:

1. Primary Face Identity Lock.
2. Reality Anchor Source Preservation.
3. Human Body Continuity.
4. Architectural Identity.
5. Four-State Readability and Abstraction Level Assignment.
6. Intentional Modular Boundary Design.
7. Global Color Relationship.
8. Artistic Experimentation.

Never let a lower-priority rule modify a higher-priority protected region. Maintain four equal logical slices while applying this protection hierarchy.

## Core principles

- Preserve one source fragment exactly; generate only the other three.
- Simplify people before breaking them.
- Remove architectural detail before identity.
- Make abstraction a structural transformation, not a filter.
- Keep a related warm, nostalgic cinematic color family while allowing clear slice-to-slice color differences.
- Keep boundaries mathematically exact and intentionally readable.
- Deliver one coherent poster, never four independent images.
