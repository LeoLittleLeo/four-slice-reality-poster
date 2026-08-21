# Abstraction Language and Calibration

## Contents

* Structural abstraction
* Method diversity and dominant language
* Ten approved methods
* Component reduction
* Level calibration
* Content-aware selection

## Structural abstraction

Make abstraction an actual reinterpretation of form, structure, space, or visual information. Blur, grading, hue shift, saturation, contrast, grain, vignette, exposure, duotone, and presets alone do not count.

Treat the following as three independent dimensions:

```text
SOURCE OWNERSHIP
= which part of the source image may be represented

PRIMARY ABSTRACTION METHOD
= how that source content is reinterpreted

ABSTRACTION LEVEL
= how far the reinterpretation departs from photographic representation
```

Do not confuse these dimensions.

A change in abstraction method does not grant permission to import source content from another logical zone.

A higher abstraction level does not grant permission to duplicate, restart, or relocate recognizable source content from another logical zone.

Abstraction must operate primarily on the source content owned by the current logical zone.

## Shared Material System, Distinct Methods

When using Layered Collage Composition (`--boundary collage`), the three
abstract states share **one material SYSTEM** — the editorial print / paper /
grain / warm Robot Dreams palette / torn-edge finish that the deterministic
pipeline applies uniformly. This is what makes the poster read as one physical
object instead of four unrelated filters.

Sharing the material system does NOT allow sharing the abstraction METHOD.
The three abstract states MUST use three **different Primary Abstraction
Methods**:

```text
30% Primary Method ≠ 65% Primary Method ≠ 90% Primary Method  (HARD REQUIREMENT)
```

Differentiate the three states through BOTH:

* a distinct Primary Abstraction Method per state (line, sketch, painterly,
  geometric, fragmentation, collage, shape reduction, ink wash, cartoon
  pixel, ...); and
* structural information density / component omission / shape merging / edge
  simplification / surface-detail reduction / spatial compression / graphic
  massing / representational distance.

```text
LEVEL ≠ MEDIUM
```

Under the Level-Gated system a method IS bound to a level: each method
belongs to exactly one level's pool (30% can never use ink wash, 90% can
never use painterly — those methods live in other pools). What LEVEL ≠
MEDIUM means now is that a level does not prescribe ONE fixed method: it
prescribes an eligible pool, and the region picks one method inside that
pool. The three chosen methods must be distinct, and each must come from
its own level's pool. For example:

```text
GOOD (each region's method comes from its own level's pool)

30% = Colored Sketch (30% pool)
65% = Fragmentation (65% pool)
90% = Shape Reduction (90% pool)
```

```text
BAD (same material system AND same method at three intensities)

30% = Color Blocking + light detail
65% = Color Blocking + medium simplification
90% = Color Blocking + large simplified masses
```

```text
BAD (unrelated mediums with no shared system)

30 pencil + 65 low-poly + 90 watercolor
```

All methods stay inside the shared editorial print / paper / warm palette
system — distinct structurally, unified materially.

## Level-Gated Primary Abstraction Method System

```text
LEVEL DETERMINES ELIGIBLE METHOD FAMILY.
CONTENT DETERMINES METHOD SELECTION.
COLOR MODULATES THE SELECTION.
```

## Core principle

Do not select the three Primary Abstraction Methods from one unrestricted global pool.

Instead, bind each abstraction level to its own **non-overlapping Primary Method Pool** (a method family).

The abstraction level determines which Primary Methods are eligible.

The local source region then determines which eligible method is most appropriate.

```text
ABSTRACTION LEVEL
→ determines the eligible Primary Method FAMILY (the pool)

LOCAL REGION CONTENT
→ selects the Primary Method inside that family

LOCAL COLOR CHARACTER
→ modulates (refines or breaks ties in) the selection
```

### Disjointness invariant

The three pools MUST be pairwise disjoint — no method is eligible at more
than one abstraction level:

```text
30% Primary Method Pool
∩
65% Primary Method Pool
∩
90% Primary Method Pool
=
∅
```

Because the pools are disjoint, choosing one Primary Method from each level's
pool AUTOMATICALLY satisfies `30% ≠ 65% ≠ 90%` — the methods are distinct by
construction, never by review.

### Pools are sets, not singletons

The disjointness requirement is HARD, but it must NOT be satisfied by
permanently pinning one fixed method to each abstraction level.

A pool is a SET of eligible methods with genuine alternatives — the same
abstraction level must remain capable of producing DIFFERENT visual languages
across different source photographs:

```text
NEVER:  30% = Colored Sketch (always)   ← singleton, level locked to one language
        65% = Geometric Abstraction (always)
        90% = Fragmentation (always)

DO:     30% may be Colored Sketch on one photo, Painterly Abstraction on
        another, Line Abstraction on a third — whichever the region character
        selects, from the 30% pool only.
```

The level gates WHICH methods are eligible; the region character decides
which one is used. Every pool therefore contains at least two eligible
methods, so each level keeps visual variety across photographs.

### Default pools (nine of the ten approved methods, each in exactly one pool)

| Abstraction level | Eligible Primary Method Pool | Why |
|---|---|---|
| **30%** | 1. Colored Sketch, 2. Line Abstraction, 3. Painterly Abstraction | structure-preserving; keep ~70% source recognition and high spatial fidelity |
| **65%** | 1. Geometric Abstraction, 2. Fragmentation, 3. Collage Abstraction | substantial restructuring while staying traceable (~35% recognition) |
| **90%** | 1. Shape Reduction, 2. Chinese Ink Wash, 3. Cartoon Pixel | semantic-skeleton / strongly reinterpreted representation |

**Color Blocking belongs to NO Primary pool.** It is a Supporting-only
method: it may support any Primary Method (simplifying tones, organizing
masses) but is never selected as a Primary Abstraction Method at any level.

These pools are the default. Moving a method between pools, or adding a
method, requires explicit user direction. Within a pool, choose the method by
the region's color, structural, and subject character (see Content-aware
selection below).

```text
LEVEL ≠ MEDIUM:
a level does not prescribe a fixed method, it prescribes an eligible pool;
the region character picks the method inside that pool.
```

### Deterministic router in the script (hard rule, not agent discretion)

The pool gate is enforced by `scripts/slice_and_compose.py`, not left to the
agent:

* `--mode prepare` routes the Primary Method per level through these pools
  and writes it into the manifest (top-level `methods`, plus each zone's
  `primary_method`; the anchor zone is `Reality`). Default: a deterministic
  auto pick per pool from the source+seed hash — the same photo + seed always
  repeats exactly, and different photos get different methods per level
  (pools stay sets, never singletons).
* `--methods "30:Colored Sketch,65:Fragmentation,90:Shape Reduction"`
  overrides the pick for content-aware selection. The script **refuses** a
  method that is not in ITS level's pool (e.g. Chinese Ink Wash at 65%), and
  **refuses** Color Blocking as a Primary Method — the level gates the pool
  first, then the region's subject/structure/color picks inside that pool.
* `--mode verify` re-checks every recorded zone method against its level's
  pool (a stale manifest without method routing only warns, keeping old
  workdirs working).

## Method diversity and dominant language

The three abstract modules must not only differ in abstraction level; they must also differ clearly in their dominant abstraction language.

For each abstract module:

1. select exactly one **Primary Abstraction Method**;
2. optionally select up to two **Supporting Methods**;
3. make the Primary Method perceptually dominant in the final appearance; and
4. prevent Supporting Methods from visually overriding the Primary Method.

Across the 30%, 65%, and 90% abstraction modules, prefer three perceptually distinct Primary Abstraction Methods.

Do not solve abstraction diversity merely through different palettes, textures, brush styles, or different amounts of the same visual treatment.

Method diversity does not override source-content ownership.

