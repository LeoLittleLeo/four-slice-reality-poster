# Robot Dreams-Inspired Cinematic Color System

## Contents

- Global emotional palette
- Palette families
- Saturation, contrast, and accents
- Color behavior by slice
- Subject-specific color
- Execution and validation

## Global emotional palette

Establish one shared palette universe before coloring individual slices. Aim for the broad emotional qualities of *Robot Dreams*—warm, nostalgic, gentle, sunlit, slightly retro, harmonious, and dreamlike without copying a specific frame. Keep the result stylized but not excessively saturated.

Make all four abstraction states belong to a related emotional family without forcing identical grading. Favor soft urban sunlight, tender melancholy, quiet optimism, softened memory-like color, editorial dreaminess, and cinematic calm. Permit clearly different color emphasis in each module so the four states remain readable. Avoid harsh, metallic, coldly futuristic, neon, horror-like, blockbuster-contrast, or random pop-art moods unless explicitly requested.

## Palette families

Build the palette primarily from:

- **Warm foundations:** warm beige, cream, dusty peach, muted coral, warm sand, soft terracotta, sunlit ochre, warm light brown, soft brick, and faded orange-red.
- **Air and sky:** powder blue, dusty sky blue, pale cyan, washed turquoise, muted teal, and soft cloud gray-blue. Keep these airy rather than digital.
- **Balanced greens:** sage, dusty olive, gray-green, muted teal-green, and softened blue-green. Avoid acidic green unless justified by the source.
- **Controlled accents:** tomato or muted cherry red, mustard yellow, coral, muted navy, warm denim blue, and terracotta red-orange.

Adapt these families to the source rather than forcing every named hue into every image. Preserve major source color identity when it supports the shared emotional palette.

## Saturation, contrast, and accents

Keep overall saturation medium-low to medium, with selective moderate saturation at focal areas. Soften strong-hue transitions and retain a slightly faded cinematic quality. Keep the image alive rather than dull, but avoid fluorescent intensity, candy oversaturation, arbitrary high-chroma clashes, or gray mud.

Use gentle tonal contrast, readable but calm value separation, soft sunlight, open highlights, and quiet shadows. Avoid crushed blacks, severe HDR, aggressive commercial-poster contrast, and glossy digital sharpness.

Choose a small accent set and repeat it intentionally across slices to guide attention, reinforce focal forms, and create rhythm. Place accents in clothing details, architectural highlights, object edges, signage fragments, selected strokes, or color blocks. Do not scatter strong accents everywhere.

## Color behavior by slice

Treat all slices as related palette families at different degrees of transformation. Allow visible differences in dominant hue, warmth, value range, or accent density when they clarify module identity.

- **Reality Anchor:** Keep the Reality state unmistakably photographic, source-faithful, and identity-preserving. Do not require source-pixel restoration when the coherent candidate already preserves recognizable identity, natural anatomy, hairline, and face-to-neck continuity. If restoration is necessary, use only geometrically verified local restoration that demonstrably improves the face. If useful, apply warming, contrast softening, or gentle muting through deterministic non-structural processing. Palette unity never outranks face identity or human continuity.
- **30% abstraction:** Stay closest to local photographic color. Preserve much source variation while gently simplifying hues, softening saturation, compressing the palette, warming highlights, and introducing mild color blocking.
- **65% abstraction:** Group colors into broader masses, simplify the palette more decisively, orchestrate warm and cool relationships, and rely less on literal local color accuracy. Keep the same emotional universe.
- **90% abstraction:** Use the smallest, most intentional palette; allow symbolic accents, large warm/cool blocks, painterly atmosphere, and abstract color rhythm. Preserve shared color DNA and avoid unrelated explosions.

As abstraction rises, reduce micro-variation and color noise. Merge similar hues more aggressively and make the emotional structure more legible. Higher abstraction should usually mean greater curation, not greater random variety.

## Cross-slice relationship

Use a small number of hue echoes, shared highlight logic, or repeated accents to make the poster coherent. Do not require continuous atmospheric color or gradual hue blending across every boundary. Allow an abrupt palette shift when it deliberately announces a new abstraction state and still belongs to the broader warm, nostalgic color world.

Apply color relationships with [intentional-modular-composition.md](intentional-modular-composition.md). Prefer readable modular contrast over color blending when the two conflict.

## Subject-specific color

For important people, use softened warm skin families, simplified coherent clothing colors, and contour/color-block interplay. Avoid over-pink, dead gray, plastic orange, or excessively vivid fashion colors that break harmony. Preserve emotional readability over tiny local color accuracy.

For architecture, favor sunlit beige, sand, terracotta, muted brick, soft façade warmth, and restrained sky-reflective cools. Merge micro-colors into larger planes as abstraction increases while preserving major architectural color identity. Avoid rainbow buildings, steel-blue domination unless source-required, or signage that overwhelms the massing.

Use sky, street, landscape, and other environmental regions to carry airy blues, warm reflected light, dusty sunlight, soft horizons, and gentle tonal openness across the composition.

## Decision priority

Color decisions inherit the global priority in `SKILL.md`; this local list applies only after face identity, human continuity, Reality role, architectural identity, and four-state readability are secure:

1. Protection of already-secure face, body, Reality, and architectural structure.
2. Readability of the four abstraction states.
3. Emotional warmth and broad palette relationship.
4. Intentional module-to-module contrast.
5. Poster-level color coherence.
6. Literal local color accuracy.

## Execution and validation

1. Establish the global palette mood.
2. Keep the Reality Anchor photographic and source-faithful. Preserve Candidate A unchanged when it passes the Face Restoration Gate; use source restoration only after gate failure and verified alignment. Optionally grade the selected Reality candidate with deterministic non-generative operations that cannot alter facial geometry, facial texture structure, feature placement, or identity; otherwise leave it unchanged.
3. Give each abstract slice a distinct but related color emphasis.
4. Increase palette compression with abstraction level.
5. Use selected repeated hues or accents to connect modules without smoothing away their differences.
6. Repeat a small, controlled accent set across multiple slices.

Before delivery, confirm that the poster reads as four distinct states inside one warm, nostalgic, gentle, slightly dreamy editorial system; the anchor belongs to that broader world; the 30%, 65%, and 90% slices show increasing palette interpretation; saturation and contrast remain controlled; accents are intentional; and color differences clarify modules without becoming random or unrelated.
