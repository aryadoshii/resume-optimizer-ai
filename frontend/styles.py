"""Custom CSS themes for Career-Sync-AI application."""

DARK_THEME_CSS = """
<style>
    /* Dark Theme - Qubrid Branded */
    
    :root {
        --bg-primary: #1a1a2e;
        --bg-secondary: #252538;
        --bg-elevated: #2d2d44;
        --text-primary: #e0e0e0;
        --text-secondary: #b0b0b0;
        --accent-purple: #8B5CF6;
        --accent-pink: #EC4899;
        --border-color: #3d3d5c;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
    }
    
    .stApp {
        background-color: var(--bg-primary);
        color: var(--text-primary);
    }
    
    /* Remove white header bar */
    header {
        background-color: var(--bg-primary) !important;
    }
    
    .stApp > header {
        background-color: transparent !important;
    }
    
    [data-testid="stHeader"] {
        background-color: var(--bg-primary) !important;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
        border-right: 1px solid var(--border-color);
    }
    
    section[data-testid="stSidebar"] * {
        color: var(--text-primary) !important;
    }
    
    /* Fix all text visibility */
    p, span, div, label, h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background-color: var(--bg-elevated);
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color);
        border-radius: 8px;
    }
    
    /* Fix placeholder visibility in dark mode */
    .stTextArea > div > div > textarea::placeholder {
        color: #6b7280 !important;
        opacity: 1;
    }
    
    /* File uploader fix for dark mode */
    .stFileUploader section {
        color: var(--text-primary) !important;
    }

    .stFileUploader label {
        color: var(--text-primary) !important;
    }

    .stFileUploader [data-testid="stFileUploaderFileName"] {
        color: var(--text-primary) !important;
    }
    
    .stFileUploader small {
        color: var(--text-secondary) !important;
    }
    
    /* File uploader */
    .stFileUploader {
        background-color: var(--bg-elevated);
        border: 2px dashed var(--border-color);
        border-radius: 8px;
        padding: 20px;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-purple) 0%, var(--accent-pink) 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(139, 92, 246, 0.4);
    }
    
    .stDownloadButton > button {
        background: var(--bg-elevated);
        color: var(--text-primary) !important;
        border: 1px solid var(--accent-purple);
        border-radius: 8px;
        padding: 10px 20px;
    }
    
    .stDownloadButton > button:hover {
        background: var(--accent-purple);
        color: white !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--accent-purple) 0%, var(--accent-pink) 100%);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: var(--bg-elevated);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        color: var(--text-primary) !important;
    }
    
    .streamlit-expanderContent {
        background-color: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 0 0 8px 8px;
    }
    
    /* Cards/Containers */
    .element-container {
        background-color: transparent;
    }
    
    /* Success/Error/Warning boxes */
    .stSuccess {
        background-color: rgba(16, 185, 129, 0.1);
        border-left: 4px solid var(--success);
        padding: 12px;
        border-radius: 4px;
        color: var(--text-primary) !important;
    }
    
    .stError {
        background-color: rgba(239, 68, 68, 0.1);
        border-left: 4px solid var(--error);
        padding: 12px;
        border-radius: 4px;
        color: var(--text-primary) !important;
    }
    
    .stWarning, .stInfo {
        background-color: rgba(139, 92, 246, 0.1);
        border-left: 4px solid var(--accent-purple);
        padding: 12px;
        border-radius: 4px;
        color: var(--text-primary) !important;
    }
    
    /* Code blocks */
    code {
        background-color: var(--bg-elevated);
        color: var(--accent-pink) !important;
        padding: 2px 6px;
        border-radius: 4px;
    }
    
    pre {
        background-color: var(--bg-elevated);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 16px;
    }
    
    /* Markdown */
    .stMarkdown {
        color: var(--text-primary) !important;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: var(--text-primary) !important;
    }
    
    /* Headers with gradient */
    h1 {
        background: linear-gradient(135deg, var(--accent-purple) 0%, var(--accent-pink) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: var(--success) !important;
    }
</style>
"""

LIGHT_THEME_CSS = """
<style>
    /* Light Theme - Clean & Professional */
    
    :root {
        --bg-primary: #ffffff;
        --bg-secondary: #f9fafb;
        --bg-elevated: #f3f4f6;
        --text-primary: #1f2937;
        --text-secondary: #6b7280;
        --accent-blue: #3B82F6;
        --accent-purple: #8B5CF6;
        --border-color: #e5e7eb;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
    }
    
    .stApp {
        background-color: var(--bg-primary);
        color: var(--text-primary);
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-elevated) 100%);
        border-right: 1px solid var(--border-color);
    }
    
    section[data-testid="stSidebar"] * {
        color: var(--text-primary) !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background-color: var(--bg-primary);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-blue);
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
    }
    
    /* File uploader */
    .stFileUploader {
        background-color: var(--bg-secondary);
        border: 2px dashed var(--border-color);
        border-radius: 8px;
        padding: 20px;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-purple) 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(59, 130, 246, 0.3);
    }
    
    .stDownloadButton > button {
        background: var(--bg-primary);
        color: var(--text-primary);
        border: 1px solid var(--accent-blue);
        border-radius: 8px;
        padding: 10px 20px;
    }
    
    .stDownloadButton > button:hover {
        background: var(--accent-blue);
        color: white;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--accent-blue) 0%, var(--accent-purple) 100%);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        color: var(--text-primary);
    }
    
    .streamlit-expanderContent {
        background-color: var(--bg-primary);
        border: 1px solid var(--border-color);
        border-radius: 0 0 8px 8px;
    }
    
    /* Success/Error/Warning boxes */
    .stSuccess {
        background-color: rgba(16, 185, 129, 0.1);
        border-left: 4px solid var(--success);
        padding: 12px;
        border-radius: 4px;
    }
    
    .stError {
        background-color: rgba(239, 68, 68, 0.1);
        border-left: 4px solid var(--error);
        padding: 12px;
        border-radius: 4px;
    }
    
    .stWarning {
        background-color: rgba(245, 158, 11, 0.1);
        border-left: 4px solid var(--warning);
        padding: 12px;
        border-radius: 4px;
    }
    
    /* Code blocks */
    code {
        background-color: var(--bg-elevated);
        color: var(--accent-purple);
        padding: 2px 6px;
        border-radius: 4px;
    }
    
    pre {
        background-color: var(--bg-elevated);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 16px;
    }
    
    /* Markdown */
    .stMarkdown {
        color: var(--text-primary);
    }
    
    /* Headers with gradient */
    h1 {
        background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-purple) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
</style>
"""


def get_theme_css(theme: str = "dark") -> str:
    """
    Get CSS for the specified theme.

    Args:
        theme: "dark" or "light"

    Returns:
        CSS string for the theme
    """
    if theme == "light":
        return LIGHT_THEME_CSS
    return DARK_THEME_CSS