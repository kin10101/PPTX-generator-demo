# Data Visualisation Patterns

This section provides concrete element recipes for common data and metric display components. Each pattern is self-contained and can be placed anywhere on a slide by adjusting the anchor `x`/`y` values. All coordinates are in inches on the 13.33 Ã— 7.5 inch canvas.

### Color conventions for data visualisation

| signal | hex | use |
|---|---|---|
| ERNI blue | `033778` | primary value, progress fill, neutral indicator |
| cyan | `00AADB` | positive trend, secondary metric |
| health green | `27AE60` | score > 70, passing, on-track |
| health amber | `E67E22` | score 50â€“70, at-risk, partial |
| health red | `C0392B` | score < 50, failing, critical |
| card background | `EEEEEE` | neutral tile background |
| track background | `DDDDDD` | unfilled portion of a progress bar |

---

### Pattern 1 â€” KPI tile

**Purpose:** Display a single headline metric in a self-contained card. Stack or grid multiple tiles to create a dashboard row or 2Ã—3 KPI grid (see Layout 10).

**Structure:** Light gray card rectangle. Large bold value centered in the upper portion. Optional small unit label. Plain label text beneath.

**Anchor:** The card origin is `(card_x, card_y)`. Default card size is w=3.71, h=2.70. Adjust as needed.

```json
[
  // Card background
  { "type": "shape", "shape": "rect",
    "x": 0.80, "y": 1.50, "w": 3.71, "h": 2.70,
    "fill": "EEEEEE" },

  // Large metric value
  { "type": "text", "content": "94%",
    "x": 1.00, "y": 1.75, "w": 3.31, "h": 1.10,
    "fontSize": 44, "fontFace": "Source Sans Pro",
    "color": "033778", "bold": true,
    "align": "center", "valign": "middle" },

  // Metric label
  { "type": "text", "content": "Client Satisfaction Score",
    "x": 1.00, "y": 2.90, "w": 3.31, "h": 0.55,
    "fontSize": 13, "fontFace": "Source Sans Pro",
    "color": "3C3C3B", "align": "center" },

  // Optional: thin ERNI blue bottom accent bar
  { "type": "shape", "shape": "rect",
    "x": 0.80, "y": 4.00, "w": 3.71, "h": 0.18,
    "fill": "033778" }
]
```

**Variants:**
- For currency values (e.g. `â‚¬2.1B`), encode the unit inside the `content` string.
- For a trend indicator, add a small text element directly below the label using green (`27AE60`) for positive and red (`C0392B`) for negative: `"content": "â–² +3 pts vs last quarter"`, fontSize 11.
- To highlight a KPI, change `fill` of the card rect to `033778` and all text `color` values to `FFFFFF` or `00AADB`.

---

### Pattern 2 â€” Health / status badge

**Purpose:** Indicate the health or compliance state of a system, project, or metric at a glance. The fill color is chosen programmatically based on the score value.

**Color rule:**
- Score < 50 â†’ fill `C0392B` (red)
- Score 50â€“70 â†’ fill `E67E22` (amber)
- Score > 70 â†’ fill `27AE60` (green)

**Structure:** A colored rectangle. The numeric score overlaid in large white bold text in the upper center. A short status label in smaller white text below.

**Default size:** w=1.80, h=1.00. Adjust height to 1.30 if a status word is included.

```json
[
  // Status badge rectangle â€” color is chosen based on score
  // Example: score = 78 â†’ green
  { "type": "shape", "shape": "rect",
    "x": 0.80, "y": 2.00, "w": 1.80, "h": 1.10,
    "fill": "27AE60" },

  // Score number overlay
  { "type": "text", "content": "78",
    "x": 0.80, "y": 2.00, "w": 1.80, "h": 0.70,
    "fontSize": 26, "fontFace": "Source Sans Pro",
    "color": "FFFFFF", "bold": true,
    "align": "center", "valign": "middle" },

  // Status label
  { "type": "text", "content": "HEALTHY",
    "x": 0.80, "y": 2.72, "w": 1.80, "h": 0.28,
    "fontSize": 10, "fontFace": "Source Sans Pro",
    "color": "FFFFFF", "bold": true,
    "align": "center", "valign": "middle" }
]
```

**Usage notes:**
- Place the badge flush left of the metric label it describes.
- For a row of multiple badges, space them with 0.20" gaps.
- To include a domain name, add a text element above the badge at fontSize 12, color 3C3C3B.

---

### Pattern 3 â€” Progress bar

**Purpose:** Show percentage completion, budget utilisation, or any bounded 0â€“100% metric visually.

