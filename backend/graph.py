"""LangGraph workflow for resume tailoring with user approval."""

from langgraph.graph import StateGraph, END
from .state import ResumeState
from .nodes import (
    analyze_job_description,
    critique_resume,
    finalize_resume,
)

from config.settings import settings  


def draft_suggestions_only(state: ResumeState) -> dict:
    """
    Generate suggestions WITHOUT creating new resume.
    
    Returns suggested improvements as a list.
    """
    from .nodes import call_llm_with_retry
    from config.settings import settings
    import json
    
    jd_analysis_text = json.dumps(state["jd_analysis"], indent=2)
    
    prompt = f"""You are a resume expert. Analyze this resume against the job requirements and provide SPECIFIC improvement suggestions.

Original Resume:
{state['original_resume']}

Job Requirements:
{jd_analysis_text}

Provide 5-8 specific, actionable suggestions to improve this resume for this role. Focus on:
1. Keywords to add
2. Experience to emphasize
3. Skills to highlight
4. Sections to reorder
5. Achievements to quantify

Return ONLY a JSON array of suggestion objects:
[
  {{"category": "Keywords", "suggestion": "Add 'quantitative modeling' and 'risk analytics' to skills"}},
  {{"category": "Experience", "suggestion": "Lead with your QuantEdge project - it's most relevant"}},
  ...
]"""

    response = call_llm_with_retry(
        messages=[
            {"role": "system", "content": "You are a resume optimization expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=settings.temperature_analysis
    )
    
    # Parse suggestions
    try:
        from .utils import extract_json_from_text
        suggestions = extract_json_from_text(response)
        if not isinstance(suggestions, list):
            suggestions = [{"category": "General", "suggestion": response}]
    except:
        suggestions = [{"category": "General", "suggestion": response}]
    
    return {
        "draft_resume": state["original_resume"],  # Keep original
        "suggestions": suggestions,
        "awaiting_approval": True
    }


def draft_tailored_resume(state: ResumeState) -> dict:
    """Generate tailored resume ONLY after user approval."""
    from .nodes import call_llm_with_retry
    from config.settings import settings
    from config.prompts import DRAFT_RESUME_PROMPT
    import json
    
    jd_analysis_text = json.dumps(state["jd_analysis"], indent=2)
    
    prompt = DRAFT_RESUME_PROMPT.format(
        original_resume=state["original_resume"],
        jd_analysis=jd_analysis_text
    )
    
    draft = call_llm_with_retry(
        messages=[
            {"role": "system", "content": "You are an expert resume writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=settings.temperature_generation
    )
    
    # Clean markdown
    draft = draft.strip()
    if draft.startswith("```markdown"):
        draft = draft[len("```markdown"):].strip()
    if draft.startswith("```"):
        draft = draft[3:].strip()
    if draft.endswith("```"):
        draft = draft[:-3].strip()
    
    return {"draft_resume": draft, "awaiting_approval": False}


def should_continue_iteration(state: ResumeState) -> str:
    """Decision: continue iterating or finalize."""
    if state.get("error"):
        return "finalize"
    
    critique = state.get("critique", {})
    
    if critique.get("approved", False):
        return "finalize"
    
    if state.get("iteration", 0) >= settings.max_iterations:
        return "finalize"
    
    return "draft"


def create_resume_workflow() -> StateGraph:
    """
    Create workflow with user approval step.
    
    Flow:
    1. Analyze JD
    2. Generate suggestions (NOT full resume)
    3. Wait for user approval
    4. If approved: Draft resume → Critique → Iterate
    5. Finalize
    """
    workflow = StateGraph(ResumeState)
    
    # Add nodes
    workflow.add_node("analyze_jd", analyze_job_description)
    workflow.add_node("suggest", draft_suggestions_only)
    workflow.add_node("draft", draft_tailored_resume)
    workflow.add_node("critique", critique_resume)
    workflow.add_node("finalize", finalize_resume)
    
    # Define flow
    workflow.set_entry_point("analyze_jd")
    workflow.add_edge("analyze_jd", "suggest")
    workflow.add_edge("suggest", END)  # Stop here for user approval
    
    # After approval, continue from draft
    workflow.add_edge("draft", "critique")
    
    workflow.add_conditional_edges(
        "critique",
        should_continue_iteration,
        {
            "draft": "draft",
            "finalize": "finalize"
        }
    )
    
    workflow.add_edge("finalize", END)
    
    return workflow.compile()