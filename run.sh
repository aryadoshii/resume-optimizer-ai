#!/bin/bash

# Resume-Optimizer-AI Startup Script

set -e

echo "🚀 Starting Resume-Optimizer-AI..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "❗ Please edit .env and add your QUBRID_API_KEY"
    echo "   Then run this script again."
    exit 1
fi

# Check if QUBRID_API_KEY is set
if grep -q "your_qubrid_api_key_here" .env; then
    echo "❗ Please set your QUBRID_API_KEY in .env file"
    exit 1
fi

echo "✅ Configuration verified"
echo ""

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo "⚠️  UV package manager not found!"
    echo "Installing UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo ""
    echo "✅ UV installed"
    echo "❗ Please restart your terminal and run this script again"
    exit 0
fi

echo "✅ UV found"
echo ""

# Install dependencies if needed
if [ ! -d ".venv" ]; then
    echo "📦 Installing dependencies..."
    uv pip install -r requirements.txt
    echo "✅ Dependencies installed"
    echo ""
fi

# Start the application
echo "🎯 Launching Streamlit application..."
echo ""
echo "📱 Application will open at: http://localhost:8501"
echo "   Press Ctrl+C to stop the server"
echo ""

uv run streamlit run frontend/app.py