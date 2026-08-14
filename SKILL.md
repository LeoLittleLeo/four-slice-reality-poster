---
name: four-slice-reality-poster
description: "Transform a user-supplied photograph into one readable four-state modular mixed-media poster built from four equal hidden logical zones and four roughly balanced irregular visible modules: one Reality state and 30%, 65%, and 90% source-derived abstraction states. Use for editorial collage, contour-aware reality-versus-virtual posters, progressive abstraction artworks, or identity-preserving four-state portraits. Accept a visually coherent generated face when identity and anatomy are already sound; use source-face restoration only as a gated fallback that demonstrably improves the result."
---

# Four-Slice Reality / Abstraction Poster

Create one editorial poster that juxtaposes four roughly balanced, irregular visible modules governed by four equal hidden logical zones: one photographic Reality state and three clearly distinct, non-linear abstraction states.

## Default visual objective

**Readable four-state modular poster first, seamless cinematic blending second.**

Make the four states immediately legible as intentional visual fragments while keeping them inside one poster system. Do not require visible rectangular bands. Allow irregular, contour-aware, collage-like, brush-defined, shape-defined, architectural, and people-aware boundaries. Keep the four visible modules roughly balanced in area and visual importance; do not reduce them to one dominant image plus three scraps.

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

Keep the four visible modules inside the **same cinematic emotional universe**, but do not force them into nearly identical grading. Give each module a clearly different dominant color role when useful. For example:

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

Preserve primary-face identity without assuming that pixel restoration is always necessary. Keep the strongest visually coherent candidate eligible for final delivery.

### Face Restoration Gate

After producing the strongest visually coherent candidate, inspect the primary face before performing any source restoration. When it already meets the following conditions, accept it as the selected face candidate, skip restoration, and continue to poster-level art direction and validation:

- recognizable identity;
- correct facial proportions;
- natural eye, nose, and mouth placement;
- coherent jaw and cheek contour;
- coherent hairline;
- coherent face-to-neck connection; and
- no obvious facial generation artifact.

Do not composite source pixels merely to increase pixel equality. Attempt restoration only when the coherent candidate has a meaningful identity or facial-structure failure.

Use this decision flow:

```text
coherent candidate
→ Face Restoration Gate
    ├─ face acceptable → skip restoration → poster-level validation
    └─ face unacceptable → attempt restoration
                              ↓
                         validate restoration
                              ↓
                    select only if visually better
                              ↓
                    poster-level validation
```

Prefer restoration methods in this order:

1. no restoration when the face is acceptable;
2. irregular semantic face mask;
3. aligned or registered source-face restoration;
4. rectangular face-box restoration only as a last fallback.

Do not perform pixel-level restoration when source and candidate face geometry cannot be verified as aligned.

Use this execution model:

1. Determine the four logical zones, Reality Anchor, primary face, head contour, hairline, jaw, neck, shoulders, clothing edge, and cross-boundary body connections.
2. Preserve the strongest visually coherent generated candidate before any restoration.
3. Run the Face Restoration Gate. Skip restoration when identity, facial anatomy, hairline, and face-to-neck continuity are acceptable, then continue to poster-level validation.
4. If restoration is necessary, create Candidate B with an irregular semantic face mask or verified aligned source face. Use a rectangular face box only as a last fallback.
5. Compare Candidate A, the pre-restoration coherent candidate, with Candidate B. Select B only when identity improves and anatomy, head/jaw/neck continuity, skin tone, and compositing quality remain natural.
6. Reject B and return to A whenever restoration introduces a facial patch, geometry mismatch, hairline mismatch, skin-tone discontinuity, or unnatural proportions.

Never replace a visually coherent face with a source-restored face when restoration makes the person less natural. A restoration candidate must demonstrate actual visual improvement before it may become final.

Exact source pixels are preferred only when they can be restored without damaging visual coherence. Identity preservation—not mandatory pixel identity—is the final goal.

Required invariant:

```text
final primary face identity = preserved
final human continuity = coherent head contour + coherent shoulders/body + intentional module boundary
```

Never accept:

