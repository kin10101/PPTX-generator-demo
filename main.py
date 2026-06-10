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

IMAGES_DIR = "./skill/erni-powerpoint-builder/assets/images"
ICONS_DIR = "./skill/erni-powerpoint-builder/assets/icons/template-media"

IMPLEMENTED_LAYOUTS = """- Cover Layout 1: title + subtitle + hero image (right half). Use for opening slide with a strong visual.
- Cover Layout 2: title + subtitle (white background, no image). Use for clean text-only opener.
- Cover Layout 3: title + subtitle (right-aligned, white). Alternative opening style.
- Section Layout 1: section number + title + subtitle (blue divider). Use to separate chapters.
- Info Layout 5a: title + subtitle + body text (single column, right side). General-purpose narrative slide.
- Info Layout 5b: title + subtitle + body text (two columns). Use when comparing two ideas or longer text.
- Info Layout Image and Text 6a: image (left panel) + title + body (single column). Use for visual storytelling.
- Info Layout Image and Text 6b: image (left panel) + title + body (two columns). Image slide with more text.
- Info Layout 2a: title + 3 icons with labels, vertical separators. Use for pillars, principles, capabilities.
- Flow Layout 3b: subtitle + numbered steps with descriptions. Use for processes, timelines, lifecycles.
- Chart Layout 2a: subtitle + 3 icons with descriptions. Use for comparisons, feature highlights.
- Containers Layout: 6-box grid for facts/figures/short items. Use for KPIs, stats, quick facts.
- People Layout 1: team or profile slide. Use for team introductions.
- Back Cover 1: closing/contact slide.
- Back Cover 2: closing variant.
- Back Cover 3: closing variant."""

AVAILABLE_IMAGES = [f for f in os.listdir(IMAGES_DIR) if f.endswith(('.jpg', '.png'))] if os.path.isdir(IMAGES_DIR) else []


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
        if "SKILL.md" in path
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.7,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": f"""You are a presentation planner for ERNI consulting decks.
Use these skill instructions to plan the narrative:

{skill_context}

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
    print(f"[plan_presentation] Narrative arc:")
    for arc in plan.get("narrativeArc", []):
        print(f"  Slide {arc.get('slideIndex')}: [{arc.get('intent')}] {arc.get('workingTitle')}")
    return {**state, "plan": plan}


def outline_slides(state: AgentState) -> AgentState:
    """Step 2: Select layouts, images, and icons for each slide."""
    print("\n[outline_slides] Selecting layouts and images...")

    images_list = "\n".join(f"  - {img}" for img in AVAILABLE_IMAGES)

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.3,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": f"""You are a slide layout specialist for ERNI consulting decks.
Given the presentation plan, select the best layout, image, and icons for each slide.

IMPORTANT: Use ONLY these exact layout names (these are the only ones the renderer supports):
{IMPLEMENTED_LAYOUTS}

Available background images (use bare filename only, no path prefix):
{images_list}

Layout selection guidance:
- First slide should use a Cover Layout
- Last slide should use a Back Cover
- Use Section Layout 1 for chapter dividers
- Use Flow Layout 3b for processes, timelines, or lifecycle content
- Use Containers Layout for facts, stats, or KPIs
- Use Info Layout Image and Text 6a/6b when you want a visual + text combo
- Use Info Layout 2a or Chart Layout 2a when you have 3 parallel items
- Vary layouts across the deck — avoid using the same layout on consecutive slides

Return a JSON object with:
- slides: array of objects with slideIndex, layoutName (exact name from the list above), image (bare filename like "orange-wave-70.jpg" — only for Cover Layout 1, Info Layout Image and Text 6a/6b, or section dividers; omit for other layouts), icons (array of filenames from assets/icons/template-media/ or empty array)"""
            },
            {"role": "user", "content": json.dumps(state["plan"])},
        ],
    )

    outline = json.loads(response.choices[0].message.content)
    print(f"[outline_slides] Slide layout assignments:")
    for s in outline.get("slides", []):
        img = s.get("image", "—")
        icons = s.get("icons", [])
        print(f"  Slide {s.get('slideIndex')}: {s.get('layoutName')} | image={img} | icons={len(icons)}")
    return {**state, "outline": outline}


def generate_content(state: AgentState) -> AgentState:
    """Step 3: Generate text content for each slide."""
    print("\n[generate_content] Generating slide content...")
    skill_context = ""
    for path, content in state["skill_contents"].items():
        if "SKILL.md" in path or "template_pattern_guide" in path:
            skill_context += f"\n\n{content}"

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.3,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": f"""You are a content writer for ERNI consulting presentations.
Write concise, assertive slide text following these style rules:

{skill_context}

Given the plan and outline, generate content for each slide.

Return a JSON object with:
- slides: array of objects with slideIndex, and content object containing: title (string), subtitle (optional string), body (optional string), options (optional array of {{title, description}}), steps (optional array of {{number, title, description}}), metrics (optional array of {{value, label}}), footnote (optional string)

IMPORTANT content rules:
- Every content slide (not cover, section divider, or back cover) MUST have body text of 2-4 sentences.
- Match structured content to the layout chosen in the outline:
  - Flow Layout 3b → MUST include steps (3-4 items with number, title, description)
  - Containers Layout → MUST include options (4-6 items) OR metrics (4-6 items)
  - Chart Layout 2a → MUST include metrics (3 items with value and label)
  - Info Layout 2a → MUST include options (3 items with title and description)
  - Info Layout 5a/5b/6a/6b → MUST include body text (3-5 sentences)
- Use at least one structured element (options, steps, or metrics) on at least half of all content slides.
- Keep titles concise and assertive (max 6 words). Use short body copy. Keep option/step titles parallel."""
            },
            {
                "role": "user",
                "content": json.dumps({"plan": state["plan"], "outline": state["outline"]}),
            },
        ],
    )

    content = json.loads(response.choices[0].message.content)
    print(f"[generate_content] Content generated for {len(content.get('slides', []))} slides:")
    for s in content.get("slides", []):
        c = s.get("content", s)
        elements = []
        if c.get("body"): elements.append(f"body({len(c['body'])} chars)")
        if c.get("options"): elements.append(f"options({len(c['options'])})")
        if c.get("steps"): elements.append(f"steps({len(c['steps'])})")
        if c.get("metrics"): elements.append(f"metrics({len(c['metrics'])})")
        print(f"  Slide {s.get('slideIndex')}: \"{c.get('title', '?')}\" — {', '.join(elements) or 'title only'}")
    return {**state, "content": content}


# ============================================
# Rendering & Validation
# ============================================

def build_slide_spec(state: AgentState) -> AgentState:
    """Merge outline and content into the renderer's input format."""
    print("\n[build_slide_spec] Building slide spec...")
    outline_slides = state["outline"].get("slides", [])
    content_slides = state["content"].get("slides", [])

    content_by_index = {s["slideIndex"]: s.get("content", s) for s in content_slides}

    valid_images = set(os.listdir(IMAGES_DIR)) if os.path.isdir(IMAGES_DIR) else set()
    valid_icons = set(os.listdir(ICONS_DIR)) if os.path.isdir(ICONS_DIR) else set()

    slides = []
    for s in outline_slides:
        idx = s["slideIndex"]
        content_data = content_by_index.get(idx, {})
        if "title" not in content_data and "content" in content_data:
            content_data = content_data["content"]

        raw_image = s.get("image")
        image = raw_image.split("/")[-1] if raw_image else None
        if image and image not in valid_images:
            print(f"  [!] Dropping invalid image '{image}' from slide {idx}")
            image = None

        raw_icons = s.get("icons", [])
        icons = [i if isinstance(i, str) else i.get("name", str(i)) for i in raw_icons] if raw_icons else []
        icons = [i.split("/")[-1] for i in icons]
        invalid_icons = [i for i in icons if i not in valid_icons]
        if invalid_icons:
            print(f"  [!] Dropping invalid icons from slide {idx}: {invalid_icons}")
            icons = [i for i in icons if i in valid_icons]

        raw_metrics = content_data.get("metrics")
        metrics = (
            [{"value": str(m["value"]), "label": str(m["label"])} for m in raw_metrics]
            if raw_metrics else None
        )

        raw_steps = content_data.get("steps")
        steps = (
            [{"title": st["title"], "description": st["description"], **({"number": str(st["number"])} if "number" in st else {})} for st in raw_steps]
            if raw_steps else None
        )

        content = {"title": content_data.get("title", "")}
        for key, val in [
            ("subtitle", content_data.get("subtitle")),
            ("body", content_data.get("body")),
            ("options", content_data.get("options")),
            ("steps", steps),
            ("metrics", metrics),
            ("footnote", content_data.get("footnote")),
        ]:
            if val is not None:
                content[key] = val

        slide = {
            "slideIndex": idx,
            "layoutName": s.get("layoutName", "Info Layout 5a"),
            "icons": icons,
            "content": content,
        }
        if image is not None:
            slide["image"] = image
        slides.append(slide)

    output_path = f"./output/{state['plan'].get('title', 'presentation').replace(' ', '_')}.pptx"
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
