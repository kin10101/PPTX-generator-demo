# ERNI template pattern guide

This guide summarizes findings from inspecting the uploaded master template.

## Master template facts

- Size: 16:9 widescreen (`24384000 x 13716000` EMU).
- Theme: `ERNI Standard Slides`.
- Primary font: Source Sans Pro. Use a common sans-serif fallback only when the font is unavailable; do not bundle font files.
- Core theme colors:
  - dark gray `#3C3C3B`
  - ERNI blue `#033778`
  - light gray `#B1B0B1`
  - cyan accent `#00AADB`
  - white `#FFFFFF`
- Footer pattern: small `Better ask ERNI` text at the upper-left and slide number at the upper-right on most content layouts.
- The uploaded source deck contains 1 master and 77 slide layouts. See `layout_catalog.md` for exact layout names.

## Smart-art-like structure

No native PowerPoint SmartArt or chart parts were detected in the master file. The visual system instead uses structured slide layouts with:

- picture placeholders for icons, photos, and hero images;
- fixed separator lines;
- card/background rectangles;
- title, subtitle, body, option title, and option description placeholders;
- grouped brand graphics on back covers.

When users ask for SmartArt, process diagrams, journeys, lifecycles, operating models, or frameworks, use the template's Flow, Chart, Info, and Containers layouts rather than inserting default Office SmartArt.

## Icon pattern

- Use line-style ERNI blue icons from `assets/icons/template-media/` in the template's icon placeholders.
- Keep icon placement inside existing icon placeholders whenever possible. Many icon placeholders are square and sized consistently.
- Use one icon style per slide. Do not mix blue line icons with photographic symbols or emoji.
- If no bundled icon fits, create a minimal editable line icon from simple PowerPoint shapes in ERNI blue/cyan; do not import external icons.
- For icon-led slides, keep titles short, usually one to four words, and keep descriptions to one short paragraph or up to three compact bullets.

## Common layout patterns

| pattern | use these layouts | notes |
|---|---|---|
| image cover | `Cover Layout 1` | right-side full-height image placeholder; use an approved abstract image |
| white cover | `Cover Layout 2`, `Cover Layout 3` | clean white opener; use when a conservative executive style is desired |
| section divider | `Section Layout 1` | ERNI blue background, section number on left of title block |
| narrative + image | `Info Layout Image and Text 6a`, `Info Layout Image and Text 6b` | use 6a for one paragraph, 6b for two-column text |
| full graphic | `Info Layout 9a - Full Graphic`, `Info Layout 9b - Full Graphic` | use for maps, lifecycle diagrams, or big visual systems |
| three pillars | `Info Layout 2a - Vertical Lines`, `Info Layout 8a - Subtitle 3 Icons Right Separators`, `Chart Layout 2a - Subtitle-3 Icons` | preserve vertical separators and icon rhythm |
| four items | `Chart Layout 2b - 4 Icons`, `Chart Layout 3 - Icons and Bullet points`, `People Layout 3` | good for values, service domains, locations, or capabilities |
| five/six-step flow | `Flow Layout 3b`, `Flow Layout 6b`, `Flow Layout 3a` | use for collaboration models, roadmaps, service portfolios |
| metrics/facts | `Containers Layout` | six equal cards with title and body text; keep numbers large |
| people/team | `People Layout 1`, `People Layout 2`, `People Layout 3` | use only when headshots or role descriptions are provided |
| closing | `1_Back Cover 1`, `Back Cover 2`, `Back Cover 3` | use the contact layout when contact details are supplied |

## Typography rhythm

- Keep slide titles large and concise. Prefer one clear headline over multiple competing labels.
- Use subtitles as the main explanatory line, not as a second title.
- Use short body copy. The master template favors spacious text blocks, not dense paragraphs.
- When a layout has option titles and descriptions, keep option titles parallel and descriptions similar length.
- Use title case or sentence case consistently within a deck; do not mix within a layout group.

## Visual composition

- Respect the master grid and placeholders. Do not manually reposition footer, logo, slide number, or section number unless adapting an existing slide that is already off-grid.
- Use white backgrounds for content-heavy slides and blue section dividers for structural breaks.
- Use full-bleed abstract images only in layouts designed for pictures or full graphics.
- Avoid adding decorative shapes outside the established ERNI system.
- For data visuals, use editable charts or shape-based diagrams in template colors; do not paste chart screenshots.
