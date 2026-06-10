import os
import json
import subprocess
import httpx
from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI
from langsmith.wrappers import wrap_openai
from langgraph.graph import StateGraph, END
from state import AgentState

client = wrap_openai(OpenAI())
SKILL_DIR = "./skill"
RENDERER_URL = os.environ.get("RENDERER_URL", "http://localhost:3001")
LLM_MODEL = os.environ.get("LLM_MODEL", "gpt-4o")
LLM_TEMPERATURE = float(os.environ.get("LLM_TEMPERATURE", "")) if os.environ.get("LLM_TEMPERATURE") else None

IMAGES_DIR = "./skill/erni-powerpoint-builder/assets/images"
ICONS_DIR = "./skill/erni-powerpoint-builder/assets/icons/template-media"

AVAILABLE_IMAGES = [f for f in os.listdir(IMAGES_DIR) if f.endswith(('.jpg', '.png'))] if os.path.isdir(IMAGES_DIR) else []
AVAILABLE_ICONS = [f for f in os.listdir(ICONS_DIR) if f.endswith(('.svg', '.png', '.jpeg'))] if os.path.isdir(ICONS_DIR) else []

ELEMENT_SCHEMA = """Each slide has an "elements" array. Each element is one of:

1. TEXT element:
   { "type": "text", "content": "...", "x": <inches>, "y": <inches>, "w": <inches>, "h": <inches>,
     "fontSize": <number>, "fontFace": "Source Sans Pro", "color": "<hex without #>",
     "bold": true/false, "align": "left"|"center"|"right", "valign": "top"|"middle"|"bottom" }

2. IMAGE element:
   { "type": "image", "src": "images/<filename>", "x": <inches>, "y": <inches>, "w": <inches>, "h": <inches>,
     "sizing": { "type": "cover", "w": <inches>, "h": <inches> } }

3. SHAPE element:
   { "type": "shape", "shape": "rect"|"ellipse"|"line", "x": <inches>, "y": <inches>, "w": <inches>, "h": <inches>,
     "fill": "<hex>", "line": { "color": "<hex>", "width": <number> }, "rectRadius": <number> }

4. ICON element:
   { "type": "icon", "src": "icons/template-media/<filename>", "x": <inches>, "y": <inches>, "w": <inches>, "h": <inches> }
"""


# ============================================
# Skill Discovery & Selection
# ============================================

def discover_skills(state: AgentState) -> AgentState:
    """Walk the skills folder and build a registry."""
    registry = []
    for skill_name in os.listdir(SKILL_DIR):
        skill_path = os.path.join(SKILL_DIR, skill_name)
        skill_md = os.path.join(skill_path, "SKILL.md")
        if os.path.isdir(skill_path) and os.path.exists(skill_md):
            with open(skill_md) as f:
                preview = f.read(500)
            registry.append({"name": skill_name, "path": skill_md, "preview": preview})
    return {**state, "available_skills": registry}


def select_skills(state: AgentState) -> AgentState:
    """Select the powerpoint builder skill."""
    paths = [s["path"] for s in state["available_skills"] if "powerpoint" in s["name"]]
    return {**state, "selected_skills": paths}


def read_skills(state: AgentState) -> AgentState:
    """Load the full content of each selected skill and its references."""
    print("\n[read_skills] Loading skill files...")
    contents = {}
    for path in state["selected_skills"]:
        with open(path, encoding='utf-8') as f:
            contents[path] = f.read()
        skill_dir = os.path.dirname(path)
        refs_dir = os.path.join(skill_dir, "references")
        if os.path.isdir(refs_dir):
            for ref_file in os.listdir(refs_dir):
                ref_path = os.path.join(refs_dir, ref_file)
                if os.path.isfile(ref_path):
                    with open(ref_path, encoding='utf-8') as f:
                        contents[ref_path] = f.read()
    print(f"[read_skills] Loaded {len(contents)} files")
    return {**state, "skill_contents": contents}


# ============================================
# LLM Pipeline Steps
# ============================================

