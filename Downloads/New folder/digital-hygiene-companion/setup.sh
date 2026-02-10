#!/bin/bash
# Digital Hygiene Companion - Quick Start Script (macOS/Linux)

set -e  # Exit on error

echo "🛡️  Digital Hygiene Companion - Setup Script"
echo "=============================================="
echo ""

# Check Python
echo "✓ Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 not found. Please install Python 3.8+"
    exit 1
fi
echo "  Found: $(python3 --version)"

# Check Node
echo "✓ Checking Node.js..."
if ! command -v node &> /dev/null; then
    echo "✗ Node.js not found. Please install Node.js 16+"
    exit 1
fi
echo "  Found: $(node --version)"

# Setup Backend
echo ""
echo "📦 Setting up Backend..."
cd backend

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt
echo "  ✓ Backend ready (install dependencies)"

cd ..

# Setup Frontend
echo ""
echo "📦 Setting up Frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    npm install -q
fi
echo "  ✓ Frontend ready (installed dependencies)"

cd ..

echo ""
echo "=============================================="
echo "✅ Setup Complete!"
echo ""
echo "🚀 To start the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then open: http://localhost:3000"
echo ""
echo "📖 Documentation:"
echo "  - README.md - Project overview"
echo "  - SETUP.md - Detailed setup guide"
echo "  - SAFETY_GUIDE.md - Usage and safety tips"
echo "  - ARCHITECTURE.md - Technical architecture"
echo ""