**Structure:** A light gray full-width track rectangle. A colored foreground rectangle whose width is `track_w Ã— (percentage / 100)`. A label to the left and a value to the right of the track.

**Default track:** x=2.20, y=varies, w=8.00, h=0.30
**Foreground width formula:** `foreground_w = 8.00 Ã— (pct / 100)`

**Color rule for foreground fill:** use the same health color scale as the status badge (red/amber/green) or use ERNI blue `033778` for a neutral style.

```json
[
  // Row label (left of bar)
  { "type": "text", "content": "Sprint Completion",
    "x": 0.80, "y": 3.10, "w": 1.25, "h": 0.30,
    "fontSize": 12, "fontFace": "Source Sans Pro",
    "color": "3C3C3B", "valign": "middle" },

  // Track background (full width = 8.00")
  { "type": "shape", "shape": "rect",
    "x": 2.20, "y": 3.10, "w": 8.00, "h": 0.30,
    "fill": "DDDDDD" },

  // Foreground fill â€” width = 8.00 Ã— (72 / 100) = 5.76 for 72%
  { "type": "shape", "shape": "rect",
    "x": 2.20, "y": 3.10, "w": 5.76, "h": 0.30,
    "fill": "27AE60" },

  // Percentage value (right of bar)
  { "type": "text", "content": "72%",
    "x": 10.35, "y": 3.10, "w": 0.80, "h": 0.30,
    "fontSize": 12, "fontFace": "Source Sans Pro",
    "color": "033778", "bold": true,
    "align": "right", "valign": "middle" }
]
```

**Stacking multiple bars:** Repeat the four-element group, incrementing `y` by `0.55` per row. This gives a clean 0.25" gap between bars. A slide can comfortably hold 8â€“10 rows within the content zone.

**Thin rule between groups:** Insert a `shape line` with `line: { color: "B1B0B1", width: 1 }` between logical groupings.

---

### Pattern 4 â€” Metric comparison row

**Purpose:** Present a list of named metrics side-by-side with their values â€” useful for benchmarks, SLA tables, and scorecard rows. Each row shows an icon, a label, and a right-aligned value.

**Structure (horizontal, one row):**
- Small icon at far left
- Label text spanning the middle
- Bold value right-aligned at the far right

**Default row height:** 0.45". Increment `y` by 0.50" per additional row.

```json
[
  // â€” Row 1 â€”
  { "type": "icon", "src": "icons/template-media/icon-uptime.png",
    "x": 0.80, "y": 2.50, "w": 0.38, "h": 0.38 },

  { "type": "text", "content": "System Uptime (last 30 days)",
    "x": 1.30, "y": 2.50, "w": 8.00, "h": 0.40,
    "fontSize": 13, "fontFace": "Source Sans Pro",
    "color": "3C3C3B", "valign": "middle" },

  { "type": "text", "content": "99.97%",
    "x": 9.50, "y": 2.50, "w": 2.53, "h": 0.40,
    "fontSize": 14, "fontFace": "Source Sans Pro",
    "color": "033778", "bold": true,
    "align": "right", "valign": "middle" },

  // â€” Row 2 â€”
  { "type": "icon", "src": "icons/template-media/icon-incidents.png",
    "x": 0.80, "y": 3.00, "w": 0.38, "h": 0.38 },

  { "type": "text", "content": "P1 Incidents Resolved < 1 Hour",
    "x": 1.30, "y": 3.00, "w": 8.00, "h": 0.40,
    "fontSize": 13, "fontFace": "Source Sans Pro",
    "color": "3C3C3B", "valign": "middle" },

  { "type": "text", "content": "14 / 14",
    "x": 9.50, "y": 3.00, "w": 2.53, "h": 0.40,
    "fontSize": 14, "fontFace": "Source Sans Pro",
    "color": "27AE60", "bold": true,
    "align": "right", "valign": "middle" },

  // â€” Separator rule between sections â€”
  { "type": "shape", "shape": "line",
    "x": 0.80, "y": 3.48, "w": 11.73, "h": 0,
    "line": { "color": "B1B0B1", "width": 1 } },

  // â€” Row 3 (after rule) â€”
  { "type": "icon", "src": "icons/template-media/icon-budget.png",
    "x": 0.80, "y": 3.58, "w": 0.38, "h": 0.38 },

  { "type": "text", "content": "Budget Utilisation YTD",
    "x": 1.30, "y": 3.58, "w": 8.00, "h": 0.40,
    "fontSize": 13, "fontFace": "Source Sans Pro",
    "color": "3C3C3B", "valign": "middle" },

  { "type": "text", "content": "â‚¬1.24M / â‚¬1.60M",
    "x": 9.50, "y": 3.58, "w": 2.53, "h": 0.40,
    "fontSize": 14, "fontFace": "Source Sans Pro",
    "color": "E67E22", "bold": true,
    "align": "right", "valign": "middle" }
]
```

