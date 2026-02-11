# Career-Sync-AI 📄

AI-powered resume tailoring application that uses Mistral 7B (via Qubrid API) and LangGraph to automatically optimize resumes to match job descriptions.

## ✨ Features

- **AI-Powered Optimization**: Leverages Mistral 7B Instruct for intelligent resume tailoring
- **Self-Correcting Workflow**: Automatically iterates until quality threshold is met (max 3 iterations)
- **ATS-Friendly**: Optimized for Applicant Tracking Systems with keyword matching
- **Multiple Input Formats**: Supports PDF, Markdown, and text files
- **Dual Output**: Generate both Markdown and professional PDF resumes
- **History Tracking**: Keep track of all generated resumes with metadata
- **Modern UI**: Beautiful dark/light theme interface with real-time progress tracking
- **Fast Processing**: Complete workflow typically finishes in under 60 seconds

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher
- UV package manager
- Qubrid API key

### Installation

1. **Install UV** (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Clone or download the project**:
```bash
cd career-sync-ai
```

3. **Create `.env` file**:
```bash
cp .env.example .env
```

4. **Add your Qubrid API key** to `.env`:
```env
QUBRID_API_KEY=your_actual_api_key_here
```

5. **Install dependencies**:
```bash
uv pip install -e .
```

### Running the Application

```bash
uv run streamlit run frontend/app.py
```

The application will open in your default browser at `http://localhost:8501`.

## 📖 Usage Guide

### Step 1: Upload Resume

- Click "Upload your resume" in the sidebar
- Supported formats: PDF, Markdown (.md), Text (.txt)
- File should contain your complete resume

### Step 2: Provide Job Description

Choose one of two methods:

**Option A: Paste Text**
- Select "Paste Text" radio button
- Paste the job description in the text area

**Option B: Upload File**
- Select "Upload File" radio button
- Upload PDF or text file containing the job description

### Step 3: Generate Tailored Resume

- Click "🚀 Generate Tailored Resume" button
- Watch real-time progress as the AI:
  1. Analyzes the job description
  2. Drafts a tailored resume
  3. Critiques the quality
  4. Iterates if needed (up to 3 times)
  5. Finalizes the approved version

### Step 4: Download Results

- **Markdown**: Click "📝 Download Markdown" for editable format
- **PDF**: Click "📄 Download PDF" for professional, print-ready format

### Step 5: Review History

- Previous generations appear in the sidebar under "📚 Previous Generations"
- Each entry shows: job title, company, score, and iteration count
- Click to expand and download previous resumes

## 🏗️ Project Structure

```
career-sync-ai/
├── config/
│   ├── __init__.py           # Package initialization
│   ├── settings.py           # Environment variables & configuration
│   └── prompts.py            # System prompts for Mistral 7B
│
├── data/
│   ├── inputs/               # Temporary uploaded files
│   ├── outputs/              # Generated resumes (MD + PDF)
│   └── history/              # Generation history (JSON)
│
├── backend/
│   ├── __init__.py           # Package initialization
│   ├── state.py              # TypedDict state definition
│   ├── nodes.py              # LangGraph node functions
│   ├── graph.py              # Workflow definition
│   └── utils.py              # File handling utilities
│
├── frontend/
│   ├── app.py                # Main Streamlit application
│   ├── components.py         # Reusable UI components
│   └── styles.py             # Dark/Light theme CSS
│
├── .env                      # Environment variables (create from .env.example)
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
├── .python-version           # Python version (3.12)
├── pyproject.toml            # UV dependencies
└── README.md                 # This file
```

## ⚙️ Configuration

### Environment Variables

Edit `.env` to customize settings:

```env
# Required
QUBRID_API_KEY=your_key_here

# Optional - Model Parameters
MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.3
TEMPERATURE_ANALYSIS=0.3
TEMPERATURE_GENERATION=0.7
MAX_ITERATIONS=3
```

### Workflow Parameters

The workflow can be customized in `config/settings.py`:

- `max_iterations`: Maximum critique-draft loops (default: 3)
- `critique_threshold`: Minimum score to approve (default: 8.0/10)
- `max_retries`: API retry attempts (default: 3)
- `temperature_analysis`: Analysis tasks temperature (default: 0.3)
- `temperature_generation`: Generation tasks temperature (default: 0.7)

## 🔄 How It Works

### LangGraph Workflow

```
START
  ↓
[Analyze Job Description]
  ↓
[Draft Tailored Resume]
  ↓
[Critique Resume Quality]
  ↓
[Decision: Score >= 8.0?]
  ├─ Yes → [Finalize] → END
  └─ No → Loop back to [Draft] (max 3 times)
```

### Self-Correction Loop

The workflow automatically improves the resume through iterations:

1. **First Draft**: Creates initial tailored version
2. **Critique**: Evaluates on 5 criteria (0-10 each):
   - Keyword Optimization
   - Experience Relevance
   - ATS-Friendliness
   - Professional Formatting
   - Factual Accuracy
3. **Decision**:
   - If score ≥ 8.0: Approve and finalize
   - If score < 8.0: Generate improved draft
4. **Iteration**: Repeats up to 3 times or until approved

## 🎨 Themes

### Dark Mode (Default)
- Qubrid-branded purple/pink gradient accents
- Dark background (#1a1a2e)
- High contrast for readability

### Light Mode
- Clean professional blue/purple gradient
- White background
- Optimal for printing and daytime use

Toggle between themes using the radio button in the sidebar.

## 📊 Evaluation Criteria

Each resume is scored on:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Keyword Optimization | 20% | Natural incorporation of JD keywords |
| Experience Relevance | 20% | Highlighting of relevant experience |
| ATS-Friendliness | 20% | Compatibility with tracking systems |
| Professional Formatting | 20% | Clean structure and readability |
| Factual Accuracy | 20% | Maintains truthfulness from original |

**Overall Score**: Average of all criteria (0-10 scale)

## 🧪 Testing

### Test with Sample Files

1. **Prepare test resume** (PDF or Markdown):
```bash
# Example: test_resume.pdf
# Should contain typical resume sections:
# - Name & contact
# - Professional summary
# - Work experience
# - Education
# - Skills
```

2. **Prepare test job description**:
```bash
# Example: test_jd.txt
# Should contain:
# - Job title
# - Company name
# - Requirements
# - Responsibilities
# - Nice-to-haves
```

3. **Run test**:
```bash
uv run streamlit run frontend/app.py
# Upload test files
# Click "Generate Tailored Resume"
```

### Expected Behavior

✅ Files parse successfully  
✅ Progress bar updates for each node  
✅ Critique feedback displays between iterations  
✅ Final resume generates in 30-60 seconds  
✅ Both MD and PDF downloads work  
✅ Entry appears in history sidebar  

### Common Test Scenarios

**Scenario 1: Perfect Match (1 iteration)**
- Resume already well-aligned with JD
- Expected: 1 iteration, score ≥ 8.0

**Scenario 2: Needs Improvement (2-3 iterations)**
- Resume requires significant tailoring
- Expected: 2-3 iterations, progressive score improvement

**Scenario 3: Max Iterations (3 iterations)**
- Resume very different from JD requirements
- Expected: 3 iterations, best possible score achieved

## 🐛 Troubleshooting

### Issue: "QUBRID_API_KEY not set"

**Solution**: 
```bash
# Verify .env file exists
ls -la .env

# Check contents
cat .env

# Should contain:
QUBRID_API_KEY=your_actual_key_here
```

### Issue: "Failed to parse PDF"

**Solution**:
- Ensure PDF is not password-protected
- Try converting to text or Markdown first
- Check if PDF contains extractable text (not just images)

### Issue: "API call failed after 3 attempts"

**Solution**:
- Check internet connection
- Verify API key is valid
- Check Qubrid platform status
- Increase `retry_delay` in settings

### Issue: "Workflow timeout"

**Solution**:
- Reduce resume length (keep under 2000 words)
- Shorten job description (keep under 1000 words)
- Increase `max_tokens` in settings
- Check system resources

### Issue: "PDF generation failed"

**Solution**:
```bash
# Ensure reportlab is installed
uv pip install reportlab

# Check outputs directory is writable
ls -ld data/outputs/
```

### Issue: "Theme not applying"

**Solution**:
- Clear browser cache
- Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
- Try incognito/private browsing mode

## 🔒 Security Best Practices

1. **Never commit `.env` file** to version control
2. **Rotate API keys** regularly
3. **Don't share** generated resumes containing personal data
4. **Review** AI-generated content before use
5. **Keep dependencies updated**: `uv pip install --upgrade`

## 📝 Development

### Adding New Features

1. **New Prompt**: Edit `config/prompts.py`
2. **New Node**: Add to `backend/nodes.py`
3. **New UI Component**: Add to `frontend/components.py`
4. **New Theme**: Edit `frontend/styles.py`

### Code Style

- Follow PEP 8
- Use type hints everywhere
- Add docstrings to all functions
- Keep functions focused (single responsibility)
- Comment complex logic

### Dependencies Management

```bash
# Add new package
uv pip install package-name

# Update all packages
uv pip install --upgrade

# Export requirements
uv pip freeze > requirements.txt
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- **Qubrid**: AI platform and API
- **Mistral AI**: Mistral 7B Instruct model
- **LangGraph**: Agentic workflow framework
- **Streamlit**: Web application framework

## 📧 Support

For issues and questions:

1. Check this README's troubleshooting section
2. Review error messages carefully
3. Check logs in terminal
4. Create an issue on GitHub (if applicable)
5. Contact Qubrid support for API issues

## 🗺️ Roadmap

- [ ] Support for more LLM models
- [ ] Custom styling/templates for PDFs
- [ ] Multi-language support
- [ ] Cover letter generation
- [ ] LinkedIn profile optimization
- [ ] Batch processing for multiple JDs
- [ ] Advanced analytics dashboard
- [ ] Export to Google Docs/Word

---

**Version**: 0.1.0  
**Last Updated**: February 2026  
**Maintained by**: QubridAI Team