### Primary-method diversity rule

**Required (hard):**

```text
30% Primary Method ≠ 65% Primary Method ≠ 90% Primary Method
```

This is guaranteed BY CONSTRUCTION through the Level-Gated system: the three
levels draw from three pairwise-disjoint Primary Method Pools, so repetition
across levels is structurally impossible. Each level selects exactly one
Primary Method from ITS OWN pool (see Level-Gated Primary Abstraction Method
System above).

If the available alternatives in a pool are unsuitable for the region,
re-select from that same pool — never borrow a method from another level's
pool.

For example:

```text
GOOD

30% → Painterly Abstraction (30% pool)
65% → Collage Abstraction (65% pool)
90% → Cartoon Pixel (90% pool)
```

```text
GOOD

30% → Line Abstraction
65% → Fragmentation
90% → Shape Reduction
```

Avoid:

```text
30% → Color Blocking + light detail
65% → Color Blocking + medium simplification
90% → Color Blocking + large simplified masses
```

This is merely one abstraction language at three intensities and does not provide sufficient four-state diversity.

### Anti-convergence rule

Do not let all abstraction methods converge visually toward broad filled color regions.

In particular:

* Line Abstraction should remain recognizably line-driven.
* Colored Sketch should retain visible hand-drawn stroke language.
* Painterly Abstraction should remain brush- or paint-mass-driven.
* Geometric Abstraction should remain plane-, facet-, or geometry-driven.
* Fragmentation should remain splitting-, displacement-, separation-, or reconstruction-driven.
* Collage Abstraction should remain cropping-, layering-, masking-, and recomposition-driven.
* Shape Reduction should remain silhouette-, symbol-, or simplified-form-driven.
* Chinese Ink Wash should remain ink-, wash-, and brush-driven — tonal gradation (浓淡干湿), bleed, paper, and negative space — not generic gray color blocks or a grayscale filter.
* Cartoon Pixel should remain pixel-grid- and cartoon-shape-driven — not a downsampled, pixelated, or blurred copy of the photograph.

A module fails method separation when its nominal method is only detectable in the prompt but the visible result is primarily generic color blocking.

A module also fails method separation when visual diversity is achieved by cloning recognizable source content into multiple modules.

## Ten approved methods

### 1. Line Abstraction

Reduce detail to contour, structural, architectural, perspective, and directional lines.

At stronger abstraction levels, detach, overlap, extend, interrupt, or simplify lines while preserving important structure and directional logic.

Line Abstraction should remain visibly line-driven.

Do not allow filled color masses to replace the structural role of the lines.

Use supporting color only when it reinforces rather than overrides the line language.

Operate only on source content owned by the current logical zone.

### 2. Colored Sketch

Reinterpret source content with colored pencil, crayon, pastel, marker, ink, or hand-drawn architectural strokes.

Use color as part of the drawing language.

Do not default to plain graphite unless the source or user direction clearly supports monochrome treatment.

Preserve visible stroke character, hand-drawn irregularity, and drawing structure.

Do not reduce Colored Sketch into smooth flat color regions with a few decorative lines placed on top.

Operate only on source content owned by the current logical zone.

### 3. Painterly Abstraction

Replace photographic detail with watercolor, gouache, oil-like, acrylic-like, thick-paint, dry-brush, wash, or expressive brush structures.

At lower abstraction levels, preserve more source geometry, object placement, and spatial structure.

At stronger abstraction levels, allow brush gesture, paint masses, edge loss, and painterly reconstruction to dominate.

Painterly Abstraction should remain visibly driven by brush or paint behavior rather than generic posterized color blocks.

Operate only on source content owned by the current logical zone.

### 4. Color Blocking

Compress continuous tones, textures, shadows, and gradients into fewer broad color regions when broad color organization is genuinely useful to the source structure.

Treat Color Blocking primarily as a **Supporting Abstraction Method**, not as the universal default representation of abstraction.

