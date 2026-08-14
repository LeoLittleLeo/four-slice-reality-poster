# Composition, Slicing, and Reality Anchor

## Contents

- Canvas and equal slices
- Direction selection
- Reality Anchor
- Abstraction assignment
- Spatial freedom and cohesion

## Canvas and equal slices

Preserve the source image's aspect ratio and use its dimensions as the compositional basis unless the user explicitly requests another format. Do not stretch, compress, or arbitrarily extend the canvas.

Divide the image into exactly four geometrically equal slices. Use either four equal vertical slices or four equal horizontal slices. Do not create unequal panels, a dominant center panel, or move boundaries to protect a face, person, building, or object. Build hierarchy through visual treatment rather than panel size.

Recombine all slices into the same overall rectangle and output one poster, not four independent images.

## Direction selection

Choose vertical slices when the semantic composition, subjects, architecture, landscape, or visual flow develops primarily across the width. Choose horizontal slices when foreground, middle ground, background, sky, buildings, people, or ground create strong top-to-bottom layering.

Base the decision primarily on semantic composition, subject distribution, visual flow, and dominant structure. Treat portrait or landscape orientation only as a secondary clue; do not map orientation mechanically to slice direction.

## Reality Anchor

Use exactly one photographic Reality Anchor.

When a clear primary human subject exists:

1. Identify the primary subject using face size, foreground placement, focus, centrality, compositional dominance, and visual salience.
2. Estimate the visible face area falling in each fixed slice.
3. Use the slice containing the largest portion of that primary face as the anchor.

If a face crosses boundaries, keep the fixed equal boundaries and use largest-area ownership. Do not custom-crop, enlarge the face slice, or reconstruct the face across panels. For multiple people, use only the primary visual subject to determine the single anchor.

If no reliable primary face exists—because there is no person, faces are small or obscured, or the image is mainly architecture, landscape, object, or interior—use Slice 2: second from the left for vertical slices or second from the top for horizontal slices.

For scenes without an important person, make the Anchor source-preserved through full-block compositing. For important-person scenes, protect the source face core while using the coherent candidate for the surrounding head, hair, shoulders, clothing, and cross-boundary body context. Do not require full-block restoration when it creates visible human stitching errors.

Use `../scripts/restore_protected_anchor.py --mode face-core --face-box X0 Y0 X1 Y1` for important-person scenes and verify exact source pixels inside the face core. Use `--mode full-anchor` for non-human scenes or as a comparison candidate. Permit temperature, tone, saturation, brightness, contrast, or subtle grain only through deterministic non-generative processing that does not change identity.

## Abstraction assignment

Assign exactly one 30%, one 65%, and one 90% abstraction treatment to the three non-anchor slices. Do not arrange the levels automatically as a gradient or make abstraction increase with distance from the anchor. Permutations such as `65 | Reality | 90 | 30` are valid. Choose by visual balance, semantic importance, subject placement, rhythm, palette, and contrast.

Interpret percentage as departure from photographic representation—not opacity, modified pixel count, blur, saturation, or filter strength.

## Spatial freedom and cohesion

Inside abstract slices, permit deliberate changes to object position, scale, overlap, depth, layer order, perspective emphasis, hierarchy, and occlusion. Permit merging, separation, duplication of selected fragments, and flattened depth. Exact pixel alignment with the source or neighboring slices is not required.

Make the four-slice structure clearly perceptible through each module's dominant treatment and through intentional boundary design. Allow straight boundaries, decisive tonal or chromatic breaks, and distinct media. Do not require gutters or drawn divider lines, but permit them when they strengthen the editorial system. Preserve important face identity and avoid accidental body or architectural misalignment at boundaries. Relate the modules with selected palette echoes, repeated lines, directional rhythm, or shape relationships without forcing them into one uniform rendering language. Follow [intentional-modular-composition.md](intentional-modular-composition.md).
