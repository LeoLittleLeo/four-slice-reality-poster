---
name: four-slice-reality-poster
description: "Transform a user-supplied photograph into one readable four-state modular mixed-media poster made of exactly four equal slices: one Reality Anchor and three visibly distinct source-derived slices at approximately 30%, 65%, and 90% structural abstraction. Use for modular reality-versus-virtual posters, progressive abstraction artworks, editorial photo/illustration hybrids, or requests to preserve the original subject identity while juxtaposing four visual states. Protect the primary face core with source pixels while preserving head, shoulder, body, and boundary continuity; do not default to full-Anchor restoration when it creates visible human stitching errors."
---

# Four-Slice Reality / Abstraction Poster

Create one editorial poster that visibly juxtaposes four equal modules: one photographic source region and three clearly distinct, non-linear abstraction states.

## Default visual objective

**Readable four-state modular poster first, seamless cinematic blending second.**

Make the four equal slices immediately legible as intentional modules while keeping them inside one poster system. Allow clear boundaries, decisive rendering changes, and noticeable color differences. Do not dissolve the entire image into one uniformly painted scene. A boundary may be straight, sharp, tonal, chromatic, textural, or medium-based; it must look art-directed rather than accidental.

Default to **Hybrid Transition**: allow backgrounds and large color fields to change abruptly, preserve semantic continuity for important people and buildings, and never force every boundary to be fully seamless. Keep all four states clearly readable; make boundaries visibly present whenever that strengthens modularity or poster design.

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

Keep the four slices inside the **same cinematic emotional universe**, but do not force them into nearly identical grading. Give each module a clearly different dominant color role when useful. For example:

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

## Face Identity Lock & Protected Source Region

Treat the primary face core as the non-generative protected source region. **The primary face is not content that should be faithfully regenerated. It is source content that should not be regenerated at all whenever source-preserving compositing is available.** Do not assume that the entire rectangular Anchor must always be restored.

Use this execution model:

1. Determine the four exact logical slices, Reality Anchor, primary face core, head contour, hair edge, shoulders, clothing edge, and cross-boundary body connections before generation.
2. Protect the identity-critical face core with a hard source mask. Keep the larger head and body context available for boundary-aware continuity unless a broader mask is demonstrably safe.
3. Preserve the strongest visually coherent generated candidate before any restoration; never downgrade it automatically to an intermediate state.
4. Produce a face-core restoration candidate by compositing only the identity-critical source face pixels back into the coherent candidate. Use `scripts/restore_protected_anchor.py --mode face-core --face-box ...` when local files are available.
5. Optionally produce a full-Anchor restoration candidate for comparison, especially for scenes without an important person. Do not select it when it introduces head, hair, shoulder, clothing, body, or silhouette mismatch.
6. Select the final candidate by face identity and human continuity, not by maximum Anchor pixel similarity alone.

If the Anchor contains the primary face, treat the face core as the highest-priority non-generative region. Never redraw or infer the eyes, nose, mouth, eyebrows, identity-bearing facial proportions, feature placement, texture structure, or identity characteristics. Preserve the surrounding head contour, hair silhouette, shoulder line, clothing edge, and body connection from the visually coherent candidate when replacing the full Anchor would break them.

For important-person scenes, default to exact source pixels for the face core, not the full Anchor rectangle. Allow a small deterministic feather ring outside the exact core to avoid a facial patch edge, but verify that the core itself remains pixel-identical. Apply optional grading only through deterministic non-structural processing. For scenes without an important person, full-Anchor restoration remains valid.

Required invariant:

```text
final primary face = original source face
final human continuity = coherent head contour + coherent shoulders/body + intentional module boundary
```

Never accept:

```text
final primary face = AI reconstruction of original face
final candidate = full-block restoration with obvious head or body stitching errors
```

**Protect the primary face, not necessarily the entire Anchor block, when full-block restoration causes visible human seam distortion.** A visually coherent candidate with preserved face identity is preferable to a stricter source-restored candidate that introduces obvious head or body stitching errors.

## Workflow

1. Inspect the supplied photograph. Identify dimensions, orientation, semantic flow, primary people and faces, architecture, landmarks, important objects, dominant shapes, and palette.
2. Choose one semantic slicing direction: four equal vertical slices or four equal horizontal slices. Preserve the source aspect ratio and overall rectangular canvas. Never move boundaries afterward.
3. Select exactly one Reality Anchor. If a reliable primary face exists, use the slice containing the largest visible portion of that face. Otherwise use Slice 2.
4. Locate and protect the source primary face core before any generative edit. Preserve head, hair, shoulder, clothing, and body boundary context for continuity-aware candidate generation. Use full-Anchor protection by default only when no important person is present or when it does not create a human seam.
5. Assign 30%, 65%, and 90% abstraction exactly once to the remaining slices. Choose a non-mechanical permutation based on balance, meaning, rhythm, and color—not distance from the anchor.
6. Establish the Robot Dreams-inspired default color identity before generating the abstract slices. Treat this palette direction as a core visual constraint, not optional finishing. Give the three abstract slices distinct but related dominant color roles while keeping them inside the same warm, nostalgic, sunlit, slightly retro cinematic universe. Apply any Reality Anchor grading only deterministically and non-structurally, or leave the Anchor unchanged.
7. Select source-derived abstraction methods appropriate to each abstract slice. Treat abstraction as structural reinterpretation, never filter intensity.
8. Generate the modular composition and retain the strongest visually coherent candidate before restoration. Permit reconstruction in abstract slices while retaining source DNA and human semantic continuity.
9. Art-direct the three exact boundaries as visible module relationships. Allow sharp or obvious changes in medium, value, palette, texture, or abstraction, but eliminate halos, misalignment, duplicate forms, and other accidental compositing artifacts. Do not overwrite protected Anchor pixels.
10. For important-person scenes, restore only the face core into the coherent candidate, then compare it with any full-Anchor restoration candidate. For non-human scenes, full-Anchor restoration may remain the default.
11. Reject any candidate with head seam distortion, broken shoulder/body continuity, or an awkward human silhouette mismatch, even if it preserves more Anchor pixels.
12. Art-direct the poster using shared motifs, rhythm, limited palette relationships, or structural echoes without weakening face identity or human continuity.
13. Inspect face identity, head/body continuity, four-state readability, intentional boundary design, and poster-level coherence, then validate every required condition in [subjects-validation.md](references/subjects-validation.md) before delivery.

## Decision priority

Resolve conflicts in this order:

1. Primary Face Identity Lock.
2. Head, Shoulder, and Human Body Continuity.
3. Reality Anchor Role and Local Source Preservation.
4. Architectural Identity.
5. Four-State Readability and Abstraction Level Assignment.
6. Robot Dreams-Inspired Color Identity.
7. Intentional Modular Boundary Design.
8. Artistic Experimentation.

Never let a lower-priority rule modify a higher-priority protected region. Maintain four equal logical slices while applying this protection hierarchy. After face, source, human, architectural, and four-state protections are satisfied, make the Robot Dreams-inspired color identity outrank minor boundary smoothing and general artistic experimentation.

## Core principles

- Preserve the primary face core exactly; retain the most coherent head/body context around it.
- Simplify people before breaking them.
- Remove architectural detail before identity.
- Make abstraction a structural transformation, not a filter.
- Treat the Robot Dreams-inspired warm, nostalgic, sunlit, slightly retro palette as the default visual identity of the Skill. Keep all four modules inside this shared emotional color universe while allowing strong, intentional slice-to-slice dominant color differences.
- Keep boundaries mathematically exact and intentionally readable.
- Deliver one coherent poster, never four independent images.
