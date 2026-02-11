"""Utility functions for file handling, parsing, and conversion."""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import markdown

from config.settings import OUTPUTS_DIR, HISTORY_DIR


def parse_pdf(file_path: Path) -> str:
    """
    Extract text from a PDF file.

    Args:
        file_path: Path to the PDF file

    Returns:
        Extracted text content

    Raises:
        ValueError: If file is not a valid PDF or cannot be read
    """
    try:
        reader = PdfReader(str(file_path))
        text_parts = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)

        if not text_parts:
            raise ValueError("No text could be extracted from PDF")

        return "\n\n".join(text_parts)

    except Exception as e:
        raise ValueError(f"Failed to parse PDF: {str(e)}")


def parse_text_file(file_path: Path) -> str:
    """
    Read text from a .txt or .md file.

    Args:
        file_path: Path to the text file

    Returns:
        File content as string

    Raises:
        ValueError: If file cannot be read
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if not content.strip():
            raise ValueError("File is empty")

        return content

    except Exception as e:
        raise ValueError(f"Failed to read text file: {str(e)}")


def save_markdown(content: str, filename: Optional[str] = None) -> Path:
    """
    Save content as a Markdown file.

    Args:
        content: Markdown content to save
        filename: Optional custom filename (without extension)

    Returns:
        Path to the saved file
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resume_{timestamp}"

    filepath = OUTPUTS_DIR / f"{filename}.md"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath


def convert_markdown_to_pdf(
    markdown_content: str,
    output_filename: Optional[str] = None
) -> Path:
    """
    Convert Markdown content to a professional PDF resume.

    Args:
        markdown_content: Resume content in Markdown format
        output_filename: Optional custom filename (without extension)

    Returns:
        Path to the generated PDF file
    """
    if output_filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"resume_{timestamp}"

    pdf_path = OUTPUTS_DIR / f"{output_filename}.pdf"

    # Create PDF document
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    # Define styles
    styles = getSampleStyleSheet()

    # Custom styles for resume
    title_style = ParagraphStyle(
        'ResumeTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor='#1a1a2e',
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading_style = ParagraphStyle(
        'ResumeHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#2d2d44',
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'ResumeBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor='#1f2937',
        spaceAfter=4,
        leading=14,
        fontName='Helvetica'
    )

    bullet_style = ParagraphStyle(
        'ResumeBullet',
        parent=styles['Normal'],
        fontSize=10,
        textColor='#1f2937',
        leftIndent=20,
        spaceAfter=4,
        leading=14,
        fontName='Helvetica'
    )

    # Parse Markdown into flowables
    story = []
    lines = markdown_content.split('\n')

    for line in lines:
        line = line.strip()

        if not line:
            story.append(Spacer(1, 0.1 * inch))
            continue

        # H1 - Name/Title
        if line.startswith('# '):
            text = line[2:].strip()
            story.append(Paragraph(text, title_style))

        # H2 - Section headers
        elif line.startswith('## '):
            text = line[3:].strip()
            story.append(Paragraph(text, heading_style))

        # H3 - Subsection headers
        elif line.startswith('### '):
            text = line[4:].strip()
            story.append(Paragraph(f"<b>{text}</b>", body_style))

        # Bullet points
        elif line.startswith('- ') or line.startswith('* '):
            text = line[2:].strip()
            story.append(Paragraph(f"• {text}", bullet_style))

        # Bold text
        elif '**' in line:
            text = line.replace('**', '<b>', 1).replace('**', '</b>', 1)
            story.append(Paragraph(text, body_style))

        # Regular text
        else:
            story.append(Paragraph(line, body_style))

    # Build PDF
    doc.build(story)

    return pdf_path


def save_generation_history(
    state: Dict[str, Any],
    output_files: Dict[str, str]
) -> None:
    """
    Save resume generation to history file.

    Args:
        state: Final workflow state
        output_files: Dictionary with 'markdown' and 'pdf' file paths
    """
    history_file = HISTORY_DIR / "generations.json"

    # Load existing history
    if history_file.exists():
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
    else:
        history = []

    # Extract job info from analysis
    jd_analysis = state.get("jd_analysis", {})
    critique = state.get("critique", {})

    # Create new entry
    entry = {
        "timestamp": datetime.now().isoformat(),
        "original_resume_name": state.get("resume_filename", "unknown"),
        "job_title": jd_analysis.get("job_title", "Not specified"),
        "company": jd_analysis.get("company", "Not specified"),
        "iterations": state.get("iteration", 0),
        "final_score": critique.get("overall_score", 0),
        "output_files": output_files,
        "metadata": state.get("metadata", {})
    }

    # Append and save
    history.append(entry)

    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def load_generation_history() -> list:
    """
    Load resume generation history.

    Returns:
        List of generation entries, newest first
    """
    history_file = HISTORY_DIR / "generations.json"

    if not history_file.exists():
        return []

    try:
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
        return list(reversed(history))  # Newest first
    except Exception:
        return []


def extract_json_from_text(text: str) -> Dict[str, Any]:
    """
    Extract JSON object from text that may contain markdown or other content.

    Args:
        text: Text that may contain JSON

    Returns:
        Parsed JSON object

    Raises:
        ValueError: If no valid JSON found
    """
    # Try direct parsing first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Look for JSON in code blocks
    json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
    matches = re.findall(json_pattern, text, re.DOTALL)

    if matches:
        try:
            return json.loads(matches[0])
        except json.JSONDecodeError:
            pass

    # Look for raw JSON object
    json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.findall(json_pattern, text, re.DOTALL)

    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue

    raise ValueError("No valid JSON found in response")


def validate_file_type(filename: str, allowed_extensions: list) -> bool:
    """
    Validate file extension.

    Args:
        filename: Name of the file
        allowed_extensions: List of allowed extensions (e.g., ['.pdf', '.md'])

    Returns:
        True if valid, False otherwise
    """
    return any(filename.lower().endswith(ext) for ext in allowed_extensions)
