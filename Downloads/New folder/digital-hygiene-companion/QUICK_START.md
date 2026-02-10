# 🚀 Digital Hygiene Companion - Quick Start Guide

**Status**: ✅ **READY TO RUN** - All dependencies installed and tested!

## 📋 What's Been Set Up

- ✅ **Backend**: Python 3.14 with FastAPI 0.104.1
- ✅ **Frontend**: React with Vite 5.4.21
- ✅ **Build**: Frontend builds successfully
- ✅ **Dev Server**: Tested and working

---

## 🎯 Launch Instructions

### **STEP 1: Start Backend (Terminal 1)**

```powershell
cd "c:\Users\pc\Downloads\New folder\digital-hygiene-companion\backend"
venv\Scripts\activate
python main.py
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ Backend API will be available at: **http://localhost:8000**

---

### **STEP 2: Start Frontend (Terminal 2)**

```powershell
cd "c:\Users\pc\Downloads\New folder\digital-hygiene-companion\frontend"
npm run dev
```

**Expected Output:**
```
VITE v5.4.21 ready in xxx ms
➜ Local: http://localhost:3000/
```

✅ Frontend will be available at: **http://localhost:3000**

---

### **STEP 3: Open in Browser**

Open your browser and go to:
```
http://localhost:3000
```

---

## 🧪 Testing the Application

### Test 1: Analyze a Phishing Email (Simple)

1. Click "📧 Email & Messages" tab
2. Select content type: **Email**
3. Paste this text:
```
Dear Customer,
Your account has been suspended! Click here immediately to verify your account and restore access to your account now.
Urgent action required!
Visit: secure-verify-account.tk/confirm
```
4. Click "Analyze Text"
5. **Expected Result**: HIGH or CRITICAL risk detected with phishing indicators

### Test 2: Check a Suspicious URL

1. Click "🔗 Links" tab
2. Paste this URL: `http://paypal-secure.tk/verify-account`
3. Select context: **Email**
4. Click "Check Link"
5. **Expected Result**: HIGH risk with suspicious domain indicators

### Test 3: Legitimate Email (Should be LOW risk)

1. Click "📧 Email & Messages" tab
2. Paste:
```
Hi John,
Here's the project report you requested.
Best regards,
Sarah
```
3. Click "Analyze Text"
4. **Expected Result**: LOW risk - appears safe

---

## 📡 API Testing (Optional)

Test the backend API directly:

```powershell
# Check health
curl http://localhost:8000/health

# Test text analysis
curl -X POST http://localhost:8000/api/analyze/text `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"content":"Verify your account now!","content_type":"email"}'

# Test URL analysis
curl -X POST http://localhost:8000/api/analyze/url `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"url":"http://fake-bank.tk/login","context":"email"}'
```

Or use the built-in API docs at: **http://localhost:8000/docs**

---

## 🛠️ Troubleshooting

### Backend won't start
- **Check**: Is Python 3.14 installed?
- **Check**: Is the venv activated? (should show `(venv)` in terminal)
- **Fix**: Reinstall backend: `pip install -r requirements.txt`

### Frontend shows blank page
- **Check**: Is backend running on port 8000?
- **Check**: Browser console for errors (F12)
- **Fix**: Restart frontend dev server with `npm run dev`

### Port already in use
```powershell
# Find process using port 3000 (frontend)
netstat -ano | findstr :3000

# Find process using port 8000 (backend)
netstat -ano | findstr :8000

# Kill process by PID
taskkill /PID <PID> /F
```

### Module/Package errors
```powershell
# Backend errors
cd backend
venv\Scripts\python.exe -m pip install --upgrade -r requirements.txt

# Frontend errors
cd frontend
npm install --force
npm cache clean --force
```

---

## 📚 Features to Try

✨ **Email Analyzer**
- Detects phishing attempts
- Identifies social engineering tactics
- Warns about credential theft attempts
- Explains risks in simple language

🔗 **Link Checker**
- Analyzes URLs for suspicious characteristics
- Identifies homograph attacks
- Checks for malware indicators
- Safe to use - doesn't click links

📖 **Educational Content**
- Quick safety tips
- Learn about online threats
- Best practices for staying safe

---

## 📖 Full Documentation

- **README.md** - Complete project overview
- **SETUP.md** - Detailed setup and configuration
- **SAFETY_GUIDE.md** - Usage examples and safety tips
- **ARCHITECTURE.md** - Technical architecture details

---

## ✅ Verification Checklist

Before reporting issues, verify:

- [ ] Python version is 3.10+: `python --version`
- [ ] Node.js version is 16+: `node --version`
- [ ] Backend venv activated: `(venv)` shows in terminal
- [ ] Backend dependencies installed: Run `python main.py` in backend folder
- [ ] Frontend dependencies: `node_modules` folder exists
- [ ] Ports 3000 and 8000 are available
- [ ] No errors in browser console (F12)

---

## 🎓 Learning Resources

- [NIST Cybersecurity](https://www.nist.gov/)
- [FBI Cyber Division](https://www.fbi.gov/investigate/cyber)
- [Google Safe Browsing](https://safebrowsing.google.com/)
- [CISA Awareness](https://www.cisa.gov/)

---

## 🎉 You're All Set!

**Both backend and frontend are tested and ready!**

1. Start backend: Run `python main.py` in backend folder
2. Start frontend: Run `npm run dev` in frontend folder
3. Open: http://localhost:3000
4. Start analyzing! 🛡️

---

**Need Help?**
- Check the error message in the terminal
- Review the relevant markdown file in the project root
- Verify all requirements are met

**Ready to launch? Go back to your terminal and start both services!** 🚀
