"""Reusable UI components for Career-Sync-AI application."""

import streamlit as st
from datetime import datetime
from typing import Dict, Any, Optional
import os


def render_header(theme: str = "dark"):
    """Render application header with branding."""
    st.markdown(
        f"""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="font-size: 3em; margin-bottom: 0;">Career-Sync-AI</h1>
            <p style="font-size: 1.2em; {'color: #b0b0b0' if theme == 'dark' else 'color: #6b7280'}; margin-top: 10px;">
                AI-Powered Resume Tailoring with Mistral 7B
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


def render_progress_tracker(
    current_node: str,
    progress: float,
    status: str = "running"
):
    """
    Render live progress tracker for workflow execution.

    Args:
        current_node: Name of currently executing node
        progress: Progress percentage (0-100)
        status: Status message
    """
    # Node display names
    node_names = {
        "analyze_jd": "📊 Analyzing Job Description",
        "draft": "✍️ Drafting Tailored Resume",
        "critique": "🔍 Evaluating Resume Quality",
        "finalize": "✅ Finalizing Resume"
    }

    # Progress bar
    st.progress(progress / 100)

    # Current step with LLM indicator
    display_name = node_names.get(current_node, current_node)
    
    if current_node in ["analyze_jd", "draft", "critique"]:
        st.info(f"**Current Step:** {display_name}\n\n🤖 *Mistral 7B is processing...*")
    else:
        st.info(f"**Current Step:** {display_name}")

    # Status message
    if status:
        st.caption(status)


def render_critique_feedback(critique: Dict[str, Any]):
    """
    Render critique feedback in a formatted way.

    Args:
        critique: Critique dictionary with scores and feedback
    """
    st.markdown("### 📋 Resume Evaluation")
    st.info("💡 **What you're seeing:** AI evaluation scores for your NEW tailored resume")

    # Overall score with color coding
    overall_score = critique.get("overall_score", 0)
    score_color = "#10b981" if overall_score >= 8 else "#f59e0b" if overall_score >= 6 else "#ef4444"

    st.markdown(
        f"""
        <div style="text-align: center; padding: 20px; background-color: rgba(139, 92, 246, 0.1); 
                    border-radius: 8px; margin-bottom: 20px;">
            <h2 style="color: {score_color}; margin: 0;">{overall_score:.1f}/10</h2>
            <p style="margin: 5px 0 0 0;">Overall Score</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Individual scores
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Keyword Optimization", f"{critique.get('keyword_score', 0)}/10")
        st.metric("Experience Relevance", f"{critique.get('experience_score', 0)}/10")

    with col2:
        st.metric("ATS-Friendliness", f"{critique.get('ats_score', 0)}/10")
        st.metric("Professional Formatting", f"{critique.get('formatting_score', 0)}/10")

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
    Render previous generations in sidebar.

    Args:
        history: List of generation entries
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📚 Previous Generations")

    if not history:
        st.sidebar.info("No previous generations yet.")
        return

    for i, entry in enumerate(history[:5]):  # Show last 5
        timestamp = datetime.fromisoformat(entry["timestamp"])
        formatted_time = timestamp.strftime("%b %d, %I:%M %p")

        with st.sidebar.expander(
            f"{entry.get('job_title', 'Unknown')} - {formatted_time}",
            expanded=False
        ):
            st.write(f"**Company:** {entry.get('company', 'N/A')}")
            st.write(f"**Score:** {entry.get('final_score', 0):.1f}/10")
            st.write(f"**Iterations:** {entry.get('iterations', 0)}")

            # Download links
            output_files = entry.get("output_files", {})

            if output_files.get("markdown"):
                try:
                    with open(output_files["markdown"], "r") as f:
                        md_content = f.read()
                    st.download_button(
                        "📝 MD",
                        data=md_content,
                        file_name=f"resume_{i}.md",
                        key=f"md_{i}"
                    )
                except:
                    pass

            if output_files.get("pdf"):
                try:
                    with open(output_files["pdf"], "rb") as f:
                        pdf_content = f.read()
                    st.download_button(
                        "📄 PDF",
                        data=pdf_content,
                        file_name=f"resume_{i}.pdf",
                        key=f"pdf_{i}"
                    )
                except:
                    pass


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