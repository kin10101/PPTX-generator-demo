---
name: erni-powerpoint-builder
description: "create, edit, and quality-check enterprise powerpoint .pptx decks in the erni master template. use when the user asks for a presentation, pitch deck, proposal, capability deck, executive deck, consulting deck, or slide redesign that must follow the uploaded erni template, reuse its layouts/icons/smart-art-like patterns, and use only bundled template assets plus the approved uploaded abstract images."
---

# ERNI PowerPoint Builder

## Core rule

Create PowerPoint decks from `assets/templates/erni_master_template.pptx`. Preserve the ERNI master layouts, theme, typography rhythm, footer, slide numbers, icon style, and structured flow/card patterns.

Use only these visual sources in final decks:

1. media already embedded in `assets/templates/erni_master_template.pptx`,
2. approved abstract images in `assets/images/`, and
3. ERNI template icons/brand media in `assets/icons/template-media/`.

Do not fetch web images, use stock imagery, generate new decorative images, paste screenshot charts, or import external icon packs. Create charts and diagrams as editable PowerPoint objects or shapes in ERNI theme colors.

## Required workflow

1. **Understand the deck need.** Determine audience, objective, slide count, input content, deadline, and whether the output is a new deck or a redesign. Ask only for missing information that blocks progress.
2. **Plan the narrative.** Build a concise consulting-style storyline: cover, optional agenda, context/problem, insight, recommendation/solution, evidence, roadmap/next steps, and close.
3. **Choose layouts by intent.** Use the mapping below and consult `references/layout_catalog.md` for exact layout names.
4. **Build from the master template.** Open/copy `assets/templates/erni_master_template.pptx`; add slides using existing master layouts by name. Do not recreate the visual system from scratch.
5. **Apply visuals.** Use `references/asset_manifest.md` to select approved images and template icons. Crop images to cover placeholders; never stretch them.
6. **Check the deck.** Review layout adherence, text fit, image permissions, icon consistency, footer/slide numbers, and contrast.
7. **Validate bundled media.** Before returning a PPTX, run `scripts/validate_deck_assets.py <output.pptx>` whenever code execution is available. Replace any unauthorized media it reports.

## Layout selection

| slide intent | preferred template layouts | guidance |
|---|---|---|
| image-led cover | `Cover Layout 1` | use one approved abstract image in the right-side picture placeholder |
| conservative cover | `Cover Layout 2`, `Cover Layout 3` | use for white executive openers without hero imagery |
| agenda/index | `Index Layout 1a-1d`, `Index Layout 2a-2d` | use for contents, agenda, or chapter roadmap |
| section divider | `Section Layout 1` | use ERNI blue section slides with section number and title |
| narrative text + image | `Info Layout Image and Text 6a`, `Info Layout Image and Text 6b` | use 6a for single-column prose and 6b for two-column prose |
| full graphic/system view | `Info Layout 9a - Full Graphic`, `Info Layout 9b - Full Graphic` | use for maps, lifecycle diagrams, ecosystem views, or large visuals |
| three pillars/icons | `Info Layout 2a - Vertical Lines`, `Info Layout 8a - Subtitle 3 Icons Right Separators`, `Chart Layout 2a - Subtitle-3 Icons` | preserve the separator rhythm and equal column widths |
| four item comparison | `Chart Layout 2b - 4 Icons`, `Chart Layout 3 - Icons and Bullet points`, `People Layout 3` | use for values, capabilities, services, locations, or operating model elements |
| five or six step process | `Flow Layout 3b`, `Flow Layout 6b`, `Flow Layout 3a` | use for collaboration models, service portfolios, roadmaps, and journeys |
| facts and figures | `Containers Layout` | use six consistent cards; keep numbers large and explanations short |
| people/team | `People Layout 1`, `People Layout 2`, `People Layout 3` | use only when the user provides names, roles, and approved headshots or text-only profiles |
| closing/contact | `1_Back Cover 1`, `Back Cover 2`, `Back Cover 3` | use contact layout when contact details are available |

