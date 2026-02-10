# Digital Hygiene Companion - Development Environment Setup

## Python Version Requirements

**✅ Tested & Working:** Python 3.10, 3.11, 3.12, 3.13, 3.14

> **Python 3.14 Note:** Due to wheel availability for Python 3.14, the project uses Pydantic v1.10.26 instead of v2. This is fully compatible and works perfectly with all features.

Check your Python version:
```bash
python --version
```

## Quick Start Setup

### Option 1: Manual Setup (Recommended for development)

#### Backend Setup
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
python main.py
# Backend runs on http://localhost:8000
```

#### Frontend Setup (in a new terminal)
```bash
cd frontend
npm install
npm run dev
# Frontend runs on http://localhost:3000
```

### Option 2: Docker Setup

```bash
docker-compose up
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

## API Endpoints

### Text Analysis
```
POST /api/analyze/text
Content-Type: application/json

{
  "content": "Your suspicious text here",
  "content_type": "email|message|sms|post"
}
```

### URL Analysis
```
POST /api/analyze/url
Content-Type: application/json

{
  "url": "https://example.com",
  "context": "email|chat|web|social|unknown"
}
```

## Testing the Application

### Test Case 1: Obvious Phishing
```
Text: "Dear Valued Customer, Your bank account has been suspended. Please verify your account by clicking here and entering your password."
Expected: HIGH or CRITICAL risk
```

### Test Case 2: Legitimate Email
```
Text: "Hi John, Here's the project report you requested. Best regards, Sarah"
Expected: LOW risk
```

### Test Case 3: Suspicious URL
```
URL: "http://paypal-secure.tk/verify-account"
Expected: HIGH risk
```

## Troubleshooting

### Backend won't start
- Ensure Python 3.8+: `python --version`
- Check all dependencies installed: `pip list | grep -E "fastapi|uvicorn"`
- Clear cache: `pip cache purge` and reinstall

### Frontend won't start
- Ensure Node 16+: `node --version`
- Delete node_modules: `rm -rf node_modules`
- Reinstall: `npm install`

### API requests failing
- Check backend is running: `curl http://localhost:8000/health`
- Check CORS headers in response
- Ensure ports 8000 and 3000 are not in use

## Environment Configuration

### Backend (.env)
```
DEBUG=false
LOG_LEVEL=INFO
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
```

## Performance Tips

- Keep the application window active to prevent thread throttling
- Close unnecessary applications to free up memory
- On older machines, detection might take 1-2 seconds

---

For more information, see README.md in the project root.
