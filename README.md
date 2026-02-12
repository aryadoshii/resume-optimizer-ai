![Qubrid AI Banner](frontend/assets/qubrid_banner.png)

# Resume-Optimizer-AI 🚀

> Transform your resume with Resume-Optimizer-AI . Get scored, receive personalized suggestions, and generate ATS optimized resumes tailored to any job all in seconds.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)


## ✨ Features

- **📊 Instant AI Scoring** - Get 0-10 scores across keyword optimization, ATS compatibility, experience relevance, and formatting
- **💡 Smart Suggestions** - Receive personalized, actionable recommendations before any changes are made
- **🎯 Job-Specific Tailoring** - AI rewrites your resume to match job requirements perfectly
- **📥 Multiple Formats** - Download as Markdown or professional PDF
- **🌓 Modern UI** - Sleek dark/light themes with intuitive design
- **📚 Complete History** - Track and restore all previous resume optimizations
- **⚡ Lightning Fast** - Powered by Mistral 7B via Qubrid API

---
## 📸 UI Screenshots

### 🎯 Upload & Evaluate
<img src="frontend/assets/1-upload.png" alt="Upload Resume" width="1000"/>

*Upload your resume and job description, then get instant AI-powered evaluation with progress tracking.*

---

### 📊 AI Scoring Dashboard
<img src="frontend/assets/2-scoring.png" alt="Resume Evaluation" width="1000"/>

*Receive detailed scores across 4 key metrics: Keyword Optimization, Experience Relevance, ATS-Friendliness, and Professional Formatting.*

---

### 💡 Personalized Suggestions
<img src="frontend/assets/3-suggestions.png" alt="Improvement Suggestions" width="1000"/>

*Get actionable, job-specific recommendations organized by category—review before generating your optimized resume.*

---

### 📄 Optimized Resume Preview
<img src="frontend/assets/4-resume.png" alt="Generated Resume" width="1000"/>

*Preview your AI-tailored resume with all suggestions applied, ready to download as Markdown or PDF.*

---

### 📚 History & Restore
<img src="frontend/assets/5-history.png" alt="Previous Generations" width="600"/>

*Access all past resume generations with scores and iteration counts. Click any chat to restore and review.*

---

### 🌓 Dark Mode Support
<img src="frontend/assets/6-dark-mode.png" alt="Dark Theme" width="1000"/>

*Beautiful dark and light themes with full accessibility and professional color-coded scoring.*

---

## 🏗️ System Architecture

<img src="frontend/assets/architecture.png" alt="System Architecture Diagram" width="1000"/>

*Resume-Optimizer-AI follows a streamlined 5-stage pipeline with persistent storage, ensuring every resume generation is tracked and restorable.*

---

## 🎯 How It Works

1. **Upload** → Add your resume (PDF/Markdown) and paste or upload the job description
2. **Evaluate** → Get instant AI scoring across 4 key metrics
3. **Review** → See personalized improvement suggestions before any changes
4. **Generate** → Create your optimized, ATS-friendly resume
5. **Download** → Export as Markdown or PDF

---

## 📁 Project Structure
```
resume-optimizer-ai/
├── backend/           # AI processing & workflow
├── config/            # Settings & prompts
├── data/              # User uploads & history database
├── frontend/          # Streamlit UI & components
│   └── assets/        # Screenshots & images
├── .env.example       # Environment template
└── run.sh            # One-command startup script
```

---

## 🛠️ Tech Stack

- **AI**: Mistral 7B via [Qubrid API](https://qubrid.com)
- **Workflow**: LangGraph for multi-step orchestration
- **UI**: Streamlit with custom themes
- **Storage**: SQLite for history tracking
- **Processing**: PyPDF2, WeasyPrint, python-docx

---

## 📊 Scoring Criteria

Your resume is evaluated on:
- **Keyword Optimization** - Job description alignment
- **Experience Relevance** - Skills & role match
- **ATS-Friendliness** - Applicant Tracking System compatibility
- **Professional Formatting** - Structure & readability

Each scored 0-10, averaged for overall score.

---

## 🎯 Use Cases

✅ **Job Seekers** - Tailor resumes for each application  
✅ **Career Coaches** - Help clients with AI-powered insights  
✅ **Recruiters** - Quickly improve candidate resumes  
✅ **Students** - Build professional resumes for internships  

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- [Qubrid API key](https://qubrid.com) (free tier available)
- UV package manager (recommended) or pip

### Installation
```bash
# 1. Clone the repository
git clone https://github.com/aryadoshii-qubrid/resume-optimizer-ai.git
cd resume-optimizer-ai

# 2. Set up your API key
cp .env.example .env
nano .env  # Add your QUBRID_API_KEY

# 3. Install dependencies (UV recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv pip install -r requirements.txt

# 4. Run the app
./run.sh
# OR: uv run streamlit run frontend/app.py   
```
---

## 📚 Learn More About Qubrid AI

Explore more applications and tutorials built on the Qubrid AI platform:

### 📖 Resources

- **[Qubrid Cookbook](https://github.com/QubridAI-Inc/qubrid-cookbook)** - Collection of example applications and integration guides
- **[Video Tutorials](https://youtube.com/playlist?list=PLoaE-lmLecgPoYuSa2BsmlJ8isKB5KFtq&si=bbR6pVatRWVtj9e0)** - Step-by-step tutorials and demos
- **[Qubrid Platform](https://platform.qubrid.com)** - Get your API key and explore documentation

---


<p align="center">
  <em>Made with ❤️ by Qubrid AI</em>
</p>