# Career-Sync-AI - Quick Start Guide

Get up and running in **5 minutes**! 🚀

## Prerequisites

- Python 3.12+
- Internet connection
- Qubrid API key

## Installation

### 1. Install UV Package Manager

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After installation, restart your terminal.

### 2. Setup Environment

```bash
# Navigate to project directory
cd career-sync-ai

# Create .env file from template
cp .env.example .env

# Edit .env and add your API key
# Replace 'your_qubrid_api_key_here' with your actual key
nano .env  # or use any text editor
```

### 3. Install Dependencies

```bash
# Using the startup script (recommended)
chmod +x run.sh
./run.sh

# OR manually
uv pip install -e .
```

## Running the Application

### Option 1: Use Startup Script (Easiest)

```bash
./run.sh
```

### Option 2: Manual Start

```bash
uv run streamlit run frontend/app.py
```

The app will open automatically at: **http://localhost:8501**

## First Test

### 1. Upload Resume
- Click "Upload your resume" in sidebar
- Select `sample_resume.md` from project folder

### 2. Add Job Description
- Select "Upload File"
- Choose `sample_jd.txt`
- OR paste any job description text

### 3. Generate
- Click **"🚀 Generate Tailored Resume"**
- Wait 30-60 seconds
- Watch progress bar update

### 4. Download
- Click **"📝 Download Markdown"** for editable version
- Click **"📄 Download PDF"** for print-ready version

## Expected Results

✅ Processing completes in under 60 seconds  
✅ Resume gets 8+ score  
✅ Both downloads work  
✅ Entry appears in history  

## Troubleshooting

### "QUBRID_API_KEY not set"
➡️ Edit `.env` file and add your API key

### "UV not found"
➡️ Install UV: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### "Module not found"
➡️ Run: `uv pip install -e .`

### App won't start
➡️ Check Python version: `python --version` (should be 3.12+)

## What's Next?

1. ✅ Try with your own resume
2. ✅ Test different job descriptions
3. ✅ Explore Light/Dark theme toggle
4. ✅ Check history in sidebar
5. ✅ Read full README.md for advanced features

## Key Features

- **AI-Powered**: Uses Mistral 7B for intelligent tailoring
- **Self-Correcting**: Auto-improves through iterations
- **ATS-Optimized**: Keyword matching for tracking systems
- **Multi-Format**: PDF and Markdown support
- **History Tracking**: Keep all your tailored resumes

## Need Help?

📖 **Full Documentation**: See `README.md`  
🧪 **Testing Guide**: See `TESTING.md`  
📊 **Project Details**: See `PROJECT_SUMMARY.md`

## Support

- Check README troubleshooting section
- Verify .env configuration  
- Test with sample files first
- Review error messages carefully

---

**Ready to optimize your resume?** Let's go! 🎯
