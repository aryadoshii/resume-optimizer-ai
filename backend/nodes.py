"""LangGraph nodes for resume tailoring workflow."""

import json
import time
from typing import Dict, Any, Generator
from openai import OpenAI

from config import settings, ANALYZE_JD_PROMPT, DRAFT_RESUME_PROMPT, CRITIQUE_PROMPT
from .state import ResumeState
from .utils import extract_json_from_text


# Initialize OpenAI client for Qubrid
client = OpenAI(
    base_url=settings.qubrid_base_url,
    api_key=settings.qubrid_api_key
)


def call_llm_with_retry(
    messages: list,
    temperature: float = 0.7,
    stream: bool = False,
    max_retries: int = None
) -> str:
    """
    Call LLM with exponential backoff retry logic.

    Args:
        messages: Chat messages
        temperature: Sampling temperature
        stream: Whether to stream response
        max_retries: Maximum retry attempts (uses settings default if None)

    Returns:
        LLM response text

    Raises:
        RuntimeError: If all retries fail
    """
    if max_retries is None:
        max_retries = settings.max_retries

    last_error = None

    for attempt in range(max_retries):
        try:
            if stream:
                response_text = ""
                stream_response = client.chat.completions.create(
                    model=settings.model_name,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=settings.max_tokens,
                    stream=True
                )

                for chunk in stream_response:
                    if chunk.choices[0].delta.content:
                        response_text += chunk.choices[0].delta.content

                return response_text

            else:
                response = client.chat.completions.create(
                    model=settings.model_name,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=settings.max_tokens
                )
                return response.choices[0].message.content

        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                delay = settings.retry_delay * (2 ** attempt)
                time.sleep(delay)
                continue
            break

    raise RuntimeError(f"LLM call failed after {max_retries} attempts: {last_error}")


def analyze_job_description(state: ResumeState) -> Dict[str, Any]:
    """
    Analyze job description to extract key requirements.

    Args:
        state: Current workflow state

    Returns:
        Updated state with jd_analysis
    """
    prompt = ANALYZE_JD_PROMPT.format(
        job_description=state["job_description"]
    )

    messages = [
        {"role": "system", "content": "You are an expert recruiter analyzing job descriptions."},
        {"role": "user", "content": prompt}
    ]

    try:
        response = call_llm_with_retry(
            messages=messages,
            temperature=settings.temperature_analysis
        )

        # Extract JSON from response
        jd_analysis = extract_json_from_text(response)

        return {
            "jd_analysis": jd_analysis,
            "iteration": 0
        }

    except Exception as e:
        return {"error": f"Job description analysis failed: {str(e)}"}


def draft_tailored_resume(state: ResumeState) -> Dict[str, Any]:
    """
    Generate tailored resume based on job requirements.

    Args:
        state: Current workflow state

    Returns:
        Updated state with draft_resume
    """
    # Format job analysis as readable text
    jd_analysis_text = json.dumps(state["jd_analysis"], indent=2)

    prompt = DRAFT_RESUME_PROMPT.format(
        original_resume=state["original_resume"],
        jd_analysis=jd_analysis_text
    )

    messages = [
        {"role": "system", "content": "You are an expert resume writer specializing in ATS optimization."},
        {"role": "user", "content": prompt}
    ]

    try:
        draft = call_llm_with_retry(
            messages=messages,
            temperature=settings.temperature_generation
        )

        # Clean up response (remove markdown code blocks if present)
        draft = draft.strip()
        if draft.startswith("```markdown"):
            draft = draft[len("```markdown"):].strip()
        if draft.startswith("```"):
            draft = draft[3:].strip()
        if draft.endswith("```"):
            draft = draft[:-3].strip()

        return {"draft_resume": draft}

    except Exception as e:
        return {"error": f"Resume drafting failed: {str(e)}"}


def critique_resume(state: ResumeState) -> Dict[str, Any]:
    """
    Evaluate the drafted resume and provide critique.

    Args:
        state: Current workflow state

    Returns:
        Updated state with critique and incremented iteration
    """
    jd_analysis_text = json.dumps(state["jd_analysis"], indent=2)

    prompt = CRITIQUE_PROMPT.format(
        draft_resume=state["draft_resume"],
        jd_analysis=jd_analysis_text,
        original_resume=state["original_resume"]
    )

    messages = [
        {"role": "system", "content": "You are a senior recruiter evaluating resumes."},
        {"role": "user", "content": prompt}
    ]

    try:
        response = call_llm_with_retry(
            messages=messages,
            temperature=settings.temperature_analysis
        )

        # Extract JSON critique
        critique = extract_json_from_text(response)

        return {
            "critique": critique,
            "iteration": state.get("iteration", 0) + 1
        }

    except Exception as e:
        return {"error": f"Resume critique failed: {str(e)}"}


def finalize_resume(state: ResumeState) -> Dict[str, Any]:
    """
    Finalize the approved resume.

    Args:
        state: Current workflow state

    Returns:
        Updated state with final_resume
    """
    return {
        "final_resume": state["draft_resume"],
        "output_markdown": state["draft_resume"]
    }


def should_continue_iteration(state: ResumeState) -> str:
    """
    Decision function to determine if another iteration is needed.

    Args:
        state: Current workflow state

    Returns:
        "finalize" if approved or max iterations reached, "draft" to iterate
    """
    # Check for errors
    if state.get("error"):
        return "finalize"

    # Check if we have a critique
    critique = state.get("critique", {})

    # Check if approved
    if critique.get("approved", False):
        return "finalize"

    # Check max iterations
    if state.get("iteration", 0) >= settings.max_iterations:
        return "finalize"

    # Continue iterating
    return "draft"


# Streaming wrapper for UI updates
def stream_node_execution(
    node_func,
    state: ResumeState,
    node_name: str
) -> Generator[Dict[str, Any], None, Dict[str, Any]]:
    """
    Wrapper to stream node execution progress to UI.

    Args:
        node_func: Node function to execute
        state: Current state
        node_name: Name of the node for logging

    Yields:
        Progress updates

    Returns:
        Updated state from node execution
    """
    yield {"status": "running", "node": node_name, "message": f"Starting {node_name}..."}

    try:
        result = node_func(state)
        yield {"status": "complete", "node": node_name, "message": f"Completed {node_name}"}
        return result

    except Exception as e:
        yield {"status": "error", "node": node_name, "message": str(e)}
        return {"error": str(e)}