```text
final candidate = restoration with a facial patch, geometry mismatch, or broken head/body continuity
```

**A visually coherent candidate with preserved face identity is preferable to a source-restored candidate that introduces facial or human stitching errors.**

## Workflow

1. Inspect the supplied photograph. Identify dimensions, orientation, semantic flow, primary people and faces, architecture, landmarks, important objects, dominant shapes, and palette.
2. Choose one semantic logical-division direction: four equal hidden vertical zones or four equal hidden horizontal zones. Preserve the source aspect ratio and overall rectangular canvas. Never move these ownership boundaries afterward; do not require visible module edges to follow them.
3. Establish four equal hidden logical zones and select exactly one Reality Anchor ownership zone using this hierarchy: primary-face ownership first; crowd-dominant semantic ownership second; Logical Zone 2 only when neither exists or the scene is primarily non-human.
4. Identify the primary face and surrounding head/body continuity context before generation; do not pre-commit to source-pixel restoration.
5. Assign 30%, 65%, and 90% abstraction exactly once to the remaining logical zones. Choose a non-mechanical permutation based on balance, meaning, rhythm, and color—not distance from the anchor.
6. Establish the Robot Dreams-inspired default color identity before generating the abstract modules. Treat this palette direction as a core visual constraint, not optional finishing. Give the three abstract modules distinct but related dominant color roles while keeping them inside the same warm, nostalgic, sunlit, slightly retro cinematic universe. Apply any Reality Anchor grading only deterministically and non-structurally, or leave the Anchor unchanged.
7. Select source-derived abstraction methods appropriate to each abstract module. Treat abstraction as structural reinterpretation, never filter intensity.
8. Generate the modular composition and retain the strongest visually coherent candidate before restoration. Permit reconstruction in abstract modules while retaining source DNA and human semantic continuity.
9. Convert the hidden four-zone ownership into four roughly balanced irregular visible modules. Derive visible edges from people, crowds, architecture, skylines, trees, roads, shadows, large color fields, or expressive strokes. Allow modules to expand or contract around protected content without changing logical ownership.
10. Run the Face Restoration Gate. If Candidate A is acceptable, skip restoration and retain A for the remaining poster-level workflow. Otherwise attempt a geometrically verified irregular-mask or aligned restoration to create Candidate B.
11. Let Candidate B replace Candidate A only when identity improves without unnatural anatomy, patch appearance, skin mismatch, or broken head/jaw/neck/body continuity.
12. Art-direct the poster using shared motifs, rhythm, limited palette relationships, or structural echoes without weakening face identity or human continuity.
13. Inspect face identity, head/body continuity, four-state readability, intentional boundary design, and poster-level coherence, then validate every required condition in [subjects-validation.md](references/subjects-validation.md) before delivery.

## Decision priority

Resolve conflicts in this order:

1. Primary Face Identity and Natural Facial Coherence.
2. Head, Shoulder, and Human Body Continuity.
3. Reality Anchor Role and Local Source Preservation.
4. Architectural Identity.
5. Four-State Readability, Logical-Zone Ownership, and Abstraction Assignment.
6. Robot Dreams-Inspired Color Identity.
7. Intentional Modular Boundary Design.
8. Artistic Experimentation.

Never let a lower-priority rule modify a higher-priority protected region. Maintain four equal hidden logical zones while allowing irregular visible modules. After face, source, human, architectural, and four-state protections are satisfied, make the Robot Dreams-inspired color identity outrank minor boundary smoothing and general artistic experimentation.

## Core principles

- Preserve primary-face identity and natural anatomy; never restore pixels merely for equality.
- Simplify people before breaking them.
- Remove architectural detail before identity.
- Make abstraction a structural transformation, not a filter.
- Treat the Robot Dreams-inspired warm, nostalgic, sunlit, slightly retro palette as the default visual identity of the Skill. Keep all four modules inside this shared emotional color universe while allowing strong, intentional slice-to-slice dominant color differences.
- Keep hidden logical ownership mathematically equal; make visible module edges irregular, designed, and readable.
- Deliver one coherent poster, never four independent images.