By default, Color Blocking should support another Primary Method by simplifying tonal or chromatic information without replacing that method's defining visual structure.

For example:

* support Colored Sketch by simplifying background tonal regions;
* support Painterly Abstraction by organizing large underlying color masses;
* support Geometric Abstraction by simplifying plane colors;
* support Shape Reduction by clarifying silhouettes and major masses.

Do not automatically translate higher abstraction into larger, flatter, or fewer color blocks.

Color Blocking is **Supporting-only** under the Level-Gated system: it
belongs to NO Primary pool and has NO Primary eligibility at any level
(30%, 65%, or 90%). It may become a Primary Method ONLY when the user
explicitly overrides the default method-pool system. Without that
override, never select it as a Primary Method — even when the source image
contains strong naturally occurring graphic color structures such as:

* large façades;
* strong shadow fields;
* sky-ground divisions;
* signage;
* clothing masses;
* water reflections;
* strong architectural planes; or
* similarly dominant chromatic structures.

Those structures are exactly when Color Blocking works best as a
SUPPORTING method beneath a Primary Method, not as the Primary Method
itself.

Avoid generic posterized regions that erase the perceptual identity of the selected Primary Method.

Operate only on source content owned by the current logical zone.

### 5. Geometric Abstraction

Derive planes, polygons, facets, rectangles, triangles, volumes, or spatial structures from source silhouettes, massing, perspective, architectural rhythm, or object geometry.

Geometry must remain source-derived.

Avoid unrelated random polygons, decorative geometry with no source basis, or generic low-poly treatment applied indiscriminately.

At stronger abstraction levels, geometry may simplify or restructure source forms substantially while preserving enough source DNA for semantic recognition.

Do not import recognizable geometry or structures from another logical zone.

### 6. Fragmentation

Deliberately split, offset, rotate, displace, overlap, reorder, separate, crop, or partially remove source elements **within the current module's owned source content**.

Fragmentation may divide one source form into several visible fragments, but those fragments must continue to read as parts of one reconstructed source subject rather than multiple independent copies.

Do not clone recognizable source regions across modules.

Do not use repetition of complete people, faces, buildings, landmarks, vehicles, crowd groups, skyline sections, or other recognizable source structures as a fragmentation device.

Small non-semantic repetitions such as strokes, texture marks, micro-fragments, line segments, or decorative motifs are permitted when they do not create another readable instance of the source object.

Local displacement is allowed, but do not displace a recognizable structure so far that it reads as a second independent object or appears to belong to another logical zone.

Make reconstruction intentional, never like broken masking, accidental duplication, bad compositing, or generation artifacts.

### 7. Collage Abstraction

Recompose source-derived photographic and illustrated material owned by the current module through:

* moving;
* scaling;
* isolating;
* cropping;
* masking;
* overlapping;
* partial occlusion; or
* re-layering.

Do not duplicate recognizable source objects or substantial source regions across modules.

Do not create multiple independent copies of a complete:

* person;
* face;
* building;
* landmark feature;
* crowd cluster;
* vehicle;
* skyline section;
* roofline section;
* major tree cluster; or
* other scene-defining structure.

Repetition may be used only for non-semantic micro-elements such as texture fragments, tiny marks, strokes, small architectural rhythms, paper-like fragments, or decorative motifs when the repetition does not create a second readable copy of the source subject.

Collage recomposition may alter local layering and spatial hierarchy, but it must preserve source provenance.

Make the result editorial and designed rather than resembling accidental cutout duplication.

### 8. Shape Reduction

Reduce people, buildings, vegetation, objects, or other structures through simplified forms, silhouettes, broad masses, symbols, or characteristic outlines.

Do not confuse simplification with blur.

Preserve the minimum semantic evidence necessary for the source structure to remain understandable.

For people, preserve pose, body relationship, and identity-critical structure according to protected-subject rules.

For architecture, preserve landmark silhouette, massing, perspective cues, or characteristic structural rhythm when those features carry identity.