**Usage notes:**
- Use the value color to encode health: `27AE60` (green) for on-target, `E67E22` (amber) for at-risk, `C0392B` (red) for breached, `033778` (blue) for neutral.
- If icons are not available for every row, omit the icon element and set the label `x` to `0.80`.
- Combine with a progress bar (Pattern 3) on the same row by reducing the label width and placing the bar in the middle column.

---

### Pattern 5 â€” Alert callout

**Purpose:** Draw attention to a finding, risk, action item, or note. A colored left-border strip signals severity. Use sparingly â€” one or two callouts per slide maximum.

**Severity color rule:**
- Informational / note â†’ left border `033778` (ERNI blue)
- Warning / at-risk â†’ left border `E67E22` (amber)
- Critical / blocker â†’ left border `C0392B` (red)
- Success / resolved â†’ left border `27AE60` (green)

**Structure:** A light gray background rectangle spans the full callout area. A narrow colored rectangle overlays the left edge (the "border strip"). Title text and body text sit inside with a left indent.

**Default size:** w=9.00, h=1.50. Increase h for longer body text.

```json
[
  // â€” Callout 1: Critical risk â€”

  // Background rectangle
  { "type": "shape", "shape": "rect",
    "x": 0.80, "y": 2.00, "w": 9.00, "h": 1.50,
    "fill": "EEEEEE" },

  // Left border strip (colored by severity: red = critical)
  { "type": "shape", "shape": "rect",
    "x": 0.80, "y": 2.00, "w": 0.12, "h": 1.50,
    "fill": "C0392B" },

  // Callout title
  { "type": "text", "content": "Risk: Third-Party Dependency on Legacy API",
    "x": 1.10, "y": 2.10, "w": 8.50, "h": 0.45,
    "fontSize": 14, "fontFace": "Source Sans Pro",
    "color": "3C3C3B", "bold": true },

  // Callout body
  { "type": "text", "content": "The legacy payment API reaches end-of-life in Q3. Migration must begin by end of sprint 12 to avoid a release-blocking dependency. Owner: Platform team.",
    "x": 1.10, "y": 2.62, "w": 8.50, "h": 0.75,
    "fontSize": 12, "fontFace": "Source Sans Pro",
    "color": "3C3C3B", "valign": "top" },

  // â€” Callout 2: Informational note (stacked below, gap = 0.20") â€”

  { "type": "shape", "shape": "rect",
    "x": 0.80, "y": 3.70, "w": 9.00, "h": 1.20,
    "fill": "EEEEEE" },

  { "type": "shape", "shape": "rect",
    "x": 0.80, "y": 3.70, "w": 0.12, "h": 1.20,
    "fill": "033778" },

  { "type": "text", "content": "Note: Scope confirmed with client on 2026-05-28",
    "x": 1.10, "y": 3.80, "w": 8.50, "h": 0.40,
    "fontSize": 14, "fontFace": "Source Sans Pro",
    "color": "3C3C3B", "bold": true },

  { "type": "text", "content": "All items in this sprint were formally signed off. Change requests must go through the CCB.",
    "x": 1.10, "y": 4.27, "w": 8.50, "h": 0.50,
    "fontSize": 12, "fontFace": "Source Sans Pro",
    "color": "3C3C3B", "valign": "top" }
]
```

**Usage notes:**
- Stack multiple callouts by incrementing `y` by `callout_height + 0.20`.
- For a wider callout that spans the full content zone, set `w` to `11.73` and adjust inner text `w` to `11.43`.
- Never place a callout within the footer zone (y < 0.60) or below y=7.20.
- If the callout is the primary content of a slide, pair it with the Narrative layout header (Layout 4) above it.
```

---

### Critical Files for Implementation

- `/c/Users/extpedj/Desktop/PPTX-generator-demo/skill/erni-powerpoint-builder/references/layout_catalog.md`
- `/c/Users/extpedj/Desktop/PPTX-generator-demo/skill/erni-powerpoint-builder/references/template_pattern_guide.md`
- `/c/Users/extpedj/Desktop/PPTX-generator-demo/renderer/src/types/slideSpec.ts`
- `/c/Users/extpedj/Desktop/PPTX-generator-demo/renderer/src/config/theme.ts`
- `/c/Users/extpedj/Desktop/PPTX-generator-demo/renderer/test-spec.json`