## SmartArt and diagram pattern

Treat requests for SmartArt, frameworks, operating models, lifecycles, processes, or roadmaps as requests for ERNI template-native structured layouts. The inspected template uses placeholder-based flow, chart, info, and container layouts rather than native PowerPoint SmartArt objects.

Use the template's existing cards, separators, icon placeholders, and text placeholders. Do not insert default Office SmartArt, unrelated diagram styles, or external infographic artwork.

## Visual style rules

- Use Source Sans Pro when available; otherwise use a clean sans-serif fallback. Do not bundle or share font files.
- Use ERNI theme colors: ERNI blue `#033778`, cyan `#00AADB`, dark gray `#3C3C3B`, light gray `#B1B0B1`, and white.
- Keep slide titles concise and assertive. Prefer one headline and one explanatory subtitle over dense text.
- Preserve whitespace. The template is spacious; do not fill every empty area.
- Keep option titles parallel in grammar and similar in length.
- Place icons only in icon placeholders or aligned to the same grid. Use the ERNI blue line-icon style from `assets/icons/template-media/`.
- Use one dominant image per slide unless the selected layout explicitly requires multiple photos.
- Add overlays or white/blue panels only when necessary for text contrast.
- Avoid decorative shapes that are not part of the master layout system.

## Approved image usage

Consult `references/asset_manifest.md` before selecting images. Preferred use cases:

- dynamic innovation or AI covers: `orange-wave-70.jpg`, `cyan-magenta-fluid-ribbon-57.jpg`, `warp-speed-light-beams-64.jpg`, `neon-spiral-16.jpg`;
- engineering, architecture, security, or systems: `red-blue-architectural-stripes-14.jpg`, `blue-geometric-triangles-61.jpg`, `purple-wave-lines-54.jpg`, `red-polygon-panels-47.jpg`;
- sustainability, people, or culture: `green-palm-lines-79.jpg`, `glass-flower-ceiling-35.jpg`;
- calm operations, continuity, or ecosystem themes: `aqua-water-bubbles-84.jpg`, `icy-teal-foam-03.jpg`;
- journey, roadmap, portfolio, or transformation: `rainbow-corridor-28.jpg`, `rainbow-vertical-lines-06.jpg`, `cyan-yellow-magenta-scanlines-76.jpg`.

## Build guidance

When using code, prefer a PowerPoint-aware library that preserves the `.pptx` master. Use layout names or substring matching because some source layout names contain trailing spaces. Fill placeholders instead of placing free-floating content whenever possible.

For image placeholders, insert the image with aspect-ratio-preserving crop-to-cover behavior. For icon placeholders, insert an SVG/PNG from `assets/icons/template-media/` and keep size consistent across the slide.

If adapting an existing deck, convert each slide to the closest ERNI layout. Replace non-approved photos or icons with approved abstract images, template icons, or editable shape diagrams.

## Quality checklist

Before sending the final PPTX, verify:

- every slide uses an ERNI master layout or follows the same grid precisely;
- no web, stock, generated, or unapproved visual assets are embedded;
- the validation script passes or unauthorized media has been removed;
- footer text, slide numbers, logo/brand elements, and section numbers remain aligned;
- icons are consistent in style, size, and color;
- text does not overflow placeholders and is readable at presentation size;
- charts and diagrams are editable and use ERNI colors;
- the final slide uses an ERNI back-cover layout when appropriate.

## References and assets

- `references/template_pattern_guide.md`: theme findings, icon rules, SmartArt-like structure, and visual composition.
- `references/layout_catalog.md`: all 77 source layout names with placeholder counts.
- `references/asset_manifest.md`: approved image filenames, descriptions, and use cases.
- `assets/templates/erni_master_template.pptx`: optimized master template preserving layouts/theme.
- `assets/images/`: approved uploaded abstract images.
- `assets/icons/template-media/`: extracted ERNI template icons and brand media.
- `scripts/validate_deck_assets.py`: allowlist-based PPTX media checker.