At stronger abstraction levels, reduce internal details before removing scene-defining outer structure.

Operate only on source content owned by the current logical zone.

### 9. Chinese Ink Wash (水墨)

Reinterpret the owned source content through the language of Chinese ink-wash painting: brush-drawn structure, ink tonal gradation (焦浓重淡清 — burnt, thick, heavy, light, and clear ink), wet/dry brush contrast, wash bleed and paper absorption, soft edge loss, and deliberate negative space (留白). It is a brush- and ink-driven painting language — never a grayscale filter, a duotone preset, or generic gray color blocking.

Default treatment:

* Keep warm paper tone and restrained color washes (浅绛 light-ochre or 淡彩 pale washes) so the module stays inside the shared warm, nostalgic, sunlit, slightly retro cinematic universe.
* True monochrome ink (pure ink on paper white) is a deliberate stylistic choice and requires user direction.
* Do not drift into lifeless gray, cold steel monochrome, or muddy neutral washes.

Level behavior (90% pool only):

* Chinese Ink Wash is eligible at **90% only** under the default pools — it
  is never selected at 30% or 65%.
* At 90%: 写意 skeleton — minimal brush strokes, dominant 留白, sparse ink
  accents, retaining only the essential source silhouette, massing, or
  directional structure.

Rules:

* Ink structure must derive from the owned source content (silhouette, massing, landscape rhythm, architecture structure) — never decorative generic mountains, pines, or stock ink motifs.
* Preserve the semantic skeleton of the source so the module stays traceable to this photograph.
* Do not import or clone recognizable source content from another logical zone.
* Operate only on source content owned by the current logical zone.

### 10. Cartoon Pixel (卡通像素)

Reinterpret the owned source content as pixel-art-driven cartoon rendering: a visible pixel grid, a limited pixel palette, bold cartoon outlines, simplified flat shapes, and optional dithering. The module must be **rebuilt as a pixel composition** — never a downsampled, pixelated, or blurred copy of the photograph.

Level behavior (90% pool only):

* Cartoon Pixel is eligible at **90% only** under the default pools — it
  is never selected at 30% or 65%.
* At 90%: minimal pixel iconography — strongly reduced pixel shapes,
  symbols, and silhouettes while retaining the source's semantic skeleton
  (pose, skyline, roofline, massing, or characteristic outline).

Rules:

* Pixelation must be structural: rebuild the composition at a lower pixel resolution with intentional pixel-shape logic and a restricted palette. A pixelate filter applied to the photograph is not abstraction.
* Keep the pixel palette muted and inside the Robot Dreams-inspired family by default; avoid neon or candy saturation unless the user directs it.
* Cartoon outlines must follow the owned source content.
* Do not import or clone recognizable source content from another logical zone.
* Operate only on source content owned by the current logical zone.

## Component reduction

Within abstract modules, use controlled component reduction when it improves abstraction clarity, compositional readability, or poster design.

Reduce, merge, group, compress, or selectively omit non-essential repeated elements instead of preserving every component one to one.

Apply this especially to:

* dense trees and foliage;
* repetitive background buildings;
* repeated windows, balconies, columns, and façade details;
* dense groups of secondary people;
* repeated street furniture;
* small incidental vehicles;
* minor objects;
* signage fragments; and
* street clutter.

Prefer:

* density reduction;
* grouping;
* silhouette simplification;
* massing compression;
* rhythm compression; and
* selective omission of repetitive detail.

Component reduction applies only to source content owned by the current module.

Do not compensate for removed components by importing similar components from another logical zone.

Preserve enough evidence for the source scene to remain semantically identifiable.

Never remove or weaken:

* the primary person;
* the identity-critical face;
* the dominant crowd event when crowd activity is the main subject;
* landmark or primary architecture;
* identity-critical architectural features; or
* major compositional masses that define the scene.

The goal is controlled visual simplification, not full deletion.

