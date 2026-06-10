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
        with open(path) as f:
            contents[path] = f.read()
        skill_dir = os.path.dirname(path)
        refs_dir = os.path.join(skill_dir, "references")
        if os.path.isdir(refs_dir):
            for ref_file in os.listdir(refs_dir):
                ref_path = os.path.join(refs_dir, ref_file)
                if os.path.isfile(ref_path):
                    with open(ref_path) as f:
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
        temperature=0.7,
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
        temperature=0.3,
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
        temperature=0.3,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": f"""You are a slide layout engine for ERNI consulting decks.
Generate complete, pixel-positioned slide elements for each slide.

SLIDE CANVAS: 13.33 inches wide × 7.5 inches tall.
FONT: Source Sans Pro
BRAND COLORS: erniBlue=033778, cyan=00AADB, darkGray=3C3C3B, lightGray=B1B0B1, white=FFFFFF
FOOTER: Automatically rendered by the system (do NOT include footer elements).

{ELEMENT_SCHEMA}

Available images: {images_list}
Available icons: {icons_list}

REFERENCE GUIDELINES:
{skill_context}

RULES:
- All positions are in inches from top-left origin
- Keep elements within canvas bounds (0-13.33 x, 0-7.5 y)
- Use only "Source Sans Pro" as fontFace
- Use only hex colors without # prefix
- For images, use "images/<filename>" as src
- For icons, use "icons/template-media/<filename>" as src
- Title text: 26-40pt, bold, erniBlue (033778)
- Subtitle text: 16-20pt, darkGray (3C3C3B)
- Body text: 12-14pt, darkGray (3C3C3B)
- Leave ~0.8" margins on sides
- Leave top 0.6" clear for footer area

Return a JSON object with:
- slides: array where each object has:
  - slideIndex: number
  - background: {{ "color": "<hex>" }} (optional, default white)
  - elements: array of element objects as defined above"""
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

    task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Create a 10-slide capability deck about ERNI's digital transformation services"

    app = workflow.compile()
    result = app.invoke({"task": task})

    print(f"\nOutput: {result['output_path']}")
    if result.get("validation_result", {}).get("ok"):
        print("Validation: PASSED")
    else:
        print("Validation: FAILED")
        print(result.get("validation_result", {}).get("stderr", ""))