def plan_presentation(state: AgentState) -> AgentState:
    """Step 1: Generate narrative structure."""
    print("\n[plan_presentation] Planning presentation structure...")
    skill_context = "\n\n".join(
        f"# {path}\n{content}"
        for path, content in state["skill_contents"].items()
        if "SKILL.md" in path or "template_pattern_guide" in path
    )

    response = client.chat.completions.create(
        model=LLM_MODEL,
        **({"temperature": LLM_TEMPERATURE} if LLM_TEMPERATURE is not None else {}),
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": f"""You are a presentation planner for ERNI consulting decks.
Use these skill instructions to plan the narrative:

{skill_context}

SLIDE CANVAS: 13.33 inches wide × 7.5 inches tall.

Return a JSON object with:
- title: string
- audience: string
- objective: string
- slideCount: number (3-30)
- narrativeArc: array of objects with slideIndex, intent (one of: cover, agenda, section-divider, context, insight, solution, evidence, process, metrics, team, roadmap, closing), workingTitle, keyMessage"""
            },
            {"role": "user", "content": state["task"]},
        ],
    )

    plan = json.loads(response.choices[0].message.content)
    print(f"[plan_presentation] Plan: \"{plan.get('title')}\" — {plan.get('slideCount', '?')} slides")
    for arc in plan.get("narrativeArc", []):
        print(f"  Slide {arc.get('slideIndex')}: [{arc.get('intent')}] {arc.get('workingTitle')}")
    return {**state, "plan": plan}


def outline_slides(state: AgentState) -> AgentState:
    """Step 2: Define layout intent, select images and icons per slide."""
    print("\n[outline_slides] Defining layout intents and selecting assets...")

    images_list = "\n".join(f"  - {img}" for img in AVAILABLE_IMAGES)
    icons_list = "\n".join(f"  - {icon}" for icon in AVAILABLE_ICONS[:30])

    layout_catalog = ""
    for path, content in state["skill_contents"].items():
        if "layout_catalog" in path:
            layout_catalog = content
            break

    response = client.chat.completions.create(
        model=LLM_MODEL,
        **({"temperature": LLM_TEMPERATURE} if LLM_TEMPERATURE is not None else {}),
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": f"""You are a slide layout planner for ERNI consulting decks.
Given the presentation plan, define a layout intent and select assets for each slide.

Layout catalog (for inspiration — you can compose any layout):
{layout_catalog}

Available background images (use bare filename):
{images_list}

Available icons (use bare filename):
{icons_list}

Return a JSON object with:
- slides: array of objects with:
  - slideIndex: number
  - layoutIntent: string (brief description like "cover with hero image right half", "3-column process flow", "full-text narrative with subtitle")
  - image: string or null (bare filename from available images — use for cover slides, visual slides)
  - icons: array of icon filenames (or empty array)

Guidelines:
- First slide should be a cover-style layout
- Last slide should be a closing/back-cover style
- Vary layouts — don't repeat the same pattern on consecutive slides
- Use images sparingly (covers, section dividers, visual storytelling)"""
            },
            {"role": "user", "content": json.dumps(state["plan"])},
        ],
    )

    outline = json.loads(response.choices[0].message.content)
    print(f"[outline_slides] Slide outlines:")
    for s in outline.get("slides", []):
        img = s.get("image") or "—"
        print(f"  Slide {s.get('slideIndex')}: {s.get('layoutIntent')} | image={img}")
    return {**state, "outline": outline}


def generate_content(state: AgentState) -> AgentState:
    """Step 3: Generate full element-based slide specs with positioning."""
    print("\n[generate_content] Generating element-based slide specs...")

    skill_context = ""
    for path, content in state["skill_contents"].items():
        if any(k in path for k in ["template_pattern_guide", "layout_catalog", "asset_manifest"]):
            skill_context += f"\n\n--- {os.path.basename(path)} ---\n{content}"

    images_list = ", ".join(AVAILABLE_IMAGES)
    icons_list = ", ".join(AVAILABLE_ICONS[:30])

    response = client.chat.completions.create(
        model=LLM_MODEL,
        **({"temperature": LLM_TEMPERATURE} if LLM_TEMPERATURE is not None else {}),
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": f"""You are a slide layout engine for ERNI consulting decks.
Generate complete, pixel-positioned slide elements for each slide.

SLIDE CANVAS: 13.33 inches wide × 7.5 inches tall.
SAFE ZONE: x=0.80 to 12.53, y=0.70 to 7.20 (footer at top y=0.20-0.45 — leave clear)
FONT: Source Sans Pro
BRAND COLORS: erniBlue=033778, cyan=00AADB, darkGray=3C3C3B, lightGray=B1B0B1, white=FFFFFF
FOOTER: Auto-rendered — do NOT include footer elements.

{ELEMENT_SCHEMA}

Available images: {images_list}
Available icons (use exact filenames): {icons_list}

REFERENCE GUIDELINES (layout recipes, data viz patterns, icon meanings):
{skill_context}

== COORDINATE RECIPES ==

COVER (hero image right):
  image:    x=6.67 y=0    w=6.66 h=7.5  (sizing cover)
  title:    x=0.80 y=2.00 w=5.50 h=1.20 fontSize=36 bold erniBlue
  subtitle: x=0.80 y=3.40 w=5.50 h=0.70 fontSize=20 darkGray
  accent:   shape rect x=0.80 y=1.75 w=0.05 h=1.20 fill=00AADB (cyan left bar)

SECTION DIVIDER (blue background):
  background: color=033778
  title:    x=1.00 y=2.80 w=11.33 h=1.20 fontSize=36 bold white align=center
  subtitle: x=1.00 y=4.20 w=11.33 h=0.60 fontSize=20 white align=center

3-COLUMN (icons + titles + descriptions):
  col1: x=0.80  col2: x=4.95  col3: x=9.10  each w=3.50
  separators: shape line x=4.72 y=1.80 w=0 h=4.50 (and x=8.87)
  icon:  y=1.80 w=0.55 h=0.55 (centered in col: icon_x = col_x + 1.475)
  title: y=2.55 h=0.50 fontSize=16 bold erniBlue
  body:  y=3.15 h=2.80 fontSize=12 darkGray valign=top

5-STEP PROCESS (horizontal flow):
  step spacing: cols at x=0.80, 3.06, 5.32, 7.58, 9.84 each w=2.10
  circle: shape ellipse x=col_x+0.75 y=2.00 w=0.60 h=0.60 fill=033778
  number: text  x=col_x+0.75 y=2.00 w=0.60 h=0.60 fontSize=14 bold white align=center valign=middle
  connector: shape line x=col_x+1.60 y=2.30 w=0.90 h=0 line color=033778 width=1 (between steps)
  title: y=2.80 h=0.50 fontSize=13 bold erniBlue
  desc:  y=3.40 h=2.00 fontSize=11 darkGray valign=top

KPI GRID 2×3:
  tile w=3.71 h=2.60, gap=0.15
  row1 y=1.10, row2 y=3.85
  col1 x=0.80, col2 x=4.66, col3 x=8.52
  tile bg: shape rect fill=F5F5F5 rectRadius=0.05
  value:   fontSize=32 bold erniBlue align=center y=tile_y+0.40 h=0.80
  label:   fontSize=12 darkGray align=center y=tile_y+1.30 h=0.50

IMAGE LEFT + TEXT RIGHT:
  image: x=0    y=0    w=6.00 h=7.50 (sizing cover)
  title: x=6.50 y=1.20 w=6.30 h=0.80 fontSize=26 bold erniBlue
  body:  x=6.50 y=2.20 w=6.30 h=3.50 fontSize=13 darkGray valign=top

== DESIGN RULES ==

1. ALWAYS use shape elements as structural components:
   - Use rect shapes as card backgrounds BEFORE placing text on top
   - Use line shapes as column separators (x same, w=0, h spans content area)
   - Section dividers MUST use background.color=033778 with white text
   - Use a cyan accent bar (thin rect fill=00AADB) to anchor title blocks on covers

2. TYPOGRAPHY HIERARCHY (enforce on every slide):
   - Slide title: 26-40pt bold erniBlue — ONE per slide
   - Subtitle: 16-20pt darkGray
   - Body/description: 11-14pt darkGray
   - KPI values: 28-40pt bold erniBlue
   - Labels: 10-12pt lightGray

3. VISUAL DENSITY — every slide MUST have at minimum:
   - A title text element
   - At least 2 structural shape elements (accent bars, card backgrounds, separators, or background color)
   - If slide has image in outline: include the image element
   - If slide has icons in outline: include icon elements

4. DATA SLIDES — never put numbers in bullets:
   - Metric/KPI data → use KPI tile recipe (gray rect + large value text + label)
   - Health scores → colored rect badge (red <50 fill=C0392B, amber 50-70 fill=E67E22, green >70 fill=27AE60) + score text on top
   - Percentages → progress bar (gray rect width=full, colored rect width=percent*full)

5. CLOSING SLIDES: background.color=033778, centered white text, no image needed

Return a JSON object with:
- slides: array where each object has:
  - slideIndex: number
  - background: {{ "color": "<hex>" }} (required — use FFFFFF for white or 033778 for blue)
  - elements: array of element objects"""
            },
            {
                "role": "user",
                "content": json.dumps({
                    "plan": state["plan"],
                    "outline": state["outline"],
                }),
            },
        ],
    )

    content = json.loads(response.choices[0].message.content)
    print(f"[generate_content] Generated elements for {len(content.get('slides', []))} slides:")
    for s in content.get("slides", []):
        el_count = len(s.get("elements", []))
        types = {}
        for el in s.get("elements", []):
            t = el.get("type", "?")
            types[t] = types.get(t, 0) + 1
        type_str = ", ".join(f"{v} {k}" for k, v in types.items())
        print(f"  Slide {s.get('slideIndex')}: {el_count} elements ({type_str})")
    return {**state, "content": content}


# ============================================
# Rendering & Validation
# ============================================

def build_slide_spec(state: AgentState) -> AgentState:
    """Validate elements and assemble the final renderer spec."""
    print("\n[build_slide_spec] Building and validating slide spec...")

    valid_images = set(os.listdir(IMAGES_DIR)) if os.path.isdir(IMAGES_DIR) else set()
    valid_icons = set(os.listdir(ICONS_DIR)) if os.path.isdir(ICONS_DIR) else set()

    raw_slides = state["content"].get("slides", [])
    slides = []

    for s in raw_slides:
        elements = []
        for el in s.get("elements", []):
            el_type = el.get("type")

            if el_type == "image":
                src = el.get("src", "")
                filename = src.split("/")[-1] if "/" in src else src
                if filename not in valid_images:
                    print(f"  [!] Dropping invalid image '{src}' from slide {s.get('slideIndex')}")
                    continue
                el["src"] = f"images/{filename}"

            elif el_type == "icon":
                src = el.get("src", "")
                filename = src.split("/")[-1] if "/" in src else src
                if filename not in valid_icons:
                    print(f"  [!] Dropping invalid icon '{src}' from slide {s.get('slideIndex')}")
                    continue
                el["src"] = f"icons/template-media/{filename}"

            elif el_type == "text":
                if "content" not in el or not isinstance(el.get("content"), str):
                    continue

            elif el_type == "shape":
                if "shape" not in el:
                    continue

            elements.append(el)

        slide = {
            "slideIndex": s.get("slideIndex", len(slides) + 1),
            "elements": elements,
        }
        if s.get("background"):
            slide["background"] = s["background"]
        slide["footer"] = s.get("footer", True)
        slides.append(slide)

    raw_title = state['plan'].get('title', 'presentation')
    safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in raw_title).replace(' ', '_')
    output_path = f"./output/{safe_title}.pptx"
    slide_spec = {
        "metadata": {"title": state["plan"].get("title", "Presentation"), "output": output_path},
        "slides": slides,
    }
    print(f"[build_slide_spec] Spec ready: {len(slides)} slides → {output_path}")
    return {**state, "slide_spec": slide_spec, "output_path": output_path}


def render_pptx(state: AgentState) -> AgentState:
    """Call the Node renderer service (HTTP or subprocess fallback)."""
    print("\n[render_pptx] Rendering PPTX...")
    try:
        resp = httpx.post(
            f"{RENDERER_URL}/render",
            json=state["slide_spec"],
            timeout=30.0,
        )
        if not resp.is_success:
            raise RuntimeError(f"Renderer returned {resp.status_code}: {resp.text}")
        result = resp.json()
        print(f"[render_pptx] Complete: {result['outputPath']}")
        return {**state, "output_path": result["outputPath"], "validation_result": result.get("validation", {})}
    except httpx.ConnectError:
        spec_path = "./output/slide_spec.json"
        os.makedirs("./output", exist_ok=True)
        with open(spec_path, "w") as f:
            json.dump(state["slide_spec"], f)

        result = subprocess.run(
            ["npx", "tsx", "src/cli.ts", "render", "--input", os.path.abspath(spec_path)],
            cwd="./renderer",
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"Renderer failed: {result.stderr}")
        print(f"[render_pptx] Complete (subprocess): {state['slide_spec']['metadata']['output']}")
        return {**state, "output_path": state["slide_spec"]["metadata"]["output"]}


def validate_pptx(state: AgentState) -> AgentState:
    """Run the Python validation script."""
    print("\n[validate_pptx] Validating deck assets...")
    result = subprocess.run(
        ["python", "skill/erni-powerpoint-builder/scripts/validate_deck_assets.py", state["output_path"]],
        capture_output=True,
        text=True,
    )
    validation = {
        "ok": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
    print(f"[validate_pptx] {'PASSED' if validation['ok'] else 'FAILED'}")
    return {**state, "validation_result": validation}


# ============================================
# Graph Building
# ============================================

workflow = StateGraph(AgentState)

workflow.add_node("discover_skills", discover_skills)
workflow.add_node("select_skills", select_skills)
workflow.add_node("read_skills", read_skills)
workflow.add_node("plan_presentation", plan_presentation)
workflow.add_node("outline_slides", outline_slides)
workflow.add_node("generate_content", generate_content)
workflow.add_node("build_slide_spec", build_slide_spec)
workflow.add_node("render_pptx", render_pptx)
workflow.add_node("validate_pptx", validate_pptx)

workflow.set_entry_point("discover_skills")
workflow.add_edge("discover_skills", "select_skills")
workflow.add_edge("select_skills", "read_skills")
workflow.add_edge("read_skills", "plan_presentation")
workflow.add_edge("plan_presentation", "outline_slides")
workflow.add_edge("outline_slides", "generate_content")
workflow.add_edge("generate_content", "build_slide_spec")
workflow.add_edge("build_slide_spec", "render_pptx")
workflow.add_edge("render_pptx", "validate_pptx")
workflow.add_edge("validate_pptx", END)


if __name__ == "__main__":
    import sys

    #task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Create a 10-slide capability deck about ERNI's digital transformation services"


    task = '''
    {
  "customer": {
    "customer_id": "CUST-0041",
    "company_name": "Borneo Apex Mining Sdn Bhd",
    "industry": "Mining",
    "region": "Sarawak, Malaysia",
    "account_manager": "Faizal Harun",
    "contract_type": "Full Service Agreement",
    "contract_start": "2022-01-01",
    "contract_end": "2026-12-31",
    "report_generated": "2026-06-10",
    "reporting_period": "Q2 2026 (April \u2013 June)"
  },
  "assets": [
    {
      "asset_id": "EXC-102",
      "make": "Komatsu",
      "model": "PC490LC-11",
      "type": "Hydraulic Excavator",
      "year": 2019,
      "serial_number": "K49011-A2041",
      "site": "Block 7 \u2014 Open Pit",
      "engine_hours": 9420,
      "health_score": 38,
      "health_label": "Critical",
      "utilization_rate_pct": 81,
      "last_service_date": "2026-04-24",
      "next_scheduled_service": "2026-06-23",
      "predicted_failure": {
        "component": "Hydraulic Pump",
        "confidence_pct": 87,
        "remaining_useful_life_days": 18,
        "failure_type": "Bearing fatigue",
        "urgency": "Critical"
      },
      "telemetry_summary": {
        "engine_temp_avg_c": 94,
        "hydraulic_pressure_efficiency_pct": 82,
        "vibration_zscore_trend": "+24% over 30 days",
        "oil_pressure_bar": 3.1,
        "fuel_consumption_lph": 28.4
      }
    },
    {
      "asset_id": "TRK-204",
      "make": "Caterpillar",
      "model": "793F",
      "type": "Haul Truck",
      "year": 2018,
      "serial_number": "CAT793F-B8812",
      "site": "Block 7 \u2014 Haul Road",
      "engine_hours": 14870,
      "health_score": 61,
      "health_label": "Moderate Risk",
      "utilization_rate_pct": 74,
      "last_service_date": "2026-05-19",
      "next_scheduled_service": "2026-07-08",
      "predicted_failure": {
        "component": "Brake Actuator",
        "confidence_pct": 74,
        "remaining_useful_life_days": 34,
        "failure_type": "Hydraulic seal degradation",
        "urgency": "High"
      },
      "telemetry_summary": {
        "engine_temp_avg_c": 88,
        "brake_pressure_bar": 4.7,
        "vibration_zscore_trend": "+11% over 30 days",
        "oil_pressure_bar": 3.8,
        "fuel_consumption_lph": 95.2
      }
    },
    {
      "asset_id": "BLD-305",
      "make": "Komatsu",
      "model": "D375A-8",
      "type": "Bulldozer",
      "year": 2020,
      "serial_number": "KD375-C3301",
      "site": "Block 9 \u2014 Overburden",
      "engine_hours": 6210,
      "health_score": 72,
      "health_label": "Good",
      "utilization_rate_pct": 68,
      "last_service_date": "2026-05-30",
      "next_scheduled_service": "2026-07-29",
      "predicted_failure": null,
      "telemetry_summary": {
        "engine_temp_avg_c": 82,
        "track_tension_pct": 91,
        "vibration_zscore_trend": "Stable",
        "oil_pressure_bar": 4.2,
        "fuel_consumption_lph": 41.7
      }
    },
    {
      "asset_id": "GRD-118",
      "make": "Caterpillar",
      "model": "16M3",
      "type": "Motor Grader",
      "year": 2021,
      "serial_number": "CAT16M3-D1192",
      "site": "Block 9 \u2014 Access Road",
      "engine_hours": 3870,
      "health_score": 85,
      "health_label": "Good",
      "utilization_rate_pct": 59,
      "last_service_date": "2026-06-04",
      "next_scheduled_service": "2026-08-03",
      "predicted_failure": null,
      "telemetry_summary": {
        "engine_temp_avg_c": 78,
        "circle_drive_pressure_bar": 5.1,
        "vibration_zscore_trend": "Stable",
        "oil_pressure_bar": 4.5,
        "fuel_consumption_lph": 22.1
      }
    },
    {
      "asset_id": "EXC-317",
      "make": "Hitachi",
      "model": "ZX870LCH-6",
      "type": "Hydraulic Excavator",
      "year": 2017,
      "serial_number": "HIT870-E0774",
      "site": "Block 11 \u2014 Deep Cut",
      "engine_hours": 17650,
      "health_score": 44,
      "health_label": "High Risk",
      "utilization_rate_pct": 77,
      "last_service_date": "2026-04-10",
      "next_scheduled_service": "2026-06-19",
      "predicted_failure": {
        "component": "Engine Cooling System",
        "confidence_pct": 79,
        "remaining_useful_life_days": 26,
        "failure_type": "Coolant hose fatigue + thermostat drift",
        "urgency": "High"
      },
      "telemetry_summary": {
        "engine_temp_avg_c": 101,
        "coolant_temp_c": 108,
        "vibration_zscore_trend": "+8% over 30 days",
        "oil_pressure_bar": 3.3,
        "fuel_consumption_lph": 34.9
      }
    }
  ],
  "service_history": [
    {
      "work_order_id": "WO-8841",
      "asset_id": "EXC-102",
      "date": "2026-04-24",
      "type": "Scheduled PM",
      "description": "10,000-hour major service. Engine oil and filter, hydraulic oil, air filters, fuel filters replaced. No anomalies reported.",
      "technician": "Ahmad Zulkifli",
      "duration_hours": 6,
      "parts_used": [
        {
          "part_number": "HF-7712",
          "description": "Hydraulic Oil Filter",
          "qty": 2,
          "unit_cost_myr": 185
        },
        {
          "part_number": "EO-3301",
          "description": "Engine Oil 15W-40 (20L)",
          "qty": 3,
          "unit_cost_myr": 220
        },
        {
          "part_number": "AF-5502",
          "description": "Air Filter Primary",
          "qty": 1,
          "unit_cost_myr": 310
        },
        {
          "part_number": "FF-2201",
          "description": "Fuel Filter",
          "qty": 2,
          "unit_cost_myr": 145
        }
      ],
      "total_parts_cost_myr": 1580,
      "labour_cost_myr": 720,
      "status": "Completed"
    },
    {
      "work_order_id": "WO-8792",
      "asset_id": "EXC-102",
      "date": "2026-02-18",
      "type": "Corrective",
      "description": "Hydraulic pump pressure drop reported by operator. Replaced hydraulic pump seals and flushed hydraulic circuit. Pressure restored to spec.",
      "technician": "Ahmad Zulkifli",
      "duration_hours": 9,
      "parts_used": [
        {
          "part_number": "SK-9901",
          "description": "Hydraulic Seal Kit (Pump)",
          "qty": 1,
          "unit_cost_myr": 890
        },
        {
          "part_number": "HO-4400",
          "description": "Hydraulic Oil 46 (200L)",
          "qty": 1,
          "unit_cost_myr": 1450
        }
      ],
      "total_parts_cost_myr": 2340,
      "labour_cost_myr": 1080,
      "status": "Completed"
    },
    {
      "work_order_id": "WO-8901",
      "asset_id": "TRK-204",
      "date": "2026-05-19",
      "type": "Scheduled PM",
      "description": "500-hour interim service. Oil and filters changed. Brake system inspected \u2014 minor wear noted on rear actuator seals, flagged for monitoring.",
      "technician": "Rajan Pillai",
      "duration_hours": 4,
      "parts_used": [
        {
          "part_number": "EO-3301",
          "description": "Engine Oil 15W-40 (20L)",
          "qty": 5,
          "unit_cost_myr": 220
        },
        {
          "part_number": "OF-6601",
          "description": "Oil Filter",
          "qty": 2,
          "unit_cost_myr": 95
        },
        {
          "part_number": "FF-2201",
          "description": "Fuel Filter",
          "qty": 2,
          "unit_cost_myr": 145
        }
      ],
      "total_parts_cost_myr": 1580,
      "labour_cost_myr": 480,
      "status": "Completed"
    },
    {
      "work_order_id": "WO-8755",
      "asset_id": "TRK-204",
      "date": "2026-01-06",
      "type": "Corrective",
      "description": "Rear right brake drag reported. Brake caliper assembly removed and inspected. Piston seal replaced. Brake fluid flushed.",
      "technician": "Rajan Pillai",
      "duration_hours": 7,
      "parts_used": [
        {
          "part_number": "BC-1120",
          "description": "Brake Caliper Seal Kit",
          "qty": 1,
          "unit_cost_myr": 760
        },
        {
          "part_number": "BF-3300",
          "description": "Brake Fluid DOT 4 (5L)",
          "qty": 2,
          "unit_cost_myr": 85
        }
      ],
      "total_parts_cost_myr": 930,
      "labour_cost_myr": 840,
      "status": "Completed"
    },
    {
      "work_order_id": "WO-8820",
      "asset_id": "BLD-305",
      "date": "2026-05-30",
      "type": "Scheduled PM",
      "description": "1,000-hour service. Engine oil, filters, track tension checked and adjusted. Final drive oil changed. All systems nominal.",
      "technician": "Chen Wei Liang",
      "duration_hours": 5,
      "parts_used": [
        {
          "part_number": "EO-3301",
          "description": "Engine Oil 15W-40 (20L)",
          "qty": 4,
          "unit_cost_myr": 220
        },
        {
          "part_number": "OF-6601",
          "description": "Oil Filter",
          "qty": 2,
          "unit_cost_myr": 95
        },
        {
          "part_number": "FD-7701",
          "description": "Final Drive Oil (10L)",
          "qty": 2,
          "unit_cost_myr": 195
        }
      ],
      "total_parts_cost_myr": 1470,
      "labour_cost_myr": 600,
      "status": "Completed"
    },
    {
      "work_order_id": "WO-8798",
      "asset_id": "GRD-118",
      "date": "2026-06-04",
      "type": "Scheduled PM",
      "description": "500-hour interim service. All fluids checked. Blade wear within acceptable limits. Circle drive gear backlash measured \u2014 nominal.",
      "technician": "Chen Wei Liang",
      "duration_hours": 3,
      "parts_used": [
        {
          "part_number": "EO-3301",
          "description": "Engine Oil 15W-40 (20L)",
          "qty": 2,
          "unit_cost_myr": 220
        },
        {
          "part_number": "OF-6601",
          "description": "Oil Filter",
          "qty": 1,
          "unit_cost_myr": 95
        },
        {
          "part_number": "FF-2201",
          "description": "Fuel Filter",
          "qty": 1,
          "unit_cost_myr": 145
        }
      ],
      "total_parts_cost_myr": 680,
      "labour_cost_myr": 360,
      "status": "Completed"
    },
    {
      "work_order_id": "WO-8867",
      "asset_id": "EXC-317",
      "date": "2026-04-10",
      "type": "Scheduled PM",
      "description": "2,000-hour major service. Engine inspected. Coolant system flushed and refilled. Operator reported intermittent high-temp warning over past two weeks \u2014 noted in log.",
      "technician": "Ahmad Zulkifli",
      "duration_hours": 8,
      "parts_used": [
        {
          "part_number": "CL-8801",
          "description": "Coolant Premix (20L)",
          "qty": 2,
          "unit_cost_myr": 175
        },
        {
          "part_number": "TH-5502",
          "description": "Thermostat Assembly",
          "qty": 1,
          "unit_cost_myr": 620
        },
        {
          "part_number": "EO-3301",
          "description": "Engine Oil 15W-40 (20L)",
          "qty": 4,
          "unit_cost_myr": 220
        },
        {
          "part_number": "OF-6601",
          "description": "Oil Filter",
          "qty": 2,
          "unit_cost_myr": 95
        }
      ],
      "total_parts_cost_myr": 2000,
      "labour_cost_myr": 960,
      "status": "Completed"
    },
    {
      "work_order_id": "WO-8714",
      "asset_id": "EXC-317",
      "date": "2025-11-24",
      "type": "Corrective",
      "description": "Coolant hose burst on site. Emergency repair. Hose replaced and system pressure-tested. Machine returned to service in 4 hours.",
      "technician": "Rajan Pillai",
      "duration_hours": 4,
      "parts_used": [
        {
          "part_number": "CH-3310",
          "description": "Coolant Hose Upper (1.2m)",
          "qty": 1,
          "unit_cost_myr": 380
        },
        {
          "part_number": "CH-3311",
          "description": "Coolant Hose Lower (0.9m)",
          "qty": 1,
          "unit_cost_myr": 310
        },
        {
          "part_number": "CL-8801",
          "description": "Coolant Premix (20L)",
          "qty": 1,
          "unit_cost_myr": 175
        },
        {
          "part_number": "HC-0011",
          "description": "Hose Clamp Set",
          "qty": 2,
          "unit_cost_myr": 45
        }
      ],
      "total_parts_cost_myr": 955,
      "labour_cost_myr": 480,
      "status": "Completed"
    }
  ],
  "inventory": [
    {
      "part_number": "HP-4401",
      "description": "Hydraulic Pump Assembly (PC490)",
      "on_hand_qty": 0,
      "reorder_point": 1,
      "unit_cost_myr": 18500,
      "supplier": "Komatsu Parts MY",
      "lead_time_days": 14,
      "status": "Out of Stock"
    },
    {
      "part_number": "SK-9901",
      "description": "Hydraulic Seal Kit (Pump)",
      "on_hand_qty": 2,
      "reorder_point": 2,
      "unit_cost_myr": 890,
      "supplier": "Komatsu Parts MY",
      "lead_time_days": 5,
      "status": "Low Stock"
    },
    {
      "part_number": "HF-7712",
      "description": "Hydraulic Oil Filter",
      "on_hand_qty": 8,
      "reorder_point": 4,
      "unit_cost_myr": 185,
      "supplier": "Local \u2014 AHB Parts",
      "lead_time_days": 2,
      "status": "In Stock"
    },
    {
      "part_number": "BC-1120",
      "description": "Brake Caliper Seal Kit (793F)",
      "on_hand_qty": 1,
      "reorder_point": 2,
      "unit_cost_myr": 760,
      "supplier": "CAT Dealer MY",
      "lead_time_days": 7,
      "status": "Low Stock"
    },
    {
      "part_number": "BA-5501",
      "description": "Brake Actuator Assembly (793F)",
      "on_hand_qty": 0,
      "reorder_point": 1,
      "unit_cost_myr": 12400,
      "supplier": "CAT Dealer MY",
      "lead_time_days": 10,
      "status": "Out of Stock"
    },
    {
      "part_number": "CH-3310",
      "description": "Coolant Hose Upper (ZX870)",
      "on_hand_qty": 1,
      "reorder_point": 2,
      "unit_cost_myr": 380,
      "supplier": "Hitachi Parts SEA",
      "lead_time_days": 8,
      "status": "Low Stock"
    },
    {
      "part_number": "CH-3311",
      "description": "Coolant Hose Lower (ZX870)",
      "on_hand_qty": 1,
      "reorder_point": 2,
      "unit_cost_myr": 310,
      "supplier": "Hitachi Parts SEA",
      "lead_time_days": 8,
      "status": "Low Stock"
    },
    {
      "part_number": "TH-5502",
      "description": "Thermostat Assembly (ZX870)",
      "on_hand_qty": 0,
      "reorder_point": 1,
      "unit_cost_myr": 620,
      "supplier": "Hitachi Parts SEA",
      "lead_time_days": 8,
      "status": "Out of Stock"
    },
    {
      "part_number": "CL-8801",
      "description": "Coolant Premix (20L)",
      "on_hand_qty": 6,
      "reorder_point": 4,
      "unit_cost_myr": 175,
      "supplier": "Local \u2014 AHB Parts",
      "lead_time_days": 1,
      "status": "In Stock"
    },
    {
      "part_number": "EO-3301",
      "description": "Engine Oil 15W-40 (20L)",
      "on_hand_qty": 18,
      "reorder_point": 10,
      "unit_cost_myr": 220,
      "supplier": "Local \u2014 AHB Parts",
      "lead_time_days": 1,
      "status": "In Stock"
    },
    {
      "part_number": "OF-6601",
      "description": "Oil Filter",
      "on_hand_qty": 14,
      "reorder_point": 8,
      "unit_cost_myr": 95,
      "supplier": "Local \u2014 AHB Parts",
      "lead_time_days": 1,
      "status": "In Stock"
    },
    {
      "part_number": "AF-5502",
      "description": "Air Filter Primary",
      "on_hand_qty": 3,
      "reorder_point": 3,
      "unit_cost_myr": 310,
      "supplier": "Local \u2014 AHB Parts",
      "lead_time_days": 2,
      "status": "Low Stock"
    },
    {
      "part_number": "FF-2201",
      "description": "Fuel Filter",
      "on_hand_qty": 9,
      "reorder_point": 5,
      "unit_cost_myr": 145,
      "supplier": "Local \u2014 AHB Parts",
      "lead_time_days": 1,
      "status": "In Stock"
    },
    {
      "part_number": "HO-4400",
      "description": "Hydraulic Oil 46 (200L)",
      "on_hand_qty": 2,
      "reorder_point": 2,
      "unit_cost_myr": 1450,
      "supplier": "Local \u2014 AHB Parts",
      "lead_time_days": 2,
      "status": "Low Stock"
    }
  ],
  "procurement_recommendations": [
    {
      "priority": "URGENT",
      "part_number": "HP-4401",
      "description": "Hydraulic Pump Assembly (PC490)",
      "reason": "EXC-102 predicted failure in 18 days. Zero stock. Lead time 14 days \u2014 order today to maintain safety margin.",
      "recommended_qty": 1,
      "estimated_cost_myr": 18500,
      "order_by_date": "2026-06-11",
      "linked_asset": "EXC-102"
    },
    {
      "priority": "URGENT",
      "part_number": "TH-5502",
      "description": "Thermostat Assembly (ZX870)",
      "reason": "EXC-317 cooling system failure predicted in 26 days. Zero stock. Lead time 8 days.",
      "recommended_qty": 1,
      "estimated_cost_myr": 620,
      "order_by_date": "2026-06-13",
      "linked_asset": "EXC-317"
    },
    {
      "priority": "HIGH",
      "part_number": "BA-5501",
      "description": "Brake Actuator Assembly (793F)",
      "reason": "TRK-204 brake actuator degradation detected. 34 days RUL. Zero stock, 10-day lead time. Pre-order recommended.",
      "recommended_qty": 1,
      "estimated_cost_myr": 12400,
      "order_by_date": "2026-06-17",
      "linked_asset": "TRK-204"
    },
    {
      "priority": "HIGH",
      "part_number": "SK-9901",
      "description": "Hydraulic Seal Kit (Pump)",
      "reason": "Required alongside HP-4401 for EXC-102 pump replacement. Current stock of 2 will be consumed by repair.",
      "recommended_qty": 2,
      "estimated_cost_myr": 1780,
      "order_by_date": "2026-06-11",
      "linked_asset": "EXC-102"
    },
    {
      "priority": "MEDIUM",
      "part_number": "CH-3310",
      "description": "Coolant Hose Upper (ZX870)",
      "reason": "EXC-317 has prior hose failure history. Current stock below reorder point. Replenish before next scheduled service.",
      "recommended_qty": 2,
      "estimated_cost_myr": 760,
      "order_by_date": "2026-06-19",
      "linked_asset": "EXC-317"
    },
    {
      "priority": "MEDIUM",
      "part_number": "CH-3311",
      "description": "Coolant Hose Lower (ZX870)",
      "reason": "Same reasoning as CH-3310. Hoses typically replaced in pairs on ZX870.",
      "recommended_qty": 2,
      "estimated_cost_myr": 620,
      "order_by_date": "2026-06-19",
      "linked_asset": "EXC-317"
    },
    {
      "priority": "MEDIUM",
      "part_number": "HO-4400",
      "description": "Hydraulic Oil 46 (200L)",
      "reason": "EXC-102 pump replacement will require full hydraulic circuit flush. Current stock (2 drums) at reorder point.",
      "recommended_qty": 2,
      "estimated_cost_myr": 2900,
      "order_by_date": "2026-06-15",
      "linked_asset": "EXC-102"
    }
  ],
  "fleet_summary": {
    "total_assets": 5,
    "critical_assets": 1,
    "high_risk_assets": 2,
    "good_assets": 2,
    "average_fleet_health_score": 60,
    "average_utilization_pct": 72,
    "total_service_events_q2": 8,
    "total_corrective_events_q2": 3,
    "total_planned_events_q2": 5,
    "total_parts_spend_myr_q2": 18535,
    "total_labour_spend_myr_q2": 5520,
    "total_maintenance_spend_myr_q2": 24055,
    "assets_with_predicted_failure": 3,
    "earliest_predicted_failure_days": 18,
    "earliest_predicted_failure_asset": "EXC-102",
    "total_procurement_value_recommended_myr": 37580,
    "urgent_procurement_items": 2,
    "estimated_downtime_risk_hours": 34,
    "downtime_cost_per_hour_myr": 8500,
    "estimated_financial_exposure_myr": 289000
  },
  "upcoming_maintenance": [
    {
      "asset_id": "EXC-317",
      "type": "Scheduled PM",
      "due_date": "2026-06-19",
      "estimated_duration_hours": 8,
      "notes": "Critical \u2014 combine with cooling system repair. Pre-order TH-5502 before this date."
    },
    {
      "asset_id": "EXC-102",
      "type": "Corrective \u2014 Hydraulic Pump Replacement",
      "due_date": "2026-06-23",
      "estimated_duration_hours": 10,
      "notes": "Must complete before RUL expiry (18 days). HP-4401 on order \u2014 confirm delivery."
    },
    {
      "asset_id": "TRK-204",
      "type": "Scheduled PM + Brake Inspection",
      "due_date": "2026-07-08",
      "estimated_duration_hours": 6,
      "notes": "Inspect brake actuator. Replace if BA-5501 delivered. Do not defer beyond this date."
    },
    {
      "asset_id": "BLD-305",
      "type": "Scheduled PM",
      "due_date": "2026-07-29",
      "estimated_duration_hours": 5,
      "notes": "Routine 1,000-hour service. No predicted failures. Low risk."
    },
    {
      "asset_id": "GRD-118",
      "type": "Scheduled PM",
      "due_date": "2026-08-03",
      "estimated_duration_hours": 3,
      "notes": "Routine 500-hour service. All systems nominal."
    }
  ]
}
    
    '''
    
    app = workflow.compile()
    result = app.invoke({"task": task})

    print(f"\nOutput: {result['output_path']}")
    if result.get("validation_result", {}).get("ok"):
        print("Validation: PASSED")
    else:
        print("Validation: FAILED")
        print(result.get("validation_result", {}).get("stderr", ""))