Reduce secondary density before altering a protected subject or scene-defining structure.

Component reduction must reduce content rather than create duplicated replacements.

## Level calibration

The three abstraction levels must differ perceptually in structural information density, not merely in palette, brush texture, rendering style, or medium.

Calibrate every abstract module across all five dimensions:

* detail retention;
* component density;
* spatial fidelity;
* shape fidelity; and
* photographic surface retention.

At least one major difference between every pair of abstract modules must come from structural information density.

If 30%, 65%, and 90% could be mistaken for the same abstraction level with only a color, texture, or medium change, reject the result and rebuild the modules.

Abstraction level changes **how much information is retained**.

It does not change source ownership.

### 30% abstraction

Keep the module immediately recognizable: approximately 70% source recognition and 30% reinterpretation.

Preserve:

* most major components;
* most secondary components;
* substantial photographic surface;
* original spatial relationships;
* strong major-shape fidelity; and
* broad source object placement.

Only lightly reduce repetitive elements.

Artistic intervention should be clearly visible but remain partial.

A filtered photograph is insufficient, but the module must retain the highest structural information density of the three abstract states.

The selected Primary Abstraction Method must already be perceptible.

Do not import recognizable source structures from neighboring logical zones to enrich the module.

### 65% abstraction

Keep the source semantically traceable: approximately 35% recognition and 65% reinterpretation.

Remove or merge a substantial amount of secondary components, significantly reduce photographic surface, simplify major forms, and permit visible spatial reconstruction.

The 65% module should be structurally transformed through its selected Primary Abstraction Method rather than merely simplified into larger color regions.

Depending on the selected Primary Method (chosen from the 65% pool —
Geometric Abstraction, Fragmentation, or Collage Abstraction), emphasize
one or more of:

* source-derived geometric planes;
* controlled fragmentation; or
* collage recomposition.

Color masses may support the transformation but should not automatically dominate it.

Spatial reconstruction must remain derived from source content owned by the current logical zone.

Do not import or duplicate recognizable content from another logical zone merely to increase abstraction complexity.

Shape fidelity and spatial fidelity must be visibly lower than 30% while the scene remains clearly derived from the source.

### 90% abstraction

Retain only the semantic skeleton of the source and allow artistic reconstruction to dominate.

Aggressively reduce component count, eliminate most photographic texture and secondary detail, and permit major spatial and shape reconstruction.

High abstraction does not inherently mean large flat color blocks.

Express the semantic skeleton through the selected Primary Abstraction Method.

Depending on that method (chosen from the 90% pool — Shape Reduction,
Chinese Ink Wash, or Cartoon Pixel), the result may consist primarily of:

* silhouettes;
* symbols;
* highly reduced shapes;
* ink-wash strokes with dominant negative space; or
* minimal pixel-art iconography.

Preserve only enough source DNA for recognition, such as:

* pose;
* dominant crowd event;
* skyline;
* roofline;
* architectural massing;
* dominant directional structure;
* landmark outline;
* perspective direction;
* characteristic silhouette; or
* restrained source-derived color relationships.

Major reconstruction does not permit cross-module source duplication.

The module may radically reinterpret its owned source content, but it must not import, restart, or clone recognizable source structures owned by another logical zone.

Do not substitute unrelated abstract art.

Do not assume that abstraction strength should increase monotonically with color-block size, flatness, or visual emptiness.

### Level is not method

Do not map abstraction percentage to a fixed visual language.

In particular, never assume:

```text
lower abstraction → more photographic
higher abstraction → progressively larger flat color blocks
```

Abstraction level controls **how much structural information is retained**.

Primary Abstraction Method controls **how the remaining information is represented**.

Source ownership controls **which part of the original image may be represented**.

These are independent dimensions.

Therefore a 90% abstraction (using a method from the 90% pool — Shape
Reduction, Chinese Ink Wash, or Cartoon Pixel) may be:

* reduced silhouettes or symbols;
* ink-wash strokes with dominant negative space;
* minimal pixel-art iconography; or
* another 90%-pool method's structural language.

It does not need to contain broad filled color regions.

Likewise, a 30% abstraction may use Color Blocking as a SUPPORTING method
when appropriate, without making Color Blocking the default pathway toward
stronger abstraction — Color Blocking is never a Primary Method by default.

Changing abstraction level or method never grants permission to duplicate or import recognizable source content from another logical zone.

## Content-aware selection

Choose the Primary Abstraction Method from the semantic and structural character of each module — **inside that level's eligible Primary Method Pool** (see Level-Gated Primary Abstraction Method System above). The level already narrowed the family; the region's content decides which member of the family is used, and local color character modulates (refines or breaks ties in) that choice.

Do not repeatedly select the easiest universally applicable method.

Method diversity across the three abstract modules is an explicit design objective.

Method selection must occur **after source ownership is understood**.

Do not search the entire image for content that better suits a selected abstraction method and then move that content into another module.

Use this order:

```text
1. determine source ownership
2. inspect the content owned by each abstract module
3. choose an appropriate Primary Abstraction Method
4. choose optional Supporting Methods
5. apply the assigned abstraction level
```

Never use this order:

```text
choose a desired abstraction method
→ search the whole source image for a suitable object
→ copy or move that object into the module
```

### Human-dominant modules

The level gates the pool FIRST; the subject character then selects inside
that pool:

* **30% pool** (Colored Sketch, Line Abstraction, Painterly Abstraction):
  prefer contour-focused Line Abstraction, Painterly Abstraction, or
  Colored Sketch when clothing, pose, or gesture supports it.
* **65% pool** (Geometric Abstraction, Fragmentation, Collage Abstraction):
  prefer Fragmentation when identity-critical anatomy remains protected.
  Use Geometric Abstraction selectively and mainly on clothing, massing,
  or background structure rather than on faces or anatomy.
* **90% pool** (Shape Reduction, Chinese Ink Wash, Cartoon Pixel): prefer
  Shape Reduction for pose-preserving silhouettes; Chinese Ink Wash for a
  写意 symbolic figure; Cartoon Pixel for a flat, iconic figure.

Color Blocking is Supporting-only and may be used as support for:

* clothing masses;
* background separation;
* silhouettes;
* light-shadow organization; or
* tonal compression.

Color Blocking is never a Primary Method (Supporting-only) — do not use it
as the automatic Primary Method.

Preserve primary-face identity and coherent human anatomy regardless of abstraction method.

Do not duplicate a person, face, limb, body segment, or pose into another module.

When a person physically spans multiple logical zones, render one continuous person whose corresponding portions change abstraction language across the zones.

Do not restart the complete person independently inside each module.

### Architecture-dominant modules

The level gates the pool FIRST; the architectural character then selects
inside that pool:

* **30% pool** (Colored Sketch, Line Abstraction, Painterly Abstraction):
  structural drawing (Line Abstraction), colored architectural sketch
  (Colored Sketch), or painterly massing (Painterly Abstraction).
* **65% pool** (Geometric Abstraction, Fragmentation, Collage Abstraction):
  plane extraction (Geometric Abstraction), controlled deconstruction
  (Fragmentation), or collage reconstruction (Collage Abstraction).
* **90% pool** (Shape Reduction, Chinese Ink Wash, Cartoon Pixel): landmark
  silhouette and massing (Shape Reduction), ink-wash architectural
  atmosphere (Chinese Ink Wash), or flat pixel architecture (Cartoon
  Pixel).

Architecture is especially suitable for variation between:

* structural drawing;
* colored architectural sketch;
* plane extraction;
* controlled deconstruction;
* collage reconstruction; and
* painterly massing.

Do not default architecture to broad flat façade color blocks when line structure, perspective, roofline, repeated façade rhythm, landmark geometry, or massing could provide a more distinctive abstraction language.

