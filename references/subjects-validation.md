# Subject Rules and Validation

## Contents

- People
- Architecture
- Hard constraints
- Validation checklist

## People

Only the primary head is hard-locked: preserve the primary face identity and natural head anatomy above everything. The rest of the body is not hard-locked — body parts may cross module boundaries and exist at different abstraction levels simultaneously, like buildings.

Keep head protection first: preserve face identity, head contour, hairline, and face-to-neck continuity longest. For the body, the treatment comes from the region's own level's pool (see [abstraction-language.md](abstraction-language.md)); silhouette, head/body relationship, pose, gesture, and presence are soft preferences — readable fragments across abstraction states are acceptable and can be more impactful than a fully continuous body. Color Blocking may support any Primary Method but is never a Primary Method.

- **30% (30% pool: Colored Sketch / Line Abstraction / Painterly Abstraction):** preserve proportions, pose, silhouette, clothing structure, and face direction; reduce surface detail. Colored Sketch carries the figure through strokes and clothing color; Line Abstraction through contour/pose lines; Painterly Abstraction through brush masses. Normally omit geometry (Geometry is not in the 30% pool).
- **65% (65% pool: Geometric Abstraction / Fragmentation / Collage Abstraction):** restructure the figure through source-derived geometric planes (clothing, massing), controlled fragmentation, or collage recomposition — not through painterly masses or color blocks (those belong to other pools). Simplify face and body detail; keep the figure traceable.
- **90% (90% pool: Shape Reduction / Chinese Ink Wash / Cartoon Pixel):** permit a symbolic or silhouette figure (Shape Reduction), a 写意 ink figure with dominant negative space (Chinese Ink Wash), or a flat pixel icon figure (Cartoon Pixel), retaining a recognizable human silhouette, head/body relation, pose direction, and presence. Painterly treatment, geometry, and dominant color blocking are NOT eligible at 90% under the default pools.

Do not use fragmentation as the default for important people. If the 65% pool selects Fragmentation, keep each fragment readable and avoid duplicated anatomy, displaced face fragments, malformed photorealistic remnants, misaligned cutouts, or random polygon bodies. When fidelity is difficult, prefer an intentional silhouette, contour, or geometric mass from the 65% pool. A body may span multiple abstraction states, but never accidentally duplicate limbs or faces.

## Architecture

Remove surface detail before architectural identity. Simplify material texture, grain, reflections, repetitive windows, decoration, signage, small shadows, weathering, and minor variation before silhouette, primary massing, volume relationships, perspective, roofline, skyline, large openings, structural voids, or landmark features.

- At 30%, keep the building clearly recognizable. Simplify texture, windows, and shadows; add restrained sketch, planes, or color blocks while preserving proportions, silhouette, mass, perspective, and landmarks.
- At 65%, collapse repeated details into lines or blocks, reduce façades to large planes, repaint materials, and simplify secondary structures while retaining outer silhouette, mass arrangement, dominant perspective, façade rhythm, and distinctive features when possible.
- At 90%, reduce the building to an architectural identity skeleton: retain several cues such as silhouette, roofline, mass arrangement, perspective, iconic feature, or structural rhythm.

Derive geometry from actual façade planes, volumes, rooflines, perspective, and divisions. Fragment secondary information before major silhouette, volumes, roofline, or landmark features. Preserve primary or landmark buildings strongly, important background buildings moderately, and allow incidental architecture to become generic background masses.

## Hard constraints

Never:

1. Create more or fewer than four logical states or output them as independent images.
2. Stretch or compress the source, or move the state-ownership boundaries after ownership assignment.
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
14. (One-shot fallback path only.) Perform source-face restoration without first applying the Face Restoration Gate. The deterministic pipeline never runs the gate — its primary head is source-composited and verify-checked.
15. Replace an acceptable coherent face merely to increase source-pixel equality.
16. Select any restoration candidate that introduces facial patch appearance, geometry mismatch, jaw or cheek mismatch, hairline mismatch, skin-tone discontinuity, neck mismatch, body continuity breaks, or unnatural proportions.
17. Force all visible modules into four hard rectangular bands when irregular content-aware edges would produce a stronger composition.
18. Collapse the design into one dominant image with three tiny fragments, random scraps, or an unstructured montage.
19. Treat component reduction as permission to remove the primary person, identity-critical face, dominant crowd event, landmark or primary architecture, or a major scene-defining mass.
20. Fall back to Logical Zone 2 before checking for an important architectural subject, or choose an architectural Anchor from minor façade detail alone.
21. Move the ownership boundaries to contain an important building, or force the entire building into one photographic module when a coherent cross-state treatment would strengthen the composition.
22. Trigger architecture-anchor selection from an ordinary background building, generic streetscape façade, distant structure, incidental urban fabric, or visible area alone.
23. Treat 30%, 65%, and 90% as the same structural abstraction level with only palette, brush texture, rendering style, or medium changes.
24. Output the four states as four full-image versions of the photograph — a 2×2 grid, a strip, a contact sheet, or any layout where the full scene appears more than once — instead of one continuous image tiled by four adjacent regions.
25. Force the whole primary body or a whole building into exactly one abstraction state. Cross-state presence is allowed and encouraged when it strengthens the poster; only accidental duplication (clones, double faces, ghost edges) is forbidden.
26. In the legacy torn family, create blob-shaped territories, isolated islands, enclosed pockets, contour loops, U-shaped wraps around subjects, large peninsulas or wedges that destroy the ordered four-region structure, or seams that repeatedly follow object contours. Torn seams are layout-defined cuts, not semantic segmentation contours; irregularity belongs to the seam geometry, not to the global module topology.
27. In the default natural family, produce arbitrary blob segmentation, tiny floating scraps, disconnected islands, contact-sheet layouts, or regions that look like four separate paper sheets (z-order, sheet bodies, sheet grain). The poster must read as ONE photograph in four natural regions, each region differing only by abstraction, with the paper material layer representing only the boundary.
28. Redraw a recognizable scene object (mountain, building, road, vehicle, pole, tree, person) as a separate copy inside more than one region. One-Scene / One-Object Ownership: cross-state coexistence means one physical object crosses a boundary and changes rendering language — never the same object separately redrawn once inside each region.

