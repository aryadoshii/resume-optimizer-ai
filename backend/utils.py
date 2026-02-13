"""Utility functions for file processing."""

from pathlib import Path
import PyPDF2
import markdown

# Data directories
DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUTS_DIR = DATA_DIR / "outputs"


def parse_pdf(file_path: Path) -> str:
    """
    Extract text from PDF file.
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        Extracted text
    """
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            text_parts = []
            for page in pdf_reader.pages:
                text_parts.append(page.extract_text())
            
            return "\n\n".join(text_parts)
            
    except Exception as e:
        raise ValueError(f"Failed to parse PDF: {str(e)}")


def parse_text_file(file_path: Path) -> str:
    """
    Read text from .txt or .md file.
    
    Args:
        file_path: Path to text file
        
    Returns:
        File contents
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        raise ValueError(f"Failed to read file: {str(e)}")


def validate_file_type(filename: str, allowed_extensions: list) -> bool:
    """
    Check if file extension is allowed.
    
    Args:
        filename: Name of file
        allowed_extensions: List like ['.pdf', '.txt', '.md']
        
    Returns:
        True if valid, False otherwise
    """
    return any(filename.lower().endswith(ext) for ext in allowed_extensions)


def save_markdown(content: str, filename: str) -> Path:
    """
    Save resume as markdown file.
    
    Args:
        content: Markdown text
        filename: Base filename (without extension)
        
    Returns:
        Path to saved file
    """
    output_path = OUTPUTS_DIR / f"{filename}.md"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return output_path


def convert_markdown_to_pdf(content: str, filename: str) -> Path:
    """
    Convert markdown to styled PDF.
    
    Args:
        content: Markdown text
        filename: Base filename (without extension)
        
    Returns:
        Path to generated PDF
    """
    # Lazy import WeasyPrint (only when needed)
    try:
        from weasyprint import HTML
    except Exception as e:
        raise ImportError(
            "WeasyPrint not available. On macOS, install dependencies:\n"
            "brew install cairo pango gdk-pixbuf libffi\n"
            f"Error: {str(e)}"
        )
    
    # Convert markdown to HTML
    html_content = markdown.markdown(
        content,
        extensions=['extra', 'nl2br']
    )
    
    # Wrap in styled HTML
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{
                size: A4;
                margin: 2cm;
            }}
            body {{
                font-family: 'Arial', 'Helvetica', sans-serif;
                font-size: 11pt;
                line-height: 1.6;
                color: #333;
            }}
            h1 {{
                color: #2c3e50;
                font-size: 24pt;
                margin-bottom: 10pt;
                border-bottom: 2px solid #3498db;
                padding-bottom: 5pt;
            }}
            h2 {{
                color: #34495e;
                font-size: 16pt;
                margin-top: 15pt;
                margin-bottom: 8pt;
            }}
            h3 {{
                color: #7f8c8d;
                font-size: 13pt;
                margin-top: 10pt;
                margin-bottom: 5pt;
            }}
            ul, ol {{
                margin-left: 20pt;
            }}
            li {{
                margin-bottom: 3pt;
            }}
            a {{
                color: #3498db;
                text-decoration: none;
            }}
            strong {{
                color: #2c3e50;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Generate PDF
    output_path = OUTPUTS_DIR / f"{filename}.pdf"
    HTML(string=full_html).write_pdf(output_path)
    
    return output_path