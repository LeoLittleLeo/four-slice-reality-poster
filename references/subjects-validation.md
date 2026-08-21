# Subject Rules and Validation

## Contents

- People
- Architecture
- Hard constraints
- Validation checklist

## People

Only the primary head is hard-locked: preserve the primary face identity and natural head anatomy above everything. The rest of the body is not hard-locked — body parts may cross module boundaries and exist at different abstraction levels simultaneously, like buildings.

Keep head protection first: preserve face identity, head contour, hairline, and face-to-neck continuity longest. For the body, prioritize shape simplification, contour abstraction, color blocking, and painterly support; silhouette, head/body relationship, pose, gesture, and presence are soft preferences — readable fragments across abstraction states are acceptable and can be more impactful than a fully continuous body.

- At 30%, preserve proportions, pose, silhouette, clothing structure, and face direction; reduce surface detail; normally omit geometry.
- At 65%, strengthen simplification, contours, color blocks, and painterly masses; simplify face and body detail; use geometry only as an accent.
- At 90%, permit a symbolic figure, dominant color blocking, painterly treatment, and limited geometry while retaining a recognizable human silhouette, head/body relation, pose direction, and presence.

Do not use fragmentation as the default for important people. If used, keep each fragment readable and avoid duplicated anatomy, displaced face fragments, malformed photorealistic remnants, misaligned cutouts, or random polygon bodies. When fidelity is difficult, prefer an intentional silhouette, contour, color block, or painterly mass. A body may span multiple abstraction states, but never accidentally duplicate limbs or faces.

## Architecture

Remove surface detail before architectural identity. Simplify material texture, grain, reflections, repetitive windows, decoration, signage, small shadows, weathering, and minor variation before silhouette, primary massing, volume relationships, perspective, roofline, skyline, large openings, structural voids, or landmark features.

- At 30%, keep the building clearly recognizable. Simplify texture, windows, and shadows; add restrained sketch, planes, or color blocks while preserving proportions, silhouette, mass, perspective, and landmarks.
- At 65%, collapse repeated details into lines or blocks, reduce façades to large planes, repaint materials, and simplify secondary structures while retaining outer silhouette, mass arrangement, dominant perspective, façade rhythm, and distinctive features when possible.
- At 90%, reduce the building to an architectural identity skeleton: retain several cues such as silhouette, roofline, mass arrangement, perspective, iconic feature, or structural rhythm.

Derive geometry from actual façade planes, volumes, rooflines, perspective, and divisions. Fragment secondary information before major silhouette, volumes, roofline, or landmark features. Preserve primary or landmark buildings strongly, important background buildings moderately, and allow incidental architecture to become generic background masses.

## Hard constraints

Never:

1. Create more or fewer than four logical states or output them as independent images.
2. Stretch or compress the source, or move the hidden equal logical boundaries after ownership assignment.
3. Create more than one Reality Anchor, or discard its intended reality role without reason.
4. Treat filters as abstraction or turn all four slices into illustrations.
5. Force levels into sequential order or derive them from anchor distance.
6. Generate unrelated abstract slices or random source-independent geometry.
7. Destroy important human readability before photographic detail.
8. Default to heavy human fragmentation, malformed anatomy, duplicated limbs, displaced faces, or accidental masking artifacts.
9. Destroy important architectural identity before surface detail or replace a landmark with generic architecture.
10. Interpret 90% abstraction as permission to discard all source DNA.
11. Blend the four states into one nearly uniform painterly image or hide the modular structure behind broad feathering and continuous texture migration.
12. Use defective boundary artifacts such as muddy blur, ragged masking, duplicated outlines, ghost edges, offset object copies, cutout halos, accidental gaps, or mismatched anatomy.
13. Give slices unrelated palette identities or drift into neon cyberpunk, purple-magenta sci-fi glow, cold steel monochrome, random rainbow abstraction, hyper-saturated pop art, dark horror, lifeless gray, or glossy commercial-ad color unless explicitly requested.
14. Perform source-face restoration without first applying the Face Restoration Gate.
15. Replace an acceptable coherent face merely to increase source-pixel equality.
16. Select any restoration candidate that introduces facial patch appearance, geometry mismatch, jaw or cheek mismatch, hairline mismatch, skin-tone discontinuity, neck mismatch, body continuity breaks, or unnatural proportions.
17. Force all visible modules into four hard rectangular bands when irregular content-aware edges would produce a stronger composition.
18. Collapse the design into one dominant image with three tiny fragments, random scraps, or an unstructured montage.
19. Treat component reduction as permission to remove the primary person, identity-critical face, dominant crowd event, landmark or primary architecture, or a major scene-defining mass.
20. Fall back to Logical Zone 2 before checking for an important architectural subject, or choose an architectural Anchor from minor façade detail alone.
21. Move hidden logical boundaries to contain an important building, or force the entire building into one photographic module when a coherent cross-state treatment would strengthen the composition.
22. Trigger architecture-anchor selection from an ordinary background building, generic streetscape façade, distant structure, incidental urban fabric, or visible area alone.
23. Treat 30%, 65%, and 90% as the same structural abstraction level with only palette, brush texture, rendering style, or medium changes.
24. Output the four states as four full-image versions of the photograph — a 2×2 grid, a strip, a contact sheet, or any layout where the full scene appears more than once — instead of one continuous image tiled by four adjacent regions.
25. Force the whole primary body or a whole building into exactly one abstraction state. Cross-state presence is allowed and encouraged when it strengthens the poster; only accidental duplication (clones, double faces, ghost edges) is forbidden.
26. In the legacy torn family, create blob-shaped territories, isolated islands, enclosed pockets, contour loops, U-shaped wraps around subjects, large peninsulas or wedges that destroy the ordered four-region structure, or seams that repeatedly follow object contours. Torn seams are layout-defined cuts, not semantic segmentation contours; irregularity belongs to the seam geometry, not to the global module topology.
27. In the default natural family, produce arbitrary blob segmentation, tiny floating scraps, disconnected islands, contact-sheet layouts, or regions that look like four separate paper sheets (z-order, sheet bodies, sheet grain). The poster must read as ONE photograph in four natural regions, each region differing only by abstraction, with the paper material layer representing only the boundary.
28. Redraw a recognizable scene object (mountain, building, road, vehicle, pole, tree, person) as a separate copy inside more than one region. One-Scene / One-Object Ownership: cross-state coexistence means one physical object crosses a boundary and changes rendering language — never the same object separately redrawn once inside each region.

## Validation checklist

Confirm before delivery:

- Exactly four equal hidden logical zones govern ownership and abstraction assignment inside one source-ratio canvas.
- Direction follows semantic structure rather than orientation alone.
- Exactly one anchor exists in this order: primary-face ownership, crowd-dominant ownership, important-architecture ownership, then Logical Zone 2 fallback.
- Crowd ownership reflects concentration, activity density, event significance, and coherent focal grouping—not raw person count alone.
- Architecture ownership reflects silhouette, primary massing, landmark features, perspective-defining structure, and semantic importance—not minor façade detail alone.
- Ordinary background buildings do not trigger architecture ownership unless one demonstrably functions as a landmark, scene-recognition cue, major compositional subject, or main non-human subject.
- Hidden logical boundaries remain unchanged even when a face, crowd, or important building crosses them; visible module edges may adapt around content.
- Candidate A, the pre-restoration coherent candidate, remains eligible for final delivery.
- The Face Restoration Gate confirms recognizable identity, natural facial proportions and feature placement, coherent jaw/cheek/hairline/neck relationships, and absence of obvious artifacts.
- Restoration is skipped when Candidate A passes the gate.
- When restoration is attempted, Candidate B replaces A only if identity visibly improves while anatomy and continuity remain natural and no patch artifact appears.
- Pixel restoration is used only with an irregular semantic mask or verified alignment; rectangular face-box restoration is a last fallback.
- No head seam distortion or awkward head silhouette mismatch remains; head contour, hair edge, and face-to-neck connection stay coherent.
- Body, clothing, and building continuity across abstraction states may be soft or intentionally broken; the only hard rules are head identity/continuity and the absence of accidental duplication.
- The selected final candidate balances face identity, human continuity, modular readability, and intentional boundaries instead of maximizing full-Anchor source similarity alone.
- The other slices contain exactly one 30%, one 65%, and one 90% structural abstraction treatment in a deliberately non-mechanical order.
- The 30%, 65%, and 90% modules differ in detail retention, component density, spatial fidelity, shape fidelity, and photographic surface retention.
- At least one major difference between every pair of abstract modules comes from structural information density, not only palette or rendering style.
- Reject the result if the three abstract modules could be mistaken for the same abstraction level with different color or medium.
- Each abstract slice uses one or more source-derived approved methods rather than filters alone.
- Dense secondary components may be reduced, merged, grouped, or selectively omitted, but the scene remains semantically identifiable rather than emptied or replaced.
- The primary person, identity-critical face, dominant crowd event, landmark or primary architecture, and major scene-defining masses survive component reduction.
- People remain readable through silhouette, pose, and presence; geometry and fragmentation remain controlled.
- Important architecture loses surface detail before silhouette, massing, perspective, or landmark identity.
- When important architecture owns the Anchor, its identity-critical portion remains photographic while other portions may continue through abstract modules with coherent silhouette, massing, perspective, landmark identity, and major structural rhythm.
- Abstract slices retain source visual DNA even when spatial relationships change.
- Four roughly balanced, ordered sequential regions are immediately readable at thumbnail size, and neighboring states differ through at least two deliberate visual signals.
- Hybrid Transition is applied: backgrounds and large color fields may break abruptly, while important people and buildings retain semantic continuity.
- Hidden ownership zones remain geometrically equal while visible boundaries are intentionally contour-aware, collage-like, brush-defined, shape-defined, architectural, people-aware, or selectively straight.
- No muddy feathering, ragged mask, accidental gap, misaligned body, ghost edge, duplicated form, or cutout halo remains. The default soft transition band (`--feather`, ~2%) keeps boundaries gentle, but the four states remain readable at thumbnail size.
- The final image is ONE continuous source-ratio canvas tiled by four adjacent regions that share edges; the scene appears exactly once.
- One-Scene / One-Object Ownership: every recognizable scene object appears once, spatially continuous on the final canvas; an object may cross regions and change rendering language, but never restarts, repeats, or is redrawn as another copy inside another region.
- The full photograph appears exactly once (the Reality module). Each abstract zone re-renders only its own slice — never a second, third or fourth full-image copy at different abstraction levels; `--mode verify` warns when a zone render resembles the full source scene.
- The default boundary family is **Natural Regions** (`--boundary natural`):
  ONE photograph jointly composed of four natural regions, each region
  differing only by its abstraction; the paper material layer is the
  representation of the boundary (a torn-paper seam where the abstraction
  changes) — not four separate paper sheets (no z-order, no sheet bodies, no
  sheet grain). Optional families: `collage` (layered torn-paper sheets),
  legacy `torn` (ordered seams), `contour` (semantic contours), `mask`,
  `rect`.
