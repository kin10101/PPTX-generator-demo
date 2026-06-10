# ERNI element-based layout catalog

This catalog provides coordinate recipes for the most common slide layouts. Every layout is expressed as a JSON `elements` array that maps directly to renderer input. Copy and adapt the recipes â€” replace placeholder strings with real content.

## Canvas facts

| property | value |
|---|---|
| canvas width | 13.33 inches |
| canvas height | 7.50 inches |
| auto-rendered footer zone | x=0.4â€“12.9, y=0.20â€“0.45 â€” do not add elements here |
| safe content top | y = 0.70 |
| safe content bottom | y = 7.20 |
| left/right margin | 0.80 inches â†’ content x = 0.80 to 12.53 (width = 11.73") |
| font | Source Sans Pro |
| erniBlue | 033778 |
| cyan | 00AADB |
| darkGray | 3C3C3B |
| lightGray | B1B0B1 |
| white | FFFFFF |

## Element types quick reference

| type | required fields | key optional fields |
|---|---|---|
| text | type, content, x, y, w, h | fontSize, fontFace, color, bold, italic, align, valign, autoFit, lineSpacing |
| image | type, src, x, y, w, h | sizing: { type:"cover"\|"contain", w, h } |
| shape | type, shape ("rect"\|"ellipse"\|"line"), x, y, w, h | fill (hex), line: { color, width }, rectRadius |
| icon | type, src, x, y, w, h | â€” |

Image `src` must start with `images/`. Icon `src` must start with `icons/template-media/`.

---

## Layout 1 â€” Cover: hero image right half

**Purpose:** Opening slide with a full-height abstract image on the right and title/subtitle on the left. Use when an approved hero image is available.

**Visual:** White left panel occupies the left 6.67 inches. A full-bleed abstract image fills the right 6.66 inches from top to bottom. A thin cyan accent line anchors the title block. An ERNI blue strip at the bottom left provides brand weight.

**Element recipe:**

```json
{
  "slideIndex": 1,
  "background": { "color": "FFFFFF" },
  "footer": true,
  "elements": [
    // Right-half hero image â€” full bleed
    {
      "type": "image",
      "src": "images/cyan-magenta-fluid-ribbon-57.jpg",
      "x": 6.67, "y": 0.00, "w": 6.66, "h": 7.50,
      "sizing": { "type": "cover", "w": 6.66, "h": 7.50 }
    },
    // Cyan accent line above title
    {
      "type": "shape", "shape": "line",
      "x": 0.80, "y": 1.90, "w": 2.50, "h": 0,
      "line": { "color": "00AADB", "width": 2 }
    },
    // Main title
    {
      "type": "text",
      "content": "Presentation Title",
      "x": 0.80, "y": 2.00, "w": 5.50, "h": 1.60,
      "fontSize": 36, "fontFace": "Source Sans Pro",
      "color": "033778", "bold": true, "valign": "top"
    },
    // Subtitle / deck descriptor
    {
      "type": "text",
      "content": "Subtitle or client name",
      "x": 0.80, "y": 3.70, "w": 5.50, "h": 0.70,
      "fontSize": 18, "fontFace": "Source Sans Pro",
      "color": "3C3C3B"
    },
    // Date / presenter line
    {
      "type": "text",
      "content": "Author Â· Month Year",
      "x": 0.80, "y": 5.50, "w": 5.50, "h": 0.45,
      "fontSize": 13, "fontFace": "Source Sans Pro",
      "color": "B1B0B1"
    },
    // ERNI blue brand strip â€” bottom left
    {
      "type": "shape", "shape": "rect",
      "x": 0.00, "y": 6.80, "w": 6.67, "h": 0.70,
      "fill": "033778"
    }
  ]
}
```

---

## Layout 2 â€” Cover: text only, white

**Purpose:** Clean executive cover with no image. Use for conservative client contexts or when no approved hero image is suitable.

**Visual:** Full white background. Title is large and centered. A thin cyan rule separates title from subtitle. An ERNI blue strip anchors the bottom edge.

**Element recipe:**

```json
{
  "slideIndex": 1,
  "background": { "color": "FFFFFF" },
  "footer": false,
  "elements": [
    // Large centered title
    {
      "type": "text",
      "content": "Presentation Title",
      "x": 1.50, "y": 2.20, "w": 10.33, "h": 1.50,
      "fontSize": 40, "fontFace": "Source Sans Pro",
      "color": "033778", "bold": true,
      "align": "center", "valign": "middle"
    },
    // Cyan accent rule
    {
      "type": "shape", "shape": "line",
      "x": 4.50, "y": 3.85, "w": 4.33, "h": 0,
      "line": { "color": "00AADB", "width": 2 }
    },
    // Subtitle
    {
      "type": "text",
      "content": "Subtitle or client name",
      "x": 1.50, "y": 4.00, "w": 10.33, "h": 0.75,
      "fontSize": 20, "fontFace": "Source Sans Pro",
      "color": "3C3C3B", "align": "center"
    },
    // Date / presenter
    {
      "type": "text",
      "content": "Author Â· Month Year",
      "x": 1.50, "y": 5.10, "w": 10.33, "h": 0.50,
      "fontSize": 13, "fontFace": "Source Sans Pro",
      "color": "B1B0B1", "align": "center"
    },
    // ERNI blue bottom strip
    {
      "type": "shape", "shape": "rect",
      "x": 0.00, "y": 7.00, "w": 13.33, "h": 0.50,
      "fill": "033778"
    }
  ]
}
```

---

## Layout 3 â€” Section divider: blue background

**Purpose:** Chapter break slide. Signals a structural transition in the deck. Use before each major section.

**Visual:** Full ERNI blue canvas. A large section number sits on the left. A white vertical line separates it from the section title and subtitle on the right.

**Element recipe:**

```json
{
  "slideIndex": 3,
  "background": { "color": "033778" },
  "footer": false,
  "elements": [
    // Large section number (right-aligned in its box)
    {
      "type": "text",
      "content": "01",
      "x": 0.80, "y": 1.80, "w": 2.70, "h": 2.50,
      "fontSize": 96, "fontFace": "Source Sans Pro",
      "color": "FFFFFF", "bold": true,
      "align": "right", "valign": "middle"
    },
    // White vertical separator
    {
      "type": "shape", "shape": "line",
      "x": 3.80, "y": 1.80, "w": 0, "h": 3.50,
      "line": { "color": "FFFFFF", "width": 2 }
    },
    // Section title
    {
      "type": "text",
      "content": "Section Title",
      "x": 4.20, "y": 2.30, "w": 8.13, "h": 1.40,
      "fontSize": 34, "fontFace": "Source Sans Pro",
      "color": "FFFFFF", "bold": true, "valign": "bottom"
    },
    // Section subtitle / descriptor
    {
      "type": "text",
      "content": "Brief description of what this section covers",
      "x": 4.20, "y": 3.85, "w": 8.13, "h": 1.00,
      "fontSize": 18, "fontFace": "Source Sans Pro",
      "color": "FFFFFF", "valign": "top"
    }
  ]
}
```

---

## Layout 4 â€” Narrative / full text

**Purpose:** Content-heavy slide with a single large text block. Use for analysis, recommendations, or any slide where prose is the primary content.

**Visual:** Standard title and subtitle at the top, a light horizontal rule below the subtitle, and a full-width body text column beneath.

**Element recipe:**

```json
{
  "slideIndex": 4,
  "background": { "color": "FFFFFF" },
  "footer": true,
  "elements": [
    // Slide title
    {
      "type": "text",
      "content": "Slide Title",
      "x": 0.80, "y": 0.70, "w": 11.73, "h": 0.75,
      "fontSize": 28, "fontFace": "Source Sans Pro",
      "color": "033778", "bold": true
    },
    // Subtitle / lead-in sentence
    {
      "type": "text",
      "content": "A concise subtitle or framing sentence",
      "x": 0.80, "y": 1.55, "w": 11.73, "h": 0.45,
      "fontSize": 16, "fontFace": "Source Sans Pro",
      "color": "3C3C3B"
    },
    // Horizontal rule
    {
      "type": "shape", "shape": "line",
      "x": 0.80, "y": 2.10, "w": 11.73, "h": 0,
      "line": { "color": "B1B0B1", "width": 1 }
    },
    // Body text (single full-width column)
    {
      "type": "text",
      "content": "Body copy goes here. Keep paragraphs short. The ERNI style favors spacious text â€” aim for 3â€“5 short paragraphs or a structured narrative with clear topic sentences.",
      "x": 0.80, "y": 2.30, "w": 11.73, "h": 4.70,
      "fontSize": 13, "fontFace": "Source Sans Pro",
      "color": "3C3C3B", "valign": "top", "lineSpacing": 1.4
    }
  ]
}
```

---

## Layout 5 â€” Two column text

**Purpose:** Parallel content â€” compare two themes, show before/after, or split a topic into two dimensions.

**Visual:** Title and subtitle span full width. A horizontal rule separates the header from two equal text columns divided by a vertical light-gray line.

**Column positions:**
- Column 1: x=0.80, w=5.70 (right edge 6.50)
- Vertical separator: x=6.70
- Column 2: x=6.90, w=5.63 (right edge 12.53)

**Element recipe:**

```json
{
  "slideIndex": 5,
  "background": { "color": "FFFFFF" },
  "footer": true,
  "elements": [
    { "type": "text", "content": "Slide Title",
      "x": 0.80, "y": 0.70, "w": 11.73, "h": 0.75,
      "fontSize": 28, "fontFace": "Source Sans Pro", "color": "033778", "bold": true },
    { "type": "text", "content": "Framing subtitle that sets up the two columns",
      "x": 0.80, "y": 1.55, "w": 11.73, "h": 0.45,
      "fontSize": 16, "fontFace": "Source Sans Pro", "color": "3C3C3B" },
    { "type": "shape", "shape": "line",
      "x": 0.80, "y": 2.10, "w": 11.73, "h": 0,
      "line": { "color": "B1B0B1", "width": 1 } },

    // Left column header
    { "type": "text", "content": "Left Column Heading",
      "x": 0.80, "y": 2.25, "w": 5.70, "h": 0.45,
      "fontSize": 15, "fontFace": "Source Sans Pro", "color": "033778", "bold": true },
    // Left column body
    { "type": "text", "content": "Left column body text. Keep paragraphs short and parallel in length with the right column.",
      "x": 0.80, "y": 2.80, "w": 5.70, "h": 4.20,
      "fontSize": 13, "fontFace": "Source Sans Pro", "color": "3C3C3B", "valign": "top" },

    // Vertical separator
    { "type": "shape", "shape": "line",
      "x": 6.70, "y": 2.25, "w": 0, "h": 4.75,
      "line": { "color": "B1B0B1", "width": 1 } },

    // Right column header
    { "type": "text", "content": "Right Column Heading",
      "x": 6.90, "y": 2.25, "w": 5.63, "h": 0.45,
      "fontSize": 15, "fontFace": "Source Sans Pro", "color": "033778", "bold": true },
    // Right column body
    { "type": "text", "content": "Right column body text. Match the depth and tone of the left column.",
      "x": 6.90, "y": 2.80, "w": 5.63, "h": 4.20,
      "fontSize": 13, "fontFace": "Source Sans Pro", "color": "3C3C3B", "valign": "top" }
  ]
}
```

---

## Layout 6 â€” Image left + text right

**Purpose:** Combine a strong visual with supporting narrative. Use for case study evidence, location context, or any slide where a visual needs prose explanation.

**Visual:** Title spans full width. Below the title, an image fills the left panel. A vertical rule separates it from a text block on the right.

**Image panel:** x=0.80, y=1.65, w=5.20, h=5.40
**Text panel:** x=6.50, y=1.65, w=6.03, h=5.40

**Element recipe:**

```json
{
  "slideIndex": 6,
  "background": { "color": "FFFFFF" },
  "footer": true,
  "elements": [
    { "type": "text", "content": "Slide Title",
      "x": 0.80, "y": 0.70, "w": 11.73, "h": 0.70,
      "fontSize": 26, "fontFace": "Source Sans Pro", "color": "033778", "bold": true },
    { "type": "shape", "shape": "line",
      "x": 0.80, "y": 1.50, "w": 11.73, "h": 0,
      "line": { "color": "B1B0B1", "width": 1 } },

    // Left image
    { "type": "image", "src": "images/blue-geometric-triangles-61.jpg",
      "x": 0.80, "y": 1.65, "w": 5.20, "h": 5.40,
      "sizing": { "type": "cover", "w": 5.20, "h": 5.40 } },

    // Vertical separator
    { "type": "shape", "shape": "line",
      "x": 6.20, "y": 1.65, "w": 0, "h": 5.40,
      "line": { "color": "B1B0B1", "width": 1 } },

    // Text panel header
    { "type": "text", "content": "Key Insight or Section Heading",
      "x": 6.50, "y": 1.65, "w": 6.03, "h": 0.55,
      "fontSize": 16, "fontFace": "Source Sans Pro", "color": "033778", "bold": true },
    // Text panel body
    { "type": "text", "content": "Supporting narrative. Can include 3â€“5 short paragraphs or bulleted observations. Keep the text panel less dense than the image to preserve breathing room.",
      "x": 6.50, "y": 2.30, "w": 6.03, "h": 4.75,
      "fontSize": 13, "fontFace": "Source Sans Pro", "color": "3C3C3B", "valign": "top" }
  ]
}
```

---

## Layout 7 â€” Three column: icons + titles + descriptions

**Purpose:** Three parallel pillars â€” capabilities, values, service areas, or principles. The canonical ERNI three-pillar layout.

**Visual:** Title and subtitle header. Three equal columns separated by vertical light-gray lines, each headed by a centered icon, bold title, and description text beneath.

**Column positions (w=3.64 each):**
| element | x | y |
|---|---|---|
| Column 1 content | 0.80 | â€” |
| Column 1 icon center | 2.37 | 2.20 |
| Vertical separator 1 | 4.64 | â€” |
| Column 2 content | 4.84 | â€” |
| Column 2 icon center | 6.41 | 2.20 |
| Vertical separator 2 | 8.68 | â€” |
| Column 3 content | 8.88 | â€” |
| Column 3 icon center | 10.45 | 2.20 |

**Element recipe:**

```json
{
  "slideIndex": 7,
  "background": { "color": "FFFFFF" },
  "footer": true,
  "elements": [
    { "type": "text", "content": "Slide Title",
      "x": 0.80, "y": 0.70, "w": 11.73, "h": 0.70,
      "fontSize": 28, "fontFace": "Source Sans Pro", "color": "033778", "bold": true },
    { "type": "text", "content": "Subtitle describing the three pillars",
      "x": 0.80, "y": 1.50, "w": 11.73, "h": 0.45,
      "fontSize": 16, "fontFace": "Source Sans Pro", "color": "3C3C3B" },
    { "type": "shape", "shape": "line",
      "x": 0.80, "y": 2.05, "w": 11.73, "h": 0,
      "line": { "color": "B1B0B1", "width": 1 } },

    // Icons (0.50" square, centered per column)
    { "type": "icon", "src": "icons/template-media/icon-1.png",
      "x": 2.37, "y": 2.20, "w": 0.50, "h": 0.50 },
    { "type": "icon", "src": "icons/template-media/icon-2.png",
      "x": 6.41, "y": 2.20, "w": 0.50, "h": 0.50 },
    { "type": "icon", "src": "icons/template-media/icon-3.png",
      "x": 10.45, "y": 2.20, "w": 0.50, "h": 0.50 },

    // Column titles
    { "type": "text", "content": "Pillar One",
      "x": 0.80, "y": 2.85, "w": 3.64, "h": 0.50,
      "fontSize": 15, "fontFace": "Source Sans Pro", "color": "033778", "bold": true, "align": "center" },
    { "type": "text", "content": "Pillar Two",
      "x": 4.84, "y": 2.85, "w": 3.64, "h": 0.50,
      "fontSize": 15, "fontFace": "Source Sans Pro", "color": "033778", "bold": true, "align": "center" },
    { "type": "text", "content": "Pillar Three",
      "x": 8.88, "y": 2.85, "w": 3.64, "h": 0.50,
      "fontSize": 15, "fontFace": "Source Sans Pro", "color": "033778", "bold": true, "align": "center" },

    // Column descriptions
    { "type": "text", "content": "Description of the first pillar. Keep to two or three sentences.",
      "x": 0.80, "y": 3.45, "w": 3.64, "h": 3.55,
      "fontSize": 13, "fontFace": "Source Sans Pro", "color": "3C3C3B" },
    { "type": "text", "content": "Description of the second pillar. Parallel in length to column one.",
      "x": 4.84, "y": 3.45, "w": 3.64, "h": 3.55,
      "fontSize": 13, "fontFace": "Source Sans Pro", "color": "3C3C3B" },
    { "type": "text", "content": "Description of the third pillar. Parallel in length to columns one and two.",
      "x": 8.88, "y": 3.45, "w": 3.64, "h": 3.55,
      "fontSize": 13, "fontFace": "Source Sans Pro", "color": "3C3C3B" },

    // Vertical separators
    { "type": "shape", "shape": "line",
      "x": 4.64, "y": 2.10, "w": 0, "h": 4.90,
      "line": { "color": "B1B0B1", "width": 1 } },
    { "type": "shape", "shape": "line",
      "x": 8.68, "y": 2.10, "w": 0, "h": 4.90,
      "line": { "color": "B1B0B1", "width": 1 } }
  ]
}
```

---

## Layout 8 â€” Four column

**Purpose:** Four equal items â€” service lines, locations, team functions, or product pillars.

**Visual:** Same header pattern as the three-column layout. Four equal columns (w=2.63 each) separated by three vertical lines. Use smaller icons (0.45") to maintain breathing room.

**Column x positions:** 0.80, 3.83, 6.86, 9.89
**Separator x positions:** 3.63, 6.66, 9.69
**Icon x positions (centered, 0.45" icon):** 1.89, 4.92, 7.95, 10.98

**Element recipe:**

```json
{
  "slideIndex": 8,
  "background": { "color": "FFFFFF" },
  "footer": true,
  "elements": [
    { "type": "text", "content": "Slide Title",
      "x": 0.80, "y": 0.70, "w": 11.73, "h": 0.70,
      "fontSize": 28, "fontFace": "Source Sans Pro", "color": "033778", "bold": true },
    { "type": "text", "content": "Subtitle",
      "x": 0.80, "y": 1.50, "w": 11.73, "h": 0.45,
      "fontSize": 16, "fontFace": "Source Sans Pro", "color": "3C3C3B" },
    { "type": "shape", "shape": "line",
      "x": 0.80, "y": 2.05, "w": 11.73, "h": 0,
      "line": { "color": "B1B0B1", "width": 1 } },

    // Icons (0.45" square)
    { "type": "icon", "src": "icons/template-media/icon-1.png",
      "x": 1.89, "y": 2.20, "w": 0.45, "h": 0.45 },
    { "type": "icon", "src": "icons/template-media/icon-2.png",
      "x": 4.92, "y": 2.20, "w": 0.45, "h": 0.45 },
    { "type": "icon", "src": "icons/template-media/icon-3.png",
      "x": 7.95, "y": 2.20, "w": 0.45, "h": 0.45 },
    { "type": "icon", "src": "icons/template-media/icon-4.png",
      "x": 10.98, "y": 2.20, "w": 0.45, "h": 0.45 },

    // Column titles (w=2.63, centered)
    { "type": "text", "content": "Item One",
      "x": 0.80, "y": 2.80, "w": 2.63, "h": 0.45,
      "fontSize": 14, "fontFace": "Source Sans Pro", "color": "033778", "bold": true, "align": "center" },
    { "type": "text", "content": "Item Two",
      "x": 3.83, "y": 2.80, "w": 2.63, "h": 0.45,
      "fontSize": 14, "fontFace": "Source Sans Pro", "color": "033778", "bold": true, "align": "center" },
    { "type": "text", "content": "Item Three",
      "x": 6.86, "y": 2.80, "w": 2.63, "h": 0.45,
      "fontSize": 14, "fontFace": "Source Sans Pro", "color": "033778", "bold": true, "align": "center" },
    { "type": "text", "content": "Item Four",
      "x": 9.89, "y": 2.80, "w": 2.63, "h": 0.45,
      "fontSize": 14, "fontFace": "Source Sans Pro", "color": "033778", "bold": true, "align": "center" },

    // Descriptions
    { "type": "text", "content": "Description one.",
      "x": 0.80, "y": 3.35, "w": 2.63, "h": 3.65,
      "fontSize": 12, "fontFace": "Source Sans Pro", "color": "3C3C3B" },
    { "type": "text", "content": "Description two.",
      "x": 3.83, "y": 3.35, "w": 2.63, "h": 3.65,
      "fontSize": 12, "fontFace": "Source Sans Pro", "color": "3C3C3B" },
    { "type": "text", "content": "Description three.",
      "x": 6.86, "y": 3.35, "w": 2.63, "h": 3.65,
      "fontSize": 12, "fontFace": "Source Sans Pro", "color": "3C3C3B" },
    { "type": "text", "content": "Description four.",
      "x": 9.89, "y": 3.35, "w": 2.63, "h": 3.65,
      "fontSize": 12, "fontFace": "Source Sans Pro", "color": "3C3C3B" },

    // Vertical separators
    { "type": "shape", "shape": "line",
      "x": 3.63, "y": 2.10, "w": 0, "h": 4.90,
      "line": { "color": "B1B0B1", "width": 1 } },
    { "type": "shape", "shape": "line",
      "x": 6.66, "y": 2.10, "w": 0, "h": 4.90,
      "line": { "color": "B1B0B1", "width": 1 } },
    { "type": "shape", "shape": "line",
      "x": 9.69, "y": 2.10, "w": 0, "h": 4.90,
      "line": { "color": "B1B0B1", "width": 1 } }
  ]
}
```

---

## Layout 9 â€” Five-step horizontal process flow

**Purpose:** Linear process, roadmap, or lifecycle with five numbered stages. Use for delivery models, transformation journeys, or service sequences.

**Visual:** Title and subtitle at top. Five ERNI blue filled circles (numbered 1â€“5) run horizontally across the center of the slide, connected by blue horizontal lines. Step titles and descriptions sit below each circle.

**Key coordinates:**

| element | slot 1 | slot 2 | slot 3 | slot 4 | slot 5 |
|---|---|---|---|---|---|
| circle x (w=0.65) | 1.00 | 3.67 | 6.34 | 9.00 | 11.67 |
| circle y | 2.80 | 2.80 | 2.80 | 2.80 | 2.80 |
| connector x (from) | 1.65 | 4.32 | 6.99 | 9.65 | â€” |
| connector w | 2.02 | 2.02 | 2.01 | 2.02 | â€” |
| step title x (w=2.0) | 0.33 | 3.00 | 5.67 | 8.33 | 11.00 |
| desc x (w=2.0) | 0.33 | 3.00 | 5.67 | 8.33 | 11.00 |

Connector y = 3.125 (vertical center of circles: y + h/2 = 2.80 + 0.325).

**Element recipe:**

```json
{
  "slideIndex": 9,
  "background": { "color": "FFFFFF" },
  "footer": true,
  "elements": [
    { "type": "text", "content": "Process Title",
      "x": 0.80, "y": 0.70, "w": 11.73, "h": 0.65,
      "fontSize": 26, "fontFace": "Source Sans Pro", "color": "033778", "bold": true },
    { "type": "text", "content": "Subtitle describing the five stages",
      "x": 0.80, "y": 1.45, "w": 11.73, "h": 0.40,
      "fontSize": 15, "fontFace": "Source Sans Pro", "color": "3C3C3B" },

    // â€” Circles (filled ellipses) â€”
    { "type": "shape", "shape": "ellipse", "fill": "033778",
      "x": 1.00, "y": 2.80, "w": 0.65, "h": 0.65 },
    { "type": "shape", "shape": "ellipse", "fill": "033778",
      "x": 3.67, "y": 2.80, "w": 0.65, "h": 0.65 },
    { "type": "shape", "shape": "ellipse", "fill": "033778",
      "x": 6.34, "y": 2.80, "w": 0.65, "h": 0.65 },
    { "type": "shape", "shape": "ellipse", "fill": "033778",
      "x": 9.00, "y": 2.80, "w": 0.65, "h": 0.65 },
    { "type": "shape", "shape": "ellipse", "fill": "033778",
      "x": 11.67, "y": 2.80, "w": 0.65, "h": 0.65 },

    // â€” Step numbers (white, centered over circles) â€”
    { "type": "text", "content": "1",
      "x": 1.00, "y": 2.80, "w": 0.65, "h": 0.65,
      "fontSize": 14, "fontFace": "Source Sans Pro",
      "color": "FFFFFF", "bold": true, "align": "center", "valign": "middle" },
    { "type": "text", "content": "2",
      "x": 3.67, "y": 2.80, "w": 0.65, "h": 0.65,
      "fontSize": 14, "fontFace": "Source Sans Pro",
      "color": "FFFFFF", "bold": true, "align": "center", "valign": "middle" },
    { "type": "text", "content": "3",
      "x": 6.34, "y": 2.80, "w": 0.65, "h": 0.65,
      "fontSize": 14, "fontFace": "Source Sans Pro",
      "color": "FFFFFF", "bold": true, "align": "center", "valign": "middle" },
    { "type": "text", "content": "4",
      "x": 9.00, "y": 2.80, "w": 0.65, "h": 0.65,
      "fontSize": 14, "fontFace": "Source Sans Pro",
      "color": "FFFFFF", "bold": true, "align": "center", "valign": "middle" },
    { "type": "text", "content": "5",
      "x": 11.67, "y": 2.80, "w": 0.65, "h": 0.65,
      "fontSize": 14, "fontFace": "Source Sans Pro",
      "color": "FFFFFF", "bold": true, "align": "center", "valign": "middle" },

    // â€” Connector lines (erniBlue, y at circle vertical center) â€”
    { "type": "shape", "shape": "line",
      "x": 1.65, "y": 3.125, "w": 2.02, "h": 0,
      "line": { "color": "033778", "width": 2 } },
    { "type": "shape", "shape": "line",
      "x": 4.32, "y": 3.125, "w": 2.02, "h": 0,
      "line": { "color": "033778", "width": 2 } },
    { "type": "shape", "shape": "line",
      "x": 6.99, "y": 3.125, "w": 2.01, "h": 0,
      "line": { "color": "033778", "width": 2 } },
    { "type": "shape", "shape": "line",
      "x": 9.65, "y": 3.125, "w": 2.02, "h": 0,
      "line": { "color": "033778", "width": 2 } },

    // â€” Step titles (centered below each circle, w=2.0) â€”
    { "type": "text", "content": "Step One",
      "x": 0.33, "y": 3.60, "w": 2.00, "h": 0.50,
      "fontSize": 14, "fontFace": "Source Sans Pro",
      "color": "033778", "bold": true, "align": "center" },
    { "type": "text", "content": "Step Two",
      "x": 3.00, "y": 3.60, "w": 2.00, "h": 0.50,
      "fontSize": 14, "fontFace": "Source Sans Pro",
      "color": "033778", "bold": true, "align": "center" },
    { "type": "text", "content": "Step Three",
      "x": 5.67, "y": 3.60, "w": 2.00, "h": 0.50,
      "fontSize": 14, "fontFace": "Source Sans Pro",
      "color": "033778", "bold": true, "align": "center" },
    { "type": "text", "content": "Step Four",
      "x": 8.33, "y": 3.60, "w": 2.00, "h": 0.50,
      "fontSize": 14, "fontFace": "Source Sans Pro",
      "color": "033778", "bold": true, "align": "center" },
    { "type": "text", "content": "Step Five",
      "x": 11.00, "y": 3.60, "w": 2.00, "h": 0.50,
      "fontSize": 14, "fontFace": "Source Sans Pro",
      "color": "033778", "bold": true, "align": "center" },

    // â€” Step descriptions (centered, w=2.0) â€”
    { "type": "text", "content": "Brief description of step one.",
      "x": 0.33, "y": 4.20, "w": 2.00, "h": 2.80,
      "fontSize": 12, "fontFace": "Source Sans Pro",
      "color": "3C3C3B", "align": "center", "valign": "top" },
    { "type": "text", "content": "Brief description of step two.",
      "x": 3.00, "y": 4.20, "w": 2.00, "h": 2.80,
      "fontSize": 12, "fontFace": "Source Sans Pro",
      "color": "3C3C3B", "align": "center", "valign": "top" },
    { "type": "text", "content": "Brief description of step three.",
      "x": 5.67, "y": 4.20, "w": 2.00, "h": 2.80,
      "fontSize": 12, "fontFace": "Source Sans Pro",
      "color": "3C3C3B", "align": "center", "valign": "top" },
    { "type": "text", "content": "Brief description of step four.",
      "x": 8.33, "y": 4.20, "w": 2.00, "h": 2.80,
      "fontSize": 12, "fontFace": "Source Sans Pro",
      "color": "3C3C3B", "align": "center", "valign": "top" },
    { "type": "text", "content": "Brief description of step five.",
      "x": 11.00, "y": 4.20, "w": 2.00, "h": 2.80,
      "fontSize": 12, "fontFace": "Source Sans Pro",
      "color": "3C3C3B", "align": "center", "valign": "top" }
  ]
}
```

---

## Layout 10 â€” KPI grid 2Ã—3

**Purpose:** Display six headline metrics, facts, or figures. Use for executive dashboards, capability summaries, or fact sheets.

**Visual:** Slide title at the top. Six equal cards in two rows of three, each with a large bold value, an optional unit, and a label.

**Card geometry:**
- Card size: w=3.71, h=2.70
- Row 1 y=1.50, Row 2 y=4.45
- Column x positions: 0.80, 4.81, 8.82
- Gap between columns: 0.30
- Gap between rows: 0.25

**Element recipe (showing one card â€” replicate the card bg + value + label blocks for all six):**

```json
{
  "slideIndex": 10,
  "background": { "color": "FFFFFF" },
  "footer": true,
  "elements": [
    { "type": "text", "content": "Key Performance Indicators",
      "x": 0.80, "y": 0.70, "w": 11.73, "h": 0.65,
      "fontSize": 28, "fontFace": "Source Sans Pro", "color": "033778", "bold": true },

    // â€” Card 1 (row 1, col 1) â€”
    { "type": "shape", "shape": "rect",
      "x": 0.80, "y": 1.50, "w": 3.71, "h": 2.70, "fill": "EEEEEE" },
    { "type": "text", "content": "94%",
      "x": 1.00, "y": 1.80, "w": 3.31, "h": 1.05,
      "fontSize": 42, "fontFace": "Source Sans Pro",
      "color": "033778", "bold": true, "align": "center" },
    { "type": "text", "content": "Client Satisfaction",
      "x": 1.00, "y": 2.90, "w": 3.31, "h": 0.55,
      "fontSize": 13, "fontFace": "Source Sans Pro",
      "color": "3C3C3B", "align": "center" },

    // â€” Card 2 (row 1, col 2) â€”
    { "type": "shape", "shape": "rect",
      "x": 4.81, "y": 1.50, "w": 3.71, "h": 2.70, "fill": "EEEEEE" },
    { "type": "text", "content": "12K",
      "x": 5.01, "y": 1.80, "w": 3.31, "h": 1.05,
      "fontSize": 42, "fontFace": "Source Sans Pro",
      "color": "033778", "bold": true, "align": "center" },
    { "type": "text", "content": "Employees Worldwide",
      "x": 5.01, "y": 2.90, "w": 3.31, "h": 0.55,
      "fontSize": 13, "fontFace": "Source Sans Pro",
      "color": "3C3C3B", "align": "center" },

    // â€” Card 3 (row 1, col 3) â€”
    { "type": "shape", "shape": "rect",
      "x": 8.82, "y": 1.50, "w": 3.71, "h": 2.70, "fill": "EEEEEE" },
    { "type": "text", "content": "30+",
      "x": 9.02, "y": 1.80, "w": 3.31, "h": 1.05,
      "fontSize": 42, "fontFace": "Source Sans Pro",
      "color": "033778", "bold": true, "align": "center" },
    { "type": "text", "content": "Countries",
      "x": 9.02, "y": 2.90, "w": 3.31, "h": 0.55,
      "fontSize": 13, "fontFace": "Source Sans Pro",
      "color": "3C3C3B", "align": "center" },

    // â€” Card 4 (row 2, col 1) â€”
    { "type": "shape", "shape": "rect",
      "x": 0.80, "y": 4.45, "w": 3.71, "h": 2.70, "fill": "EEEEEE" },
    { "type": "text", "content": "â‚¬2.1B",
      "x": 1.00, "y": 4.75, "w": 3.31, "h": 1.05,
      "fontSize": 42, "fontFace": "Source Sans Pro",
      "color": "033778", "bold": true, "align": "center" },
    { "type": "text", "content": "Annual Revenue",
      "x": 1.00, "y": 5.85, "w": 3.31, "h": 0.55,
      "fontSize": 13, "fontFace": "Source Sans Pro",
      "color": "3C3C3B", "align": "center" },

    // â€” Card 5 (row 2, col 2) â€” repeat pattern â€”
    { "type": "shape", "shape": "rect",
      "x": 4.81, "y": 4.45, "w": 3.71, "h": 2.70, "fill": "EEEEEE" },
    { "type": "text", "content": "98%",
      "x": 5.01, "y": 4.75, "w": 3.31, "h": 1.05,
      "fontSize": 42, "fontFace": "Source Sans Pro",
      "color": "033778", "bold": true, "align": "center" },
    { "type": "text", "content": "On-Time Delivery",
      "x": 5.01, "y": 5.85, "w": 3.31, "h": 0.55,
      "fontSize": 13, "fontFace": "Source Sans Pro",
      "color": "3C3C3B", "align": "center" },

    // â€” Card 6 (row 2, col 3) â€” repeat pattern â€”
    { "type": "shape", "shape": "rect",
      "x": 8.82, "y": 4.45, "w": 3.71, "h": 2.70, "fill": "EEEEEE" },
    { "type": "text", "content": "ISO",
      "x": 9.02, "y": 4.75, "w": 3.31, "h": 1.05,
      "fontSize": 42, "fontFace": "Source Sans Pro",
      "color": "033778", "bold": true, "align": "center" },
    { "type": "text", "content": "27001 Certified",
      "x": 9.02, "y": 5.85, "w": 3.31, "h": 0.55,
      "fontSize": 13, "fontFace": "Source Sans Pro",
      "color": "3C3C3B", "align": "center" }
  ]
}
```

---

## Layout 11 â€” People / team grid

**Purpose:** Introduce team members, project leads, or client stakeholders. Use only when headshots and role descriptions are available.

**Visual:** Slide title at the top. Four equal portrait cards in a horizontal row. Each card contains a headshot, name, role, department, and a short bio.

**Card geometry (4 people):**
- Card size: w=2.60, h=5.70
- Column x positions: 0.80, 3.84, 6.88, 9.92
- Gap between columns: 0.44
- Photo area: y=1.50, h=2.60 (square, same width as card)

**Element recipe:**

```json
{
  "slideIndex": 11,
  "background": { "color": "FFFFFF" },
  "footer": true,
  "elements": [
    { "type": "text", "content": "Our Team",
      "x": 0.80, "y": 0.70, "w": 11.73, "h": 0.65,
      "fontSize": 28, "fontFace": "Source Sans Pro", "color": "033778", "bold": true },

    // â€” Person 1 â€”
    // Photo placeholder background (replace with actual headshot image element)
    { "type": "shape", "shape": "rect",
      "x": 0.80, "y": 1.50, "w": 2.60, "h": 2.60, "fill": "B1B0B1" },
    // Actual headshot (add when src is available):
    // { "type": "image", "src": "images/headshot-person1.jpg",
    //   "x": 0.80, "y": 1.50, "w": 2.60, "h": 2.60,
    //   "sizing": { "type": "cover", "w": 2.60, "h": 2.60 } },
    { "type": "text", "content": "Full Name",
      "x": 0.80, "y": 4.25, "w": 2.60, "h": 0.45,
      "fontSize": 15, "fontFace": "Source Sans Pro", "color": "033778", "bold": true, "align": "center" },
    { "type": "text", "content": "Job Title",
      "x": 0.80, "y": 4.80, "w": 2.60, "h": 0.40,
      "fontSize": 13, "fontFace": "Source Sans Pro", "color": "3C3C3B", "align": "center" },
    { "type": "text", "content": "Department Â· Location",
      "x": 0.80, "y": 5.30, "w": 2.60, "h": 0.35,
      "fontSize": 12, "fontFace": "Source Sans Pro", "color": "B1B0B1", "align": "center" },
    { "type": "text", "content": "One or two sentences about the person's expertise and role on the project.",
      "x": 0.80, "y": 5.75, "w": 2.60, "h": 1.20,
      "fontSize": 11, "fontFace": "Source Sans Pro", "color": "3C3C3B" },

    // â€” Person 2 â€” (repeat at x=3.84) â€”
    { "type": "shape", "shape": "rect",
      "x": 3.84, "y": 1.50, "w": 2.60, "h": 2.60, "fill": "B1B0B1" },
    { "type": "text", "content": "Full Name",
      "x": 3.84, "y": 4.25, "w": 2.60, "h": 0.45,
      "fontSize": 15, "fontFace": "Source Sans Pro", "color": "033778", "bold": true, "align": "center" },
    { "type": "text", "content": "Job Title",
      "x": 3.84, "y": 4.80, "w": 2.60, "h": 0.40,
      "fontSize": 13, "fontFace": "Source Sans Pro", "color": "3C3C3B", "align": "center" },
    { "type": "text", "content": "Department Â· Location",
      "x": 3.84, "y": 5.30, "w": 2.60, "h": 0.35,
      "fontSize": 12, "fontFace": "Source Sans Pro", "color": "B1B0B1", "align": "center" },
    { "type": "text", "content": "One or two sentences about the person's expertise.",
      "x": 3.84, "y": 5.75, "w": 2.60, "h": 1.20,
      "fontSize": 11, "fontFace": "Source Sans Pro", "color": "3C3C3B" },

    // â€” Person 3 â€” (repeat at x=6.88) â€”
    { "type": "shape", "shape": "rect",
      "x": 6.88, "y": 1.50, "w": 2.60, "h": 2.60, "fill": "B1B0B1" },
    { "type": "text", "content": "Full Name",
      "x": 6.88, "y": 4.25, "w": 2.60, "h": 0.45,
      "fontSize": 15, "fontFace": "Source Sans Pro", "color": "033778", "bold": true, "align": "center" },
    { "type": "text", "content": "Job Title",
      "x": 6.88, "y": 4.80, "w": 2.60, "h": 0.40,
      "fontSize": 13, "fontFace": "Source Sans Pro", "color": "3C3C3B", "align": "center" },
    { "type": "text", "content": "Department Â· Location",
      "x": 6.88, "y": 5.30, "w": 2.60, "h": 0.35,
      "fontSize": 12, "fontFace": "Source Sans Pro", "color": "B1B0B1", "align": "center" },
    { "type": "text", "content": "One or two sentences about the person's expertise.",
      "x": 6.88, "y": 5.75, "w": 2.60, "h": 1.20,
      "fontSize": 11, "fontFace": "Source Sans Pro", "color": "3C3C3B" },

    // â€” Person 4 â€” (repeat at x=9.92) â€”
    { "type": "shape", "shape": "rect",
      "x": 9.92, "y": 1.50, "w": 2.60, "h": 2.60, "fill": "B1B0B1" },
    { "type": "text", "content": "Full Name",
      "x": 9.92, "y": 4.25, "w": 2.60, "h": 0.45,
      "fontSize": 15, "fontFace": "Source Sans Pro", "color": "033778", "bold": true, "align": "center" },
    { "type": "text", "content": "Job Title",
      "x": 9.92, "y": 4.80, "w": 2.60, "h": 0.40,
      "fontSize": 13, "fontFace": "Source Sans Pro", "color": "3C3C3B", "align": "center" },
    { "type": "text", "content": "Department Â· Location",
      "x": 9.92, "y": 5.30, "w": 2.60, "h": 0.35,
      "fontSize": 12, "fontFace": "Source Sans Pro", "color": "B1B0B1", "align": "center" },
    { "type": "text", "content": "One or two sentences about the person's expertise.",
      "x": 9.92, "y": 5.75, "w": 2.60, "h": 1.20,
      "fontSize": 11, "fontFace": "Source Sans Pro", "color": "3C3C3B" }
  ]
}
```

---

## Layout 12 â€” Closing / back cover: blue

**Purpose:** Final slide of the deck. Leaves the audience with a closing message, tagline, and contact details. Use ERNI blue for maximum brand impact.

**Visual:** Full ERNI blue canvas. Large white closing headline centered vertically. A thin cyan horizontal rule separates the headline from the tagline below. Contact URL or CTA line in white near the bottom.

**Element recipe:**

```json
{
  "slideIndex": 12,
  "background": { "color": "033778" },
  "footer": false,
  "elements": [
    // Full blue background (belt-and-braces â€” background.color above is sufficient,
    // but add the rect if a gradient band is desired over part of the slide)

    // Closing headline
    { "type": "text", "content": "Thank You",
      "x": 1.50, "y": 2.20, "w": 10.33, "h": 1.50,
      "fontSize": 40, "fontFace": "Source Sans Pro",
      "color": "FFFFFF", "bold": true,
      "align": "center", "valign": "middle" },

    // Cyan accent rule
    { "type": "shape", "shape": "line",
      "x": 3.67, "y": 3.85, "w": 6.00, "h": 0,
      "line": { "color": "00AADB", "width": 2 } },

    // Tagline or key closing message
    { "type": "text", "content": "Better ask ERNI.",
      "x": 1.50, "y": 4.05, "w": 10.33, "h": 0.70,
      "fontSize": 20, "fontFace": "Source Sans Pro",
      "color": "00AADB", "align": "center" },

    // Contact / URL
    { "type": "text", "content": "contact@erni.ch  Â·  www.erni.ch",
      "x": 1.50, "y": 5.60, "w": 10.33, "h": 0.50,
      "fontSize": 14, "fontFace": "Source Sans Pro",
      "color": "FFFFFF", "align": "center" }
  ]
}
```

---

## Layout selection guide

| slide intent | use layout |
|---|---|
| opening with hero image | Layout 1 â€” Cover (hero image right half) |
| opening, conservative or no image | Layout 2 â€” Cover (text only, white) |
| chapter break | Layout 3 â€” Section divider (blue) |
| prose-heavy analysis or recommendation | Layout 4 â€” Narrative / full text |
| parallel themes, compare/contrast | Layout 5 â€” Two column text |
| visual evidence + explanation | Layout 6 â€” Image left + text right |
| three service lines, values, or principles | Layout 7 â€” Three column (icons) |
| four capabilities, locations, or domains | Layout 8 â€” Four column |
| roadmap, delivery model, lifecycle | Layout 9 â€” Five-step process flow |
| dashboard, facts, headline numbers | Layout 10 â€” KPI grid 2Ã—3 |
| team introduction | Layout 11 â€” People / team grid |
| final slide | Layout 12 â€” Closing / back cover (blue) |
```

---