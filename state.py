from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END


class AgentState(TypedDict):
    task: str
    available_skills: list[dict]
    selected_skills: list[str]
    skill_contents: dict[str, str]
    plan: dict
    outline: dict
    content: dict
    slide_spec: dict
    output_path: str
    validation_result: dict
