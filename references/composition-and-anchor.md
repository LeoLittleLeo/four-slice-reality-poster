# Composition, Slicing, and Reality Anchor

## Contents

- Canvas and equal logical zones
- Direction selection
- Reality Anchor
- Crowd Anchor fallback
- Abstraction assignment
- Spatial freedom and cohesion

## Canvas and equal logical zones

Preserve the source image's aspect ratio and use its dimensions as the compositional basis unless the user explicitly requests another format. Do not stretch, compress, or arbitrarily extend the canvas.

Begin with exactly four geometrically equal hidden logical zones. Use either four equal vertical ownership zones or four equal horizontal ownership zones. Use them only for Reality Anchor selection, crowd and subject ownership, 30%/65%/90% assignment, and four-state validation. Do not move these hidden boundaries to protect content.

Translate the hidden ownership system into four visible modules that may be irregular, overlapping in influence, contour-aware, and non-rectangular. Keep them roughly balanced in area and visual importance. Recombine them into the same overall rectangle and output one poster, not four independent images.

## Direction selection

Choose vertical slices when the semantic composition, subjects, architecture, landscape, or visual flow develops primarily across the width. Choose horizontal slices when foreground, middle ground, background, sky, buildings, people, or ground create strong top-to-bottom layering.

Base the decision primarily on semantic composition, subject distribution, visual flow, and dominant structure. Treat portrait or landscape orientation only as a secondary clue; do not map orientation mechanically to slice direction.

## Reality Anchor

Use exactly one photographic Reality Anchor.

When a clear primary human subject exists:

1. Identify the primary subject using face size, foreground placement, focus, centrality, compositional dominance, and visual salience.
2. Estimate the visible face area falling in each fixed slice.
3. Use the logical zone containing the largest portion of that primary face as the anchor owner.

If a face crosses hidden logical boundaries, keep them fixed and use largest-area ownership. The visible Reality module may expand around the protected face or follow its contour while logical ownership remains unchanged. For multiple people, use only the primary visual subject to determine the single anchor.

## Crowd Anchor fallback

When no reliable single primary face exists, check for a crowd-dominant semantic region before defaulting to Logical Zone 2.

Select a slice as the Reality Anchor when:

- no clear single primary-subject face exists;
- a group of people forms the image's main semantic focus;
- the group is visually concentrated mostly within one slice; and
- that slice carries the strongest crowd presence, human activity density, or event significance.

Determine crowd ownership by combining visible-people concentration, density of human activity, semantic importance of the group, and whether the crowd reads as one coherent event or focal cluster. Do not use raw person count alone when another slice contains the more important human event.

Keep all four hidden equal boundaries fixed. Do not move or resize logical zones to accommodate a crowd. If a crowd spans multiple zones, select the zone with the strongest combined concentration and semantic importance. Allow the visible Reality module to follow the crowd grouping when the overall module system remains balanced.

Use Logical Zone 2—second from the left for vertical ownership or second from the top for horizontal ownership—only when no reliable primary face exists and no zone has a clearly dominant crowd grouping, or when the scene is primarily non-human.

For scenes without an important person, source-preserve the visible Reality module through an irregular source mask when useful. For important-person scenes, keep the coherent candidate final when the face already passes the Face Restoration Gate.

When restoration is genuinely needed, prefer `../scripts/restore_protected_anchor.py --mode face-mask --face-gate-failed --alignment-verified --mask MASK.png`. Supply `--aligned-source ALIGNED.png` when a registered source has been prepared. Use `--mode face-core --face-gate-failed --alignment-verified --face-box X0 Y0 X1 Y1` only as a last fallback. Use `--mode source-mask --mask-excludes-primary-face` only for a non-face irregular Reality module. Use full-anchor restoration only for scenes confirmed to have no primary face.

## Abstraction assignment

Assign exactly one 30%, one 65%, and one 90% abstraction treatment to the three non-anchor slices. Do not arrange the levels automatically as a gradient or make abstraction increase with distance from the anchor. Permutations such as `65 | Reality | 90 | 30` are valid. Choose by visual balance, semantic importance, subject placement, rhythm, palette, and contrast.

Interpret percentage as departure from photographic representation—not opacity, modified pixel count, blur, saturation, or filter strength.

## Spatial freedom and cohesion

Inside abstract slices, permit deliberate changes to object position, scale, overlap, depth, layer order, perspective emphasis, hierarchy, and occlusion. Permit merging, separation, duplication of selected fragments, and flattened depth. Exact pixel alignment with the source or neighboring slices is not required.

Make the four-state structure clearly perceptible through each visible module's dominant treatment and boundary design. Derive edges from human silhouettes, crowd groupings, building contours, rooflines, skylines, tree canopies, roads or rails, shadow masses, large color fields, or painterly and sketch strokes. Preserve face identity and avoid accidental human or architectural mismatch. Follow [intentional-modular-composition.md](intentional-modular-composition.md).
