@echo off
REM Digital Hygiene Companion - Quick Start Script (Windows)

setlocal enabledelayedexpansion

echo 🛡️  Digital Hygiene Companion - Setup Script
echo ============================================
echo.

REM Check Python
echo ✓ Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python not found. Please install Python 3.8+
    exit /b 1
)
for /f "tokens=*" %%a in ('python --version') do echo   Found: %%a

REM Check Node
echo ✓ Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Node.js not found. Please install Node.js 16+
    exit /b 1
)
for /f "tokens=*" %%a in ('node --version') do echo   Found: %%a

REM Setup Backend
echo.
echo 📦 Setting up Backend...
cd backend

if not exist venv (
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -q -r requirements.txt
echo   ✓ Backend ready (install dependencies)

cd ..

REM Setup Frontend
echo.
echo 📦 Setting up Frontend...
cd frontend

if not exist node_modules (
    call npm install -q
)
echo   ✓ Frontend ready (installed dependencies)

cd ..

echo.
echo ============================================
echo ✅ Setup Complete!
echo.
echo 🚀 To start the application:
echo.
echo Terminal 1 (Backend):
echo   cd backend
echo   venv\Scripts\activate.bat
echo   python main.py
echo.
echo Terminal 2 (Frontend):
echo   cd frontend
echo   npm run dev
echo.
echo Then open: http://localhost:3000
echo.
echo 📖 Documentation:
echo   - README.md - Project overview
echo   - SETUP.md - Detailed setup guide
echo   - SAFETY_GUIDE.md - Usage and safety tips
echo   - ARCHITECTURE.md - Technical architecture
echo.