## Validation checklist

Confirm before delivery:

- Four disjoint state-ownership regions tile the source-ratio canvas exactly (the exact masks the script writes). Ownership, Reality Anchor selection, and 30/65/90 assignment are defined directly by the region masks. Equal/quarter-based regions exist only in the `rect` family; the default `natural`/`collage` families are composition-driven.
- Direction follows semantic structure rather than orientation alone.
- Exactly one anchor exists via the script's `--anchor auto`: primary-face ownership (the PRIMARY face's largest overlap inside the region masks) -> side-weighted central corridor (no primary face) -> Logical Zone 2 fallback. Crowd/architecture anchors are agent-chosen via `--anchor 1..4` — the script does not auto-detect them.
- Crowd ownership reflects concentration, activity density, event significance, and coherent focal grouping—not raw person count alone.
- Architecture ownership reflects silhouette, primary massing, landmark features, perspective-defining structure, and semantic importance—not minor façade detail alone.
- Ordinary background buildings do not trigger architecture ownership unless one demonstrably functions as a landmark, scene-recognition cue, major compositional subject, or main non-human subject.
- The state-ownership boundaries remain fixed even when a face, crowd, or important building crosses them; visible module edges may adapt around content.
- On the deterministic pipeline the primary head is source-composited by construction and verified by `--mode verify` — the Face Restoration Gate does NOT run and no restoration is performed. The Candidate A/B gate items below apply ONLY to the one-shot / non-deterministic fallback path.
- Candidate A, the pre-restoration coherent candidate, remains eligible for final delivery (fallback path only).
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
- Four substantial natural regions are immediately readable at thumbnail size as parts of ONE photograph, and neighboring states differ through at least two deliberate visual signals.
- Hybrid Transition is applied: backgrounds, skies, ground planes, and large color fields may change rendering abruptly across a boundary (structure and medium change), while important people and buildings retain semantic continuity. The shared limited palette does not change — only each region's proportion rebalancing does; no module-level color break.
- The visible boundaries are intentionally contour-aware, collage-like, brush-defined, shape-defined, architectural, people-aware, or selectively straight; the underlying state-ownership masks stay exactly as the script wrote them.
- No muddy feathering, ragged mask, accidental gap, misaligned body, ghost edge, duplicated form, or cutout halo remains. The default soft transition band (`--feather`, ~2%) keeps boundaries gentle, but the four states remain readable at thumbnail size.
- The final image is ONE continuous source-ratio canvas tiled by four adjacent regions that share edges; the scene appears exactly once.
- One-Scene / One-Object Ownership: every recognizable scene object appears once, spatially continuous on the final canvas; an object may cross regions and change rendering language, but never restarts, repeats, or is redrawn as another copy inside another region.
- Every region — including Reality — shows only its own SLICE of the photograph; the four slices together compose the full photograph exactly once. Reality is the photographic version of ITS slice only; no region contains the full image, and no abstract zone is a second full-image copy at a different abstraction level; `--mode verify` warns when a zone render resembles the full source scene.
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
- The three abstract states select their Primary Abstraction Methods through the **Level-Gated system** (each level's pool is disjoint, so `30% ≠ 65% ≠ 90%` is guaranteed by construction): 30% = Colored Sketch / Line Abstraction / Painterly Abstraction; 65% = Geometric Abstraction / Fragmentation / Collage Abstraction; 90% = Shape Reduction / Chinese Ink Wash / Cartoon Pixel; Color Blocking is Supporting-only. All inside the same photograph — LEVEL ≠ MEDIUM.
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
- The four zone masks tile the canvas exactly with no gaps or overlaps. In the non-natural families areas stay roughly balanced (the script warns when max/min exceeds 2.5); the default natural family allows composition-driven region sizes.
- `scripts/slice_and_compose.py --mode verify` passes: output size matches the source, the four zone masks tile the canvas exactly, the Reality Anchor region equals the source inside its mask, the head protection region equals the source (the PRIMARY head is never reconstructed, even when a face box straddles a zone boundary), and the boundary-appropriate topology checks pass (natural/collage: region size and connectivity; torn: 3 continuous ordered seams, no crossings, no islands/pockets).
- Per-zone rendered crops were composed at fixed coordinates through their zone masks without scaling, gaps, or overlaps; no grid, strip, or contact-sheet layout was delivered.
- Every slice clearly expresses Reality, 30%, 65%, or 90%; no global treatment dissolves them into one continuous illustration or abstraction gradient.
- The four regions share ONE shared limited poster palette (Robot Dreams Shared Palette System), built by reinterpreting the source photograph's color EVIDENCE through the Robot Dreams palette families — never by copying the photo's literal colors. Color differences emerge from each region's abstraction rebalancing the proportions of the shared palette — never from arbitrary module-level recoloring or per-region palette identities.
- The 30% slice remains closest to local photographic color, the 65% slice uses stronger grouping, and the 90% slice is most interpretive while retaining shared color DNA.
- Saturation and contrast remain controlled; a small repeated accent set guides rhythm without scattered high-chroma clashes.
