"""Reusable UI components for Career-Sync-AI application."""

import streamlit as st
from datetime import datetime
from typing import Dict, Any, Optional
import os
import json


def render_header(theme: str = "dark"):
    """Render application header with branding."""
    st.markdown(
        f"""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="font-size: 3em; margin-bottom: 0;">Resume-Optimizer-AI</h1>
            <p style="font-size: 1.2em; {'color: #b0b0b0' if theme == 'dark' else 'color: #6b7280'}; margin-top: 10px;">
                AI-Powered Resume Optimization with Mistral 7B
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_theme_toggle() -> str:
    """
    Render theme toggle and return current theme.

    Returns:
        Current theme: "dark" or "light"
    """
    st.sidebar.markdown("### ⚙️ Settings")

    # Initialize theme in session state - DEFAULT TO LIGHT
    if "theme" not in st.session_state:
        st.session_state.theme = "light"

    # Theme toggle
    theme_options = {"🌙 Dark Mode": "dark", "☀️ Light Mode": "light"}
    selected = st.sidebar.radio(
        "Theme",
        options=list(theme_options.keys()),
        index=0 if st.session_state.theme == "dark" else 1,
        label_visibility="collapsed"
    )

    st.session_state.theme = theme_options[selected]
    return st.session_state.theme


def render_file_uploader(
    label: str,
    accepted_types: list,
    key: str,
    help_text: str = None
) -> Optional[Any]:
    """
    Render a file uploader with validation.

    Args:
        label: Uploader label
        accepted_types: List of accepted file extensions
        key: Unique key for the uploader
        help_text: Optional help text

    Returns:
        Uploaded file or None
    """
    uploaded_file = st.file_uploader(
        label,
        type=accepted_types,
        key=key,
        help=help_text
    )

    return uploaded_file


def render_critique_feedback(critique: Dict[str, Any]):
    """
    Render critique feedback in a formatted way with colored cards.

    Args:
        critique: Critique dictionary with scores and feedback
    """
    st.markdown("### 📋 Resume Evaluation")

    # Overall score with color coding
    overall_score = critique.get("overall_score", 0)
    score_color = "#10b981" if overall_score >= 8 else "#f59e0b" if overall_score >= 6 else "#ef4444"

    st.markdown(
        f"""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%); 
                    border-radius: 12px; margin-bottom: 20px; border: 1px solid rgba(139, 92, 246, 0.3);">
            <h2 style="color: {score_color}; margin: 0; font-size: 3em;">{overall_score:.1f}/10</h2>
            <p style="margin: 5px 0 0 0; opacity: 0.8;">Overall Score</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Individual scores in colored cards
    col1, col2 = st.columns(2)

    scores = [
        ("Keyword Optimization", critique.get('keyword_score', 0)),
        ("Experience Relevance", critique.get('experience_score', 0)),
        ("ATS-Friendliness", critique.get('ats_score', 0)),
        ("Professional Formatting", critique.get('formatting_score', 0))
    ]

    colors = ["#8B5CF6", "#EC4899", "#3B82F6", "#10B981"]

    for i, (label, score) in enumerate(scores):
        col = col1 if i < 2 else col2
        color = colors[i]
        
        with col:
            st.markdown(
                f"""
                <div style="padding: 16px; background-color: rgba(139, 92, 246, 0.05); 
                            border-left: 4px solid {color}; border-radius: 8px; margin-bottom: 12px;">
                    <p style="margin: 0; opacity: 0.7; font-size: 0.9em;">{label}</p>
                    <h3 style="margin: 5px 0 0 0; color: {color};">{score}/10</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Feedback
    if critique.get("feedback"):
        with st.expander("📝 Detailed Feedback", expanded=True):
            st.write(critique["feedback"])

    # Improvements needed
    if critique.get("improvements_needed"):
        with st.expander("🎯 AI Suggestions for Further Improvement"):
            st.caption("*These are optional suggestions to make your resume even stronger*")
            for improvement in critique["improvements_needed"]:
                st.markdown(f"- {improvement}")

    # Approval status
    if critique.get("approved"):
        st.success("✅ Resume approved for finalization!")
    else:
        st.warning("⚠️ Resume needs improvement - generating new iteration...")


def render_resume_preview(markdown_content: str):
    """
    Render resume preview with clear header.

    Args:
        markdown_content: Resume content in Markdown
    """
    st.markdown("---")
    st.markdown("## 📄 Your AI-Generated Tailored Resume")
    st.info("👇 **This is your NEW resume** - optimized for the job description you provided. Review it before downloading.")

    with st.container():
        st.markdown(markdown_content)


def render_download_buttons(
    markdown_content: str,
    pdf_path: str,
    filename_prefix: str = "resume"
):
    """
    Render download buttons for Markdown and PDF.

    Args:
        markdown_content: Resume in Markdown format
        pdf_path: Path to PDF file
        filename_prefix: Prefix for download filenames
    """
    st.markdown("### 📥 Download Resume")

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="📝 Download Markdown",
            data=markdown_content,
            file_name=f"{filename_prefix}.md",
            mime="text/markdown",
            use_container_width=True
        )

    with col2:
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()

            st.download_button(
                label="📄 Download PDF",
                data=pdf_bytes,
                file_name=f"{filename_prefix}.pdf",
                mime="application/pdf",
                use_container_width=True
            )


def render_history_sidebar(history: list):
    """
    Render previous generations in sidebar with clickable chat names.

    Args:
        history: List of generation entries from database
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📚 Previous Generations")

    if not history:
        st.sidebar.info("No previous generations yet.")
        return

    for entry in history[:10]:  # Show last 10
        timestamp = datetime.fromisoformat(entry["timestamp"])
        
        # Format: "Feb 12, 1:17 PM"
        formatted_time = timestamp.strftime("%b %d, %I:%M %p")
        
        job_title = entry.get('job_title', 'Unknown')
        company = entry.get('company', 'N/A')
        score = entry.get('final_score', 0)
        
        # Clickable expander with details
        with st.sidebar.expander(
            f"**{job_title}** • {formatted_time}",
            expanded=False
        ):
            st.markdown(f"🏢 **{company}**")
            st.markdown(f"⭐ **Score:** {score:.1f}/10")
            st.markdown(f"🔄 **Iterations:** {entry.get('iterations', 0)}")
            
            st.markdown("---")
            
            # Clickable button to restore
            if st.button("📂 Open This Chat", key=f"open_{entry['id']}", use_container_width=True):
                restore_generation(entry['id'])

            # Download buttons
            col1, col2 = st.columns(2)
            
            with col1:
                if entry.get("markdown_path"):
                    try:
                        with open(entry["markdown_path"], "r") as f:
                            md_content = f.read()
                        st.download_button(
                            "📝 MD",
                            data=md_content,
                            file_name=f"resume_{entry['id']}.md",
                            key=f"md_{entry['id']}",
                            use_container_width=True
                        )
                    except:
                        pass

            with col2:
                if entry.get("pdf_path"):
                    try:
                        with open(entry["pdf_path"], "rb") as f:
                            pdf_content = f.read()
                        st.download_button(
                            "📄 PDF",
                            data=pdf_content,
                            file_name=f"resume_{entry['id']}.pdf",
                            key=f"pdf_{entry['id']}",
                            use_container_width=True
                        )
                    except:
                        pass


def restore_generation(generation_id: int):
    """Restore a previous generation to current state."""
    from backend.database import get_generation_by_id
    
    gen = get_generation_by_id(generation_id)
    if not gen:
        st.error("Generation not found")
        return
    
    # Restore to session state
    st.session_state.final_state = {
        "original_resume": gen["original_resume"],
        "job_description": gen["job_description"],
        "jd_analysis": json.loads(gen["jd_analysis"]),
        "final_resume": gen["final_resume"],
        "critique": json.loads(gen["final_critique"]),
        "iteration": gen["iterations"],
        "output_pdf_path": gen["pdf_path"]
    }
    
    st.session_state.initial_critique = json.loads(gen["initial_critique"])
    st.session_state.suggestions = json.loads(gen["suggestions"])
    st.session_state.evaluation_done = False
    
    st.rerun()


def render_error_message(error: str):
    """
    Render user-friendly error message.

    Args:
        error: Error message
    """
    st.error(f"❌ **Error:** {error}")

    with st.expander("🔧 Troubleshooting Tips"):
        st.markdown("""
        **Common issues and solutions:**

        1. **API Key Error:** Ensure `QUBRID_API_KEY` is set in `.env` file
        2. **File Upload Error:** Check that the file is a valid PDF or Markdown
        3. **Processing Timeout:** Try with a shorter resume or job description
        4. **Network Error:** Check your internet connection and try again

        If the problem persists, please check the logs or contact support.
        """)