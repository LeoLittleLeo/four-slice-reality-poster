# Robot Dreams-Inspired Cinematic Color System

## Contents

- One-photo color identity
- Global emotional palette
- Palette families
- Saturation, contrast, and accents
- Color behavior follows abstraction, never per-region roles
- Subject-specific color
- Execution and validation

## One-photo color identity

The poster is ONE photograph. All four regions share ONE photographic color
identity: the color of a region is the source photograph's color, passed
through that region's abstraction method. Regions differ ONLY by abstraction
— there are no per-region color roles, no module-level recolorings, no
"distinct but related color emphasis" per slice, and no abrupt palette shifts
announcing a new state.

Color differences across regions are permitted only as a by-product of the
abstraction of the source color:

- a line drawing keeps the source hues in its strokes;
- a geometric reinterpretation keeps the source palette inside its planes;
- shape reduction keeps source-derived colors in its silhouettes;
- ink wash keeps the source's color character in its washes;
- and so on.

The same source color must be treated consistently by the same method in the
same region. The deterministic pipeline applies ONE uniform warm
Robot Dreams-inspired grade to the whole poster (`--paper-grade`, a color-only
transform: no grain, no structure change, no per-region tinting). The Reality
Anchor and the primary head are re-composited from the GRADED source, so they
share the same color identity as every abstract region.

Never assign a different palette, dominant hue, or color role to a region to
make the states "readable". Readability of the four states comes from
abstraction (structural information density and Primary Method), not from
color roles.

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

Build the palette primarily from:

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

## Color behavior follows abstraction, never per-region roles

Each region's color behavior is its abstraction method applied to the source
color — nothing more:

- **Reality Anchor:** source-faithful by construction. The anchor is
  composited from the (uniformly graded) source through its own zone mask, so
  it keeps the photographic color of its slice exactly. Palette unity never
  outranks face identity or human continuity.
- **30% abstraction:** closest to local photographic color. The 30%-pool
  methods (Colored Sketch, Line Abstraction, Painterly Abstraction) preserve
  much source variation while restructuring it structurally; their color is
  the source color drawn, lined, or brushed.
- **65% abstraction:** the 65%-pool methods (Geometric Abstraction,
  Fragmentation, Collage Abstraction) restructure form; color stays
  source-derived inside the planes, fragments, or collage pieces.
- **90% abstraction:** the 90%-pool methods (Shape Reduction, Chinese Ink
  Wash, Cartoon Pixel) keep only a semantic skeleton; color stays
  source-derived in the reduced shapes, washes, or pixel palette.

As abstraction rises, the same source color is carried through progressively
stronger structural reinterpretation. Do not add per-region palette
compression, per-region hue shifts, or per-region saturation curves — the
color identity is one, the abstraction differs.

## Cross-slice relationship

Because all regions share one photographic color identity, the poster is
coherent by construction: the same hues, the same highlights, the same warm
grade recur wherever the same source content recurs. Use a small number of
hue echoes, shared highlight logic, or repeated accents to reinforce
coherence.

Do not blend colors across boundaries to soften the seams — the paper-material
seam is the boundary's representation, and it is drawn by the pipeline. Do not
shift the palette at a boundary to "announce" a new abstraction state: the
state change is announced by the structural language, not by color.

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
openness across the composition — the same sky color in every region that
contains it, at that region's abstraction.

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
3. Render each abstract zone with the same color identity as the source slice
   it owns — the method's structural language carries the source color.
4. Apply the same warm grade uniformly to the whole poster; never tint regions
   differently.
5. Repeat a small, controlled accent set consistently wherever the same source
   content recurs.

Before delivery, confirm that the poster reads as ONE photograph whose four
regions differ only by abstraction: the anchor is the (graded) source; the
30%, 65%, and 90% regions reinterpret their own slice of the same color
identity; saturation and contrast remain controlled; accents are intentional;
and no region has been given its own palette, hue role, or color emphasis.