Color Blocking is Supporting-only: use it as tonal/chromatic organization
beneath the Primary Method. Strong graphic chromatic fields in the source
architecture do NOT make Color Blocking eligible as a Primary Method.

When one building spans multiple logical zones, each module may reinterpret only its corresponding source portion.

Preserve enough silhouette, massing, perspective, roofline, or structural rhythm for the building to read as one continuous subject.

Never regenerate the complete building separately in multiple modules.

### Landscape and environment modules

The level gates the pool FIRST; the environmental character then selects
inside that pool:

* **30% pool** (Colored Sketch, Line Abstraction, Painterly Abstraction):
  Painterly Abstraction, Line Abstraction, or Colored Sketch.
* **65% pool** (Geometric Abstraction, Fragmentation, Collage Abstraction):
  geometric or spatial-plane abstraction, Fragmentation, or Collage when
  the scene genuinely supports reconstruction.
* **90% pool** (Shape Reduction, Chinese Ink Wash, Cartoon Pixel): Shape
  Reduction, or Chinese Ink Wash for atmospheric, poetic renderings.

Color Blocking (Supporting-only) may organize:

* sky;
* ground;
* vegetation;
* shadows;
* water;
* atmospheric regions; or
* broad natural planes.

It is never the Primary Method and must not become the visible identity of
the module.

For dense foliage, clouds, crowds, street clutter, repetitive buildings, or repeated environmental detail, combine Component Reduction with the selected Primary Method instead of reducing everything into generic flat blobs.

Do not duplicate an entire tree cluster, skyline, road section, cloud formation, building row, or other recognizable environmental region into another module.

### Fit of the newer methods

Chinese Ink Wash suits landscape, atmospheric, architectural, and poetic modules; it also works for people when a 写意 silhouette or symbolic figure strengthens the module. It is in the **90% pool** only.

Cartoon Pixel suits people, urban scenes, architecture, and objects; it reads strongest at 90%. It is in the **90% pool** only.

Choose either like any other method — from its level's pool, by the owned content and the module's desired perceptual mechanism. Both methods still operate only on source content owned by their logical zone.

### Cross-module selection rule

After selecting methods for all three abstract modules, inspect the set together.

Reject and reselect methods when:

* two or more modules are visually dominated by generic broad color masses;
* all three modules rely on essentially the same simplification mechanism;
* nominally different methods produce nearly identical silhouettes and filled regions;
* the difference between modules comes mainly from palette rather than structural language;
* increasing abstraction merely produces progressively larger and flatter shapes;
* abstraction diversity is achieved by repeating or cloning recognizable source content across modules;
* a module imports a major source object or scene region owned by another logical zone;
* a continuous subject restarts independently in more than one module; or
* source provenance becomes unclear because spatial reconstruction has moved recognizable structures into the wrong ownership region.

Prefer combinations with visibly different perceptual mechanisms.

For example:

```text
30% → Colored Sketch (30% pool)
65% → Fragmentation (65% pool)
90% → Shape Reduction (90% pool)
```

or:

```text
30% → Line Abstraction (30% pool)
65% → Collage Abstraction (65% pool)
90% → Cartoon Pixel (90% pool)
```

or:

```text
30% → Painterly Abstraction (30% pool)
65% → Geometric Abstraction (65% pool)
90% → Chinese Ink Wash (90% pool)
```

These examples illustrate method diversity only.

The POOL is bound to the level; the method is chosen inside that pool.
Never lock a level to one fixed method (singleton), and never borrow a
method from another level's pool.

Each method must still operate primarily on the source content owned by its logical zone.

Final invariant:

```text
DIFFERENT SOURCE PORTIONS
+
DIFFERENT PRIMARY ABSTRACTION LANGUAGES
+
DIFFERENT ABSTRACTION LEVELS
=
ONE COHERENT FOUR-STATE IMAGE
```

Never interpret the four modules as four alternative renderings of the same full source scene.
