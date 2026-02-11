"""Main Streamlit application for Career-Sync-AI."""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
from datetime import datetime
import tempfile
import os

from backend import create_resume_workflow
from backend.state import ResumeState
from backend.utils import (
    parse_pdf,
    parse_text_file,
    save_markdown,
    convert_markdown_to_pdf,
    save_generation_history,
    load_generation_history,
    validate_file_type
)
from backend.nodes import call_llm_with_retry, draft_tailored_resume, critique_resume, finalize_resume, analyze_job_description
from frontend.styles import get_theme_css
from frontend.components import (
    render_header,
    render_theme_toggle,
    render_file_uploader,
    render_critique_feedback,
    render_resume_preview,
    render_download_buttons,
    render_history_sidebar,
    render_error_message
)
from config.settings import settings, INPUTS_DIR


# Page configuration
st.set_page_config(
    page_title="Career-Sync-AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


def initialize_session_state():
    """Initialize session state variables."""
    if "workflow_running" not in st.session_state:
        st.session_state.workflow_running = False
    if "final_state" not in st.session_state:
        st.session_state.final_state = None
    if "suggestions" not in st.session_state:
        st.session_state.suggestions = None
    if "current_state" not in st.session_state:
        st.session_state.current_state = None
    if "evaluation_done" not in st.session_state:
        st.session_state.evaluation_done = False
    if "initial_critique" not in st.session_state:
        st.session_state.initial_critique = None


def parse_job_description_input(text_input, file_input) -> tuple[str, str]:
    """Parse job description from text or file input."""
    if text_input and text_input.strip():
        return text_input.strip(), "pasted_text"

    if file_input is not None:
        temp_path = INPUTS_DIR / file_input.name
        with open(temp_path, "wb") as f:
            f.write(file_input.getbuffer())

        if file_input.name.lower().endswith('.pdf'):
            content = parse_pdf(temp_path)
        else:
            content = parse_text_file(temp_path)

        temp_path.unlink()
        return content, file_input.name

    raise ValueError("Please provide a job description (paste text or upload file)")


def parse_resume_input(file_input) -> tuple[str, str]:
    """Parse resume from file input."""
    if file_input is None:
        raise ValueError("Please upload a resume file")

    if not validate_file_type(file_input.name, ['.pdf', '.md', '.txt']):
        raise ValueError("Invalid file type. Please upload PDF or Markdown file.")

    temp_path = INPUTS_DIR / file_input.name
    with open(temp_path, "wb") as f:
        f.write(file_input.getbuffer())

    try:
        if file_input.name.lower().endswith('.pdf'):
            content = parse_pdf(temp_path)
        else:
            content = parse_text_file(temp_path)
        return content, file_input.name
    finally:
        if temp_path.exists():
            temp_path.unlink()


def evaluate_resume(resume_content: str, resume_filename: str, jd_content: str, jd_source: str):
    """STEP 1: Evaluate resume against JD and show metrics + suggestions."""
    
    initial_state: ResumeState = {
        "original_resume": resume_content,
        "job_description": jd_content,
        "resume_filename": resume_filename,
        "jd_source": jd_source,
        "draft_resume": resume_content,  # Use original for initial critique
        "iteration": 0,
        "metadata": {
            "start_time": datetime.now().isoformat(),
            "model": settings.model_name
        }
    }
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Step 1: Analyze JD
    status_text.info("📊 Analyzing job description...")
    progress_bar.progress(25)
    
    jd_result = analyze_job_description(initial_state)
    initial_state.update(jd_result)
    
    # Step 2: Evaluate current resume
    status_text.info("🔍 Evaluating your resume against requirements...")
    progress_bar.progress(50)
    
    critique_result = critique_resume(initial_state)
    initial_state.update(critique_result)
    
    # Step 3: Generate suggestions
    status_text.info("💡 Generating improvement suggestions...")
    progress_bar.progress(75)
    
    from backend.graph import draft_suggestions_only
    suggestions_result = draft_suggestions_only(initial_state)
    initial_state.update(suggestions_result)
    
    progress_bar.progress(100)
    status_text.empty()
    progress_bar.empty()
    
    # Store results
    st.session_state.current_state = initial_state
    st.session_state.initial_critique = initial_state.get("critique")
    st.session_state.suggestions = initial_state.get("suggestions")
    st.session_state.evaluation_done = True
    st.rerun()


def create_final_resume():
    """STEP 2: Create tailored resume with progress tracking."""
    
    current_state = st.session_state.current_state
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Step 1: Drafting
    status_text.info("✍️ Tailoring your resume...")
    progress_bar.progress(33)
    
    draft_result = draft_tailored_resume(current_state)
    current_state.update(draft_result)
    
    # Step 2: Final evaluation
    status_text.info("🔍 Quality check...")
    progress_bar.progress(66)
    
    critique_result = critique_resume(current_state)
    current_state.update(critique_result)
    
    # Step 3: Finalizing
    status_text.info("✅ Finalizing your resume...")
    progress_bar.progress(90)
    
    finalize_result = finalize_resume(current_state)
    current_state.update(finalize_result)
    
    # Save files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_base = f"resume_{timestamp}"
    
    markdown_path = save_markdown(current_state["final_resume"], filename_base)
    pdf_path = convert_markdown_to_pdf(current_state["final_resume"], filename_base)
    
    current_state["output_pdf_path"] = str(pdf_path)
    
    save_generation_history(current_state, {
        "markdown": str(markdown_path),
        "pdf": str(pdf_path)
    })
    
    progress_bar.progress(100)
    status_text.empty()
    progress_bar.empty()
    
    st.session_state.final_state = current_state
    st.rerun()


def main():
    """Main application function."""
    initialize_session_state()

    theme = render_theme_toggle()
    st.markdown(get_theme_css(theme), unsafe_allow_html=True)
    render_header(theme)

    # Sidebar
    st.sidebar.markdown("---")
    resume_file = render_file_uploader(
        "Upload your resume",
        ["pdf", "md", "txt"],
        "resume_upload",
        "PDF or Markdown"
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 Job Description")

    jd_input_method = st.sidebar.radio(
        "Input method:",
        ["Paste Text", "Upload File"],
        label_visibility="collapsed"
    )

    jd_text = None
    jd_file = None

    if jd_input_method == "Paste Text":
        jd_text = st.sidebar.text_area(
            "Paste job description",
            height=200,
            placeholder="Paste the job description here...",
            label_visibility="collapsed"
        )
    else:
        jd_file = render_file_uploader(
            "Upload job description",
            ["pdf", "txt", "md"],
            "jd_upload",
            "PDF or text file"
        )

    st.sidebar.markdown("---")

    history = load_generation_history()
    render_history_sidebar(history)

    # Main Content
    if st.session_state.final_state:
        # FINAL: Show tailored resume WITH suggestions
        final_state = st.session_state.final_state
        
        st.success("✅ Your Tailored Resume is Ready!")
        
        # Show before/after comparison
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Original Score", f"{st.session_state.initial_critique.get('overall_score', 0):.1f}/10")
        with col2:
            st.metric("New Score", f"{final_state['critique'].get('overall_score', 0):.1f}/10", 
                     delta=f"+{final_state['critique'].get('overall_score', 0) - st.session_state.initial_critique.get('overall_score', 0):.1f}")
        
        st.markdown("---")
        
        # Show suggestions in collapsible expander
        if st.session_state.suggestions:
            with st.expander("💡 View Improvement Suggestions Applied", expanded=False):
                suggestions = st.session_state.suggestions
                for i, sug in enumerate(suggestions, 1):
                    category = sug.get("category", "Suggestion")
                    text = sug.get("suggestion", "")
                    st.markdown(f"**{i}. {category}:** {text}")
        
        st.markdown("---")
        
        render_resume_preview(final_state["final_resume"])
        
        if final_state.get("output_pdf_path"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            render_download_buttons(
                final_state["final_resume"],
                final_state["output_pdf_path"],
                f"resume_{timestamp}"
            )
        
        st.markdown("---")
        
        # Reset button
        col1, col2, col3 = st.columns([2, 2, 2])
        with col2:
            if st.button("🔄 Start New Resume", use_container_width=True):
                st.session_state.final_state = None
                st.session_state.suggestions = None
                st.session_state.current_state = None
                st.session_state.evaluation_done = False
                st.session_state.initial_critique = None
                st.rerun()
    
    elif st.session_state.evaluation_done:
        # STEP 2: Show evaluation + suggestions + generate button
        
        st.success("✅ Evaluation Complete!")
        
        # Show initial evaluation
        if st.session_state.initial_critique:
            render_critique_feedback(st.session_state.initial_critique)
        
        st.markdown("---")
        
        # Show suggestions
        if st.session_state.suggestions:
            st.markdown("### 💡 Improvement Suggestions")
            st.caption("These will be applied to your tailored resume")
            
            suggestions = st.session_state.suggestions
            for i, sug in enumerate(suggestions, 1):
                category = sug.get("category", "Suggestion")
                text = sug.get("suggestion", "")
                
                with st.expander(f"**{i}. {category}**", expanded=True):
                    st.write(text)
        
        st.markdown("---")
        
        # Generate button
        col1, col2, col3 = st.columns([2, 2, 2])
        with col2:
            if st.button("🚀 Generate Tailored Resume", type="primary", use_container_width=True, key="generate_resume"):
                create_final_resume()
    
    else:
        # STEP 1: Welcome + Evaluate button
        st.markdown("""
## 👋 Transform Your Resume with AI

**Get scored. Get suggestions. Get hired.**

### How it works:

1. **Evaluate** - See how your resume scores
2. **Review** - Check AI suggestions  
3. **Generate** - Download optimized resume

### ✨ Powered by Mistral 7B

✅ ATS optimization  
✅ Keyword matching  
✅ Professional formatting  

**Ready?** Upload files in the sidebar →
""")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Evaluate button
        col1, col2, col3 = st.columns([2, 2, 2])
        with col2:
            evaluate_button = st.button(
                "📊 Evaluate Resume vs Job",
                type="primary",
                use_container_width=True,
                disabled=st.session_state.workflow_running
            )
        
        if evaluate_button:
            try:
                resume_content, resume_filename = parse_resume_input(resume_file)
                jd_content, jd_source = parse_job_description_input(jd_text, jd_file)
                
                evaluate_resume(resume_content, resume_filename, jd_content, jd_source)

            except ValueError as e:
                render_error_message(str(e))
            except Exception as e:
                render_error_message(f"Error: {str(e)}")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; padding: 10px; opacity: 0.6;">
            <p style="font-size: 0.9em;">Powered by Mistral 7B • Built with LangGraph & Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()