- At thumbnail size, the poster reads as one continuous photograph with four
  natural regions and torn-paper seams at the boundaries — not four paper
  sheets, not four wavy strips with decorative lines, not four unrelated
  medium filters, not arbitrary blob segmentation.
- The four regions are substantial and connected (each >= ~6% of the canvas,
  no islands/pockets/scattered fragments) and may have very different visible
  areas — no quarter-based balance requirement in the default natural family.
- The three abstract states MUST use three different Primary Abstraction
  Methods (30% ≠ 65% ≠ 90%), all inside the same photograph — LEVEL ≠ MEDIUM.
- Reality Anchor: script `--anchor auto` implements face ownership ->
  side-weighted central corridor -> Logical Zone 2; crowd/architecture anchors
  are agent-chosen via `--anchor 1..4` (documentation matches implementation).
- Legacy torn family: Ordered Strip Topology holds (Zone 1 broadly
  left-of/above Zone 2, etc.); every internal boundary is one continuous
  edge-to-edge seam.
- When Semantic Contour is chosen, its heuristics are sanity-checked:
  built-in sky/road/person masks are overridden by supplied
  `--class-masks-dir` masks or disabled with `--no-auto-semantic` whenever
  they misdetect a scene.
- The four zone masks tile the canvas exactly with no gaps or overlaps; zone
  areas stay roughly balanced (the script warns when max/min exceeds 2.5).
- `scripts/slice_and_compose.py --mode verify` passes: output size matches the source, the four zone masks tile the canvas exactly, the Reality Anchor region equals the source inside its mask, the head protection region equals the source (the primary face is never reconstructed, even when a face box straddles a zone boundary), and torn topology checks pass (3 continuous ordered seams, no crossings, no islands/pockets).
- Per-zone rendered crops were composed at fixed coordinates through their zone masks without scaling, gaps, or overlaps; no grid, strip, or contact-sheet layout was delivered.
- Every slice clearly expresses Reality, 30%, 65%, or 90%; no global treatment dissolves them into one continuous illustration or abstraction gradient.
- The poster maintains broad warm, nostalgic cinematic relationships while allowing clear, purposeful color differences among modules.
- The 30% slice remains closest to local photographic color, the 65% slice uses stronger grouping, and the 90% slice is most interpretive while retaining shared color DNA.
- Saturation and contrast remain controlled; a small repeated accent set guides rhythm without scattered high-chroma clashes.
