# Robot Dreams-Inspired Cinematic Color System

## Contents

- Robot Dreams Shared Palette System
- Global emotional palette
- Palette families
- Saturation, contrast, and accents
- Regional palette rebalancing
- Subject-specific color
- Execution and validation

## Robot Dreams Shared Palette System

The poster is ONE photograph, and its color comes from ONE shared, limited
palette — not four independent palettes:

```text
SOURCE COLOR EVIDENCE
+
ROBOT DREAMS PALETTE FAMILIES
↓
GLOBAL PALETTE INTERPRETATION
↓
LIMITED SHARED POSTER PALETTE
```

The source photograph is **color evidence, not a literal color list**: the
final palette is NOT derived only from colors that already exist literally
in the photograph. Instead, the source's color character (its hues, warmth,
contrast relationships, dominant and supporting colors, accents) is read as
evidence and **reinterpreted through the Robot Dreams palette families**
(below) — warm foundations, air and sky, balanced greens, controlled
accents. The result is a **global palette interpretation**: one limited,
coherent set of hues for the whole poster that honors the photograph's
evidence while living fully inside the Robot Dreams-inspired world.

The deterministic pipeline applies this mapping to the whole poster via
`--paper-grade` (a color-only transform: no grain, no structure change, no
per-region tinting). The Reality Anchor and the primary head are
re-composited from the GRADED source, so they live in exactly the same
shared poster palette as every abstract region.

The color language is therefore:

- **one shared limited palette** for all four regions — the same hue family,
  the same warm/cool relationship, the same accents, the same emotional
  temperature, produced by the global palette interpretation;
- **regional palette rebalancing**: each abstraction region may shift the
  PROPORTIONS of those shared colors — a 30% region stays closest to the
  source color evidence, a 65% region groups the shared colors into broader
  masses, a 90% region narrows the proportion set toward the most essential
  shared hues. Rebalancing changes how much of each shared color appears,
  never which colors are available;
- **regional dominant color emphasis is ALLOWED, independent regional
  palette identity is NOT**: a region may lead with a subset of the shared
  colors (e.g. dusty blue + cream dominant with a terracotta accent) while
  another region leads with a different subset (e.g. ochre + warm gray
  dominant with a muted blue accent) — this is valid because every region
  still draws from the SAME shared palette. What is forbidden is a region
  introducing hues, accents, or color relationships that are not in the
  shared palette, or building its own independent palette identity.

```text
Shared Palette ≠ Same Color Distribution

ALLOWED:      regional dominant color emphasis
NOT ALLOWED:  independent regional palette identity

Region A → dusty blue + cream dominant, terracotta accent
Region B → ochre + warm gray dominant, muted blue accent
Region C → terracotta + ochre dominant, cream + dusty blue support
→ valid: all regions draw from the same shared palette

Do NOT require:
  every region has the same dominant hue
  source blue remains blue at the same proportion
  source gray remains gray, source green remains green

Do require:
  all regional colors belong to the same poster-level color universe
```

Color differences across regions are permitted as rebalancing of the shared
palette AND as regional dominant color emphasis:

- a line drawing keeps the shared hues in its strokes;
- a geometric reinterpretation keeps the shared palette inside its planes;
- shape reduction keeps shared colors in its silhouettes;
- ink wash keeps the shared color character in its washes;
- one region may be dusty-blue-led while another is ochre-led, as long as
  both only use shared-palette colors;
- and so on.

The same shared color must be treated consistently by the same method in the
same region. Never give a region its own palette identity to make the states
"readable" — readability comes from abstraction (structural information
density and Primary Method), and regional dominant color emphasis is a
rebalancing tool inside the shared palette, not a license for independent
palette identity.

## Global emotional palette

Establish one shared palette universe for the whole poster before any
abstraction. Aim for the broad emotional qualities of *Robot Dreams* — warm,
nostalgic, gentle, sunlit, slightly retro, harmonious, and dreamlike without
copying a specific frame. Keep the result stylized but not excessively
saturated.

