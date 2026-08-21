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
SOURCE PHOTO
↓
GLOBAL ROBOT-DREAMS PALETTE MAPPING
↓
shared limited palette
↓
each abstraction region may rebalance
the proportions of those shared colors
↓
ONE coherent poster
```

The shared palette is derived from the source photograph's own colors under
the uniform warm Robot Dreams-inspired grade (the deterministic pipeline
applies this mapping to the whole poster via `--paper-grade`, a color-only
transform: no grain, no structure change, no per-region tinting). The
Reality Anchor and the primary head are re-composited from the GRADED
source, so they live in exactly the same shared palette as every abstract
region.

The color language is therefore:

- **one shared limited palette** for all four regions — the same hue family,
  the same warm/cool relationship, the same accents, the same emotional
  temperature;
- **regional palette rebalancing**: each abstraction region may shift the
  PROPORTIONS of those shared colors — a 30% region stays close to the
  source's local color distribution, a 65% region groups the shared colors
  into broader masses, a 90% region narrows the proportion set toward the
  most essential shared hues. Rebalancing changes how much of each shared
  color appears, never which colors are available;
- **no palette identity per region**: a region must never introduce a hue,
  accent, or color relationship that is not in the shared palette, and never
  assign itself a distinct dominant-hue role that breaks the shared
  relationship.

Color differences across regions are permitted only as rebalancing of the
shared palette:

- a line drawing keeps the shared hues in its strokes;
- a geometric reinterpretation keeps the shared palette inside its planes;
- shape reduction keeps shared colors in its silhouettes;
- ink wash keeps the shared color character in its washes;
- and so on.

The same shared color must be treated consistently by the same method in the
same region. Never assign a different palette, dominant hue, or color role to
a region to make the states "readable" — readability comes from abstraction
(structural information density and Primary Method), not from giving regions
different color identities.

## Global emotional palette

Establish one shared palette universe for the whole poster before any
abstraction. Aim for the broad emotional qualities of *Robot Dreams*—warm,
nostalgic, gentle, sunlit, slightly retro, harmonious, and dreamlike without
copying a specific frame. Keep the result stylized but not excessively
saturated.

Make all four abstraction states belong to one related emotional family — the
same warm, nostalgic, sunlit, slightly retro cinematic universe, applied
uniformly. Favor soft urban sunlight, tender melancholy, quiet optimism,
softened memory-like color, editorial dreaminess, and cinematic calm. Avoid
harsh, metallic, coldly futuristic, neon, horror-like, blockbuster-contrast,
or random pop-art moods unless explicitly requested.

## Palette families

Build the shared palette primarily from:

- **Warm foundations:** warm beige, cream, dusty peach, muted coral, warm sand, soft terracotta, sunlit ochre, warm light brown, soft brick, and faded orange-red.
- **Air and sky:** powder blue, dusty sky blue, pale cyan, washed turquoise, muted teal, and soft cloud gray-blue. Keep these airy rather than digital.
- **Balanced greens:** sage, dusty olive, gray-green, muted teal-green, and softened blue-green. Avoid acidic green unless justified by the source.
- **Controlled accents:** tomato or muted cherry red, mustard yellow, coral, muted navy, warm denim blue, and terracotta red-orange.

Adapt these families to the source rather than forcing every named hue into
every image. Preserve major source color identity when it supports the shared
emotional palette.

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
palette — a rebalancing of proportions, nothing more:

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
  grouped into broader masses — same colors, larger proportion chunks.
- **90% abstraction:** the 90%-pool methods (Shape Reduction, Chinese Ink
  Wash, Cartoon Pixel) keep only a semantic skeleton; the shared palette
  narrows to its most essential members (reduced shapes, washes, or pixel
  palette).

As abstraction rises, the same shared palette is carried through
progressively stronger structural reinterpretation and progressively narrower
proportion sets. Do not add per-region palette compression, per-region hue
shifts, or per-region saturation curves that change WHICH colors are
available — the palette is one, the abstraction (and its proportion
rebalancing) differs.

## Cross-slice relationship

Because all regions share one limited palette, the poster is coherent by
construction: the same hues, the same highlights, the same warm grade recur
wherever the same source content recurs, rebalanced by each region's
abstraction. Use a small number of hue echoes, shared highlight logic, or
repeated accents to reinforce coherence.

Do not blend colors across boundaries to soften the seams — the paper-material
seam is the boundary's representation, and it is drawn by the pipeline. Do not
shift the palette at a boundary to "announce" a new abstraction state: the
state change is announced by the structural language and the proportion
rebalancing, not by a new color identity.

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
2. Readability of the four abstraction states (via abstraction, not color roles).
3. Emotional warmth and one shared palette relationship.
4. Poster-level color coherence.
5. Literal local color accuracy.

There is no "module-to-module color contrast" item: contrast between regions
comes from their abstraction languages, never from per-region color roles.

## Execution and validation

1. Establish the global palette mood.
2. Keep the Reality Anchor photographic and source-faithful: the deterministic
   pipeline composites it from the (uniformly graded) source; the primary head
   is force-composited from the source on top. Optionally grade the Reality
   candidate with deterministic non-generative operations that cannot alter
   facial geometry, facial texture structure, feature placement, or identity;
   otherwise leave it unchanged.
3. Render each abstract zone from the SHARED palette — the method's structural
   language carries the shared colors, rebalancing their proportions per
   region.
4. Apply the same warm grade uniformly to the whole poster; never tint regions
   differently.
5. Repeat a small, controlled accent set consistently wherever the same source
   content recurs.

Before delivery, confirm that the poster reads as ONE photograph whose four
regions differ only by abstraction: the anchor is the (graded) source; the
30%, 65%, and 90% regions reinterpret their own slice of the SAME shared
palette, rebalancing its proportions; saturation and contrast remain
controlled; accents are intentional; and no region has been given its own
palette, hue role, or color identity.
