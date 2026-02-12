# Resume-Optimizer-AI 🚀

> AI-powered resume optimizer that scores your resume, provides personalized improvement suggestions, and generates ATS-optimized versions tailored to any job description.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ Features

- **📊 AI Resume Scoring**: Get instant ATS compatibility scores (0-10) across multiple criteria
- **💡 Smart Suggestions**: Receive personalized, actionable improvement recommendations
- **🎯 Job-Specific Optimization**: Tailor your resume to match any job description
- **📄 Multiple Formats**: Download as Markdown or professional PDF
- **🌓 Modern UI**: Beautiful dark/light theme interface
- **📚 History Tracking**: Access all your previous resume optimizations
- **⚡ Fast Processing**: Powered by Mistral 7B via Qubrid API

## 🎬 How It Works

1. **Evaluate** - Upload your resume and job description to get scored
2. **Review** - See AI-powered improvement suggestions  
3. **Optimize** - Generate and download your optimized resume

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher
- [UV package manager](https://github.com/astral-sh/uv) (recommended) or pip
- Qubrid API key ([Get one here](https://qubrid.com))

### Installation

1. **Clone the repository**
```bash
   git clone https://github.com/aryadoshii-qubrid/resume-optimizer-ai.git
   cd resume-optimizer-ai
```

2. **Set up environment**
```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your Qubrid API key
   nano .env  # or use your preferred editor
```

3. **Install dependencies**
   
   **Using UV (recommended):**
```bash
   # Install UV if not already installed
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Install dependencies
   uv pip install -r requirements.txt
```
   
   **Using pip:**
```bash
   pip install -r requirements.txt
```

4. **Run the application**
```bash
   # Easy way (uses run.sh)
   chmod +x run.sh
   ./run.sh
   
   # OR manual way
   streamlit run frontend/app.py
```

5. **Open your browser**
   
   Navigate to `http://localhost:8501`

## 📁 Project Structure
```
resume-optimizer-ai/
├── backend/              # Core optimization logic
│   ├── graph.py         # LangGraph workflow
│   ├── nodes.py         # AI processing nodes
│   ├── state.py         # State management
│   ├── utils.py         # Utility functions
│   └── database.py      # SQLite storage
├── config/              # Configuration
│   ├── prompts.py       # AI prompts
│   └── settings.py      # App settings
├── data/                # User data storage
│   ├── inputs/          # Uploaded files
│   ├── outputs/         # Generated resumes
│   └── career_sync.db   # History database
├── frontend/            # UI components
│   ├── app.py          # Main Streamlit app
│   ├── components.py   # Reusable UI components
│   └── styles.py       # Theme styling
├── .env.example        # Environment template
├── requirements.txt    # Python dependencies
└── run.sh             # Startup script
```

## 🔧 Configuration

Edit `.env` file to customize:
```bash
# Required
QUBRID_API_KEY=your_api_key_here
QUBRID_BASE_URL=https://api.qubrid.com/v1

# Optional (defaults provided)
MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.3
MAX_TOKENS=8192
TEMPERATURE=0.7
```

## 🎯 Use Cases

- **Job Seekers**: Optimize resumes for specific job applications
- **Career Coaches**: Help clients improve their resumes with AI insights
- **Recruiters**: Quickly assess and improve candidate resumes
- **Students**: Prepare professional resumes for internships and jobs

## 🛠️ Tech Stack

- **AI Model**: Mistral 7B Instruct via Qubrid API
- **Framework**: LangGraph for multi-agent workflow orchestration
- **Frontend**: Streamlit with custom dark/light themes
- **Database**: SQLite for history tracking
- **File Processing**: PyPDF2, python-docx, WeasyPrint

## 📊 Scoring Criteria

Your resume is scored across:
- **Keyword Optimization** (0-10): Job description keyword matching
- **Experience Relevance** (0-10): Alignment with job requirements
- **ATS-Friendliness** (0-10): Applicant Tracking System compatibility
- **Professional Formatting** (0-10): Structure and readability

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Powered by [Qubrid AI](https://qubrid.com)
- Built with [Mistral 7B](https://mistral.ai/)
- UI framework: [Streamlit](https://streamlit.io/)
- Workflow: [LangGraph](https://github.com/langchain-ai/langgraph)

## 📧 Support

For issues or questions:
- Open an [issue](https://github.com/aryadoshii-qubrid/resume-optimizer-ai/issues)
- Contact: [Qubrid Support](https://qubrid.com/support)

---

**Made with ❤️ by the Qubrid AI Team**