Make all four abstraction states belong to one related emotional family — the
same warm, nostalgic, sunlit, slightly retro cinematic universe, applied
uniformly. Favor soft urban sunlight, tender melancholy, quiet optimism,
softened memory-like color, editorial dreaminess, and cinematic calm.

## Palette families

Establish ONE limited Robot Dreams-inspired palette universe for the entire
poster. Prefer these families:

- **Warm foundations:** warm cream, aged ivory, soft beige, warm sand, sunlit ochre, mustard, dusty peach, muted coral, terracotta, faded orange-red, soft brick, warm brown.
- **Air / sky:** dusty blue, powder blue, pale cyan, washed turquoise, muted teal, gray-blue, warm cloud gray.
- **Greens:** sage, dusty olive, gray-green, muted teal-green, softened blue-green.
- **Darks:** warm charcoal, dark olive, muted navy, soft brown-black.
- **Controlled accents:** tomato red, muted cherry red, coral, mustard yellow, terracotta orange, warm denim blue.

Do NOT force every color family into every photograph. Select a compact
subset that suits the source scene — the palette should feel:

```text
warm        nostalgic   gentle      sunlit
slightly faded          retro       editorial
dreamlike   calm
```

Avoid:

```text
neon cyberpunk          cold steel blue domination
purple-magenta sci-fi glow           random rainbow abstraction
fluorescent pop-art     severe HDR  commercial-ad gloss
dark horror grading     lifeless gray
```

Adapt these families to the source rather than forcing every named hue into
every image. Preserve major source color identity when it supports the shared
emotional palette.

### Default interpretation examples (source color evidence → palette families)

The source photograph's colors are EVIDENCE, reinterpreted through the
families — never copied literally. When a source region shows a color like
one below, default to its Robot Dreams-family reinterpretation (the exact
choice depends on the region's content and the poster's balance):

```text
gray asphalt        → ochre / muted terracotta / dusty blue / warm gray
digital blue sky    → dusty blue / pale cyan / aged cream / muted teal
green vegetation    → sage / dusty olive / softened blue-green / ochre-green
white concrete      → warm cream / sand / pale peach / soft gray-blue
```

These are the DEFAULT interpretation directions, not a fixed palette: the
same source evidence may lean to different family members in different
regions, as long as every choice stays inside the shared poster palette and
the four regions keep rebalancing one limited color set.

## Saturation, contrast, and accents

Keep overall saturation medium-low to medium, with selective moderate
saturation at focal areas. Soften strong-hue transitions and retain a
slightly faded cinematic quality. Keep the image alive rather than dull, but
avoid fluorescent intensity, candy oversaturation, arbitrary high-chroma
clashes, or gray mud.

Use gentle tonal contrast, readable but calm value separation, soft sunlight,
open highlights, and quiet shadows. Avoid crushed blacks, severe HDR,
aggressive commercial-poster contrast, and glossy digital sharpness.

Choose a small accent set and repeat it intentionally across the whole poster
to guide attention, reinforce focal forms, and create rhythm. Place accents
in clothing details, architectural highlights, object edges, signage
fragments, selected strokes, or color blocks. Do not scatter strong accents
everywhere — the same source accents keep the same character in every region
that contains them.

## Regional palette rebalancing

Each region's color behavior is its abstraction method applied to the shared
palette — a rebalancing of proportions AND a dominant color emphasis, never
an independent palette:

- **Reality Anchor:** source-faithful by construction. The anchor is
  composited from the (uniformly graded) source through its own zone mask, so
  it keeps the shared palette of its slice exactly. Palette unity never
  outranks face identity or human continuity.
- **30% abstraction:** closest to local photographic color. The 30%-pool
  methods (Colored Sketch, Line Abstraction, Painterly Abstraction) preserve
  much of the shared color variation while restructuring it structurally;
  their color is the shared palette drawn, lined, or brushed.
- **65% abstraction:** the 65%-pool methods (Geometric Abstraction,
  Fragmentation, Collage Abstraction) restructure form; the shared palette is
  grouped into broader masses — same colors, larger proportion chunks, and
  the region may lead with a subset of shared hues.
- **90% abstraction:** the 90%-pool methods (Shape Reduction, Chinese Ink
  Wash, Cartoon Pixel) keep only a semantic skeleton; the shared palette
  narrows to its most essential members (reduced shapes, washes, or pixel
  palette).

As abstraction rises, the same shared palette is carried through
progressively stronger structural reinterpretation and progressively narrower
proportion sets. Do not add per-region palette compression, per-region hue
shifts, or per-region saturation curves that change WHICH colors are
available — the palette is one, the abstraction (its proportion rebalancing
and dominant color emphasis) differs. Regional dominant color emphasis is
fine; regional palette identity is not.

## Cross-slice relationship

Because all regions share one limited palette, the poster is coherent by
construction: the same hues, the same highlights, the same warm grade recur
wherever the same source content recurs, rebalanced by each region's
abstraction. Use a small number of hue echoes, shared highlight logic, or
repeated accents to reinforce coherence.

Do not blend colors across boundaries to soften the seams — the paper-material
seam is the boundary's representation, and it is drawn by the pipeline. Do not
shift the palette at a boundary to "announce" a new abstraction state: the
state change is announced by the structural language, the proportion
rebalancing, and the regional dominant color emphasis — never by a color that
leaves the shared poster palette.

Apply color relationships with [intentional-modular-composition.md](intentional-modular-composition.md).

## Subject-specific color

For important people, use softened warm skin families, simplified coherent
clothing colors, and contour/color-block interplay. Avoid over-pink, dead
gray, plastic orange, or excessively vivid fashion colors that break harmony.
Preserve emotional readability over tiny local color accuracy. The primary
head is always the original (graded) photograph.

For architecture, favor sunlit beige, sand, terracotta, muted brick, soft
façade warmth, and restrained sky-reflective cools. Preserve major
architectural color identity through any abstraction method. Avoid rainbow
buildings, steel-blue domination unless source-required, or signage that
overwhelms the massing.

Use sky, street, landscape, and other environmental regions to carry airy
blues, warm reflected light, dusty sunlight, soft horizons, and gentle tonal
openness across the composition — the same shared sky color in every region
that contains it, at that region's abstraction.

## Decision priority

Color decisions inherit the global priority in `SKILL.md`; this local list
applies only after face identity, human continuity, Reality role,
architectural identity, and four-state readability are secure:

1. Protection of already-secure face, body, Reality, and architectural structure.
2. Readability of the four abstraction states (via abstraction; regional dominant color emphasis may help, independent palette identity never does).
3. Emotional warmth and one shared palette relationship.
4. Poster-level color coherence.
5. Literal local color accuracy.

There is no "independent module palette identity" item: contrast between
regions comes from their abstraction languages and from dominant color
emphasis WITHIN the shared palette — never from per-region palette
identities.

## Execution and validation

1. Read the source photograph as COLOR EVIDENCE — its hues, warmth, contrast
   relationships, dominant and supporting colors, and accents — then build
   the GLOBAL PALETTE INTERPRETATION by reinterpreting that evidence through
   the Robot Dreams palette families. Never copy the photograph's literal
   color list.
2. Keep the Reality Anchor photographic and source-faithful: the deterministic
   pipeline composites it from the (uniformly graded) source; the primary head
   is force-composited from the source on top. Optionally grade the Reality
   candidate with deterministic non-generative operations that cannot alter
   facial geometry, facial texture structure, feature placement, or identity;
   otherwise leave it unchanged.
3. Render each abstract zone from the LIMITED SHARED POSTER PALETTE — the
   method's structural language carries the shared colors, rebalancing their
   proportions per region.
4. Apply the same warm grade uniformly to the whole poster; never tint regions
   differently.
5. Repeat a small, controlled accent set consistently wherever the same source
   content recurs.

Before delivery, confirm that the poster reads as ONE photograph whose four
regions differ only by abstraction: the anchor is the (graded) source; the
30%, 65%, and 90% regions reinterpret their own slice of the SAME limited
shared poster palette (built from source color evidence through the Robot
Dreams palette families), rebalancing its proportions and allowing each
region a dominant color emphasis — but no region has been given its own
independent palette identity, hue set, or color universe.
