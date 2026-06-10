---
name: erni-powerpoint-builder
description: "create, edit, and quality-check enterprise powerpoint .pptx decks in the erni visual style. use when the user asks for a presentation, pitch deck, proposal, capability deck, executive deck, consulting deck, or slide redesign that must follow ERNI branding, use only bundled template assets plus approved abstract images."
---

# ERNI PowerPoint Builder

## Core rule

Generate slide element specifications that the renderer translates directly into .pptx output. All positioning, styling, and content are specified per-element in the slide spec JSON.

Use only these visual sources:

1. approved abstract images in `assets/images/`, and
2. ERNI template icons/brand media in `assets/icons/template-media/`.

Do not fetch web images, use stock imagery, generate new decorative images, or import external icon packs.

## Slide canvas

- **Dimensions:** 13.33 inches wide × 7.5 inches tall
- **Font:** Source Sans Pro
- **Brand colors:** erniBlue=033778, cyan=00AADB, darkGray=3C3C3B, lightGray=B1B0B1, white=FFFFFF
- **Footer:** Automatically rendered by the system at the top of each slide (do not include footer elements in specs)

## Element types

Each slide is composed of positioned elements:

1. **TEXT** — text content with font, color, size, alignment, position, and dimensions
2. **IMAGE** — an approved image placed at exact coordinates with optional cover/contain sizing
3. **SHAPE** — rect, ellipse, or line with fill/stroke properties
4. **ICON** — an icon from the template-media folder placed at exact coordinates

## Required workflow

1. **Understand the deck need.** Determine audience, objective, slide count, and input content.
2. **Plan the narrative.** Build a consulting-style storyline: cover, context/problem, insight, recommendation, evidence, roadmap, and close.
3. **Define layout intents.** For each slide, describe the visual approach (e.g., "cover with hero image right half", "3-column process flow", "full-width narrative").
4. **Generate element specs.** For each slide, output a complete array of positioned elements using the canvas dimensions, brand colors, and typography rules.
5. **Select assets.** Use `references/asset_manifest.md` to pick approved images. Use icons from `assets/icons/template-media/`.
6. **Validate.** Ensure all elements stay within canvas bounds, use only approved assets, and follow ERNI style.

## Layout patterns (for inspiration)

Use `references/layout_catalog.md` for the full catalog of layout patterns. Common patterns:

| slide intent | layout approach |
|---|---|
| cover | hero image on right half (6.67" wide), title + subtitle on left |
| section divider | full blue background, large section number + title centered |
| narrative | title at top, body text below, optional image left panel |
| process/flow | numbered circles connected by lines, titles + descriptions below |
| three pillars | 3 equal columns with icons, titles, and descriptions separated by vertical lines |
| facts/figures | 2×3 or 3×2 grid of cards with large values and labels |
| closing | ERNI blue background with centered closing message |

## Visual style rules

- Title text: 26-40pt, bold, erniBlue (033778)
- Subtitle text: 16-20pt, darkGray (3C3C3B)
- Body text: 12-14pt, darkGray (3C3C3B)
- Keep ~0.8" margins on sides
- Leave top 0.6" clear for the auto-rendered footer
- Use ERNI theme colors exclusively
- Preserve whitespace — the ERNI style is spacious
- One dominant image per slide maximum
- Icons should be consistent in size (typically 0.4-0.6" square)
- Use separator lines (shape type "line") in erniBlue to divide columns

## Approved image usage

Consult `references/asset_manifest.md` before selecting images. Preferred use cases:

- dynamic innovation or AI covers: `orange-wave-70.jpg`, `cyan-magenta-fluid-ribbon-57.jpg`, `warp-speed-light-beams-64.jpg`, `neon-spiral-16.jpg`
- engineering/architecture/security: `red-blue-architectural-stripes-14.jpg`, `blue-geometric-triangles-61.jpg`, `purple-wave-lines-54.jpg`
- sustainability/people/culture: `green-palm-lines-79.jpg`, `glass-flower-ceiling-35.jpg`
- calm operations/continuity: `aqua-water-bubbles-84.jpg`, `icy-teal-foam-03.jpg`
- journey/roadmap/transformation: `rainbow-corridor-28.jpg`, `rainbow-vertical-lines-06.jpg`

## Quality checklist

Before finalizing:

- all elements stay within canvas bounds (0-13.33 x, 0-7.5 y)
- no unauthorized images or icons are referenced
- text is readable at presentation size (min 11pt)
- colors are from the ERNI palette
- font is Source Sans Pro throughout
- sufficient whitespace and visual hierarchy

## References and assets

- `references/template_pattern_guide.md`: theme findings, icon rules, visual composition guidance.
- `references/layout_catalog.md`: layout patterns with descriptions (use as inspiration).
- `references/asset_manifest.md`: approved image filenames, descriptions, and use cases.
- `assets/images/`: approved abstract background images.
- `assets/icons/template-media/`: ERNI template icons and brand media.
- `scripts/validate_deck_assets.py`: allowlist-based PPTX media checker.
