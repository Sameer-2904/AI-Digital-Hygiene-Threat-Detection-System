# Digital Hygiene Companion

An AI-powered digital safety companion designed specifically for students that detects phishing, suspicious URLs, social engineering, credential theft, and malware with a privacy-first architecture.

## 🎯 Key Features

- **🔍 Multi-threat Detection**
  - Phishing email detection
  - Suspicious URL analysis
  - Social engineering tactic identification
  - Credential theft attempt detection
  - Malware indicator recognition

- **📚 Student-Friendly Explanations**
  - Simple, non-technical explanations of why something is suspicious
  - Clear recommendations on what to do
  - Educational insights about online safety

- **🔒 Privacy by Design**
  - **ALL processing happens locally** - nothing is sent to external servers
  - No login required
  - No data collection or storage
  - Completely anonymous analysis

- **🌍 Multi-Platform Support**
  - Works on Windows, macOS, Linux
  - Web-based for easy access
  - Can work offline (with some features)

## 🏗️ Architecture

```
digital-hygiene-companion/
├── backend/                    # Python FastAPI server
│   ├── main.py               # Main API endpoints
│   ├── detectors/            # Detection modules
│   │   ├── phishing_detector.py
│   │   ├── url_analyzer.py
│   │   ├── social_engineering_detector.py
│   │   ├── credential_theft_detector.py
│   │   └── malware_detector.py
│   ├── explainers/           # Risk explanation modules
│   │   └── risk_explainer.py
│   └── requirements.txt       # Python dependencies
│
├── frontend/                   # React web application
│   ├── src/
│   │   ├── components/
│   │   │   ├── TextAnalyzer.jsx
│   │   │   ├── URLAnalyzer.jsx
│   │   │   └── RiskResult.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── ml_models/                  # Trained ML models (optional)
│   └── README.md
│
└── README.md
```

## 📋 System Requirements

- **Backend**: Python 3.8+
- **Frontend**: Node.js 16+ and npm/yarn
- **Browser**: Modern browser (Chrome, Firefox, Safari, Edge)
- **Memory**: Minimal (MB-level per analysis)
- **Internet**: Not required for core functionality

## 🚀 Getting Started

### 1. Clone or Download the Project

```bash
cd digital-hygiene-companion
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python main.py
```

The backend API will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 📖 Usage

### Analyzing Text Content
1. Click on "📧 Email & Messages" tab
2. Select the content type (Email, Chat, SMS, Social Post)
3. Paste the text you want to analyze
4. Click "Analyze Text"
5. Review the risk level and recommendations

### Analyzing URLs
1. Click on "🔗 Links" tab
2. Paste the URL you want to check (don't click it!)
3. Select where you found the link
4. Click "Check Link"
5. Review the analysis and recommendations

## 🔬 How It Works

### Detection Methods

Each detector uses pattern matching and heuristics designed to identify known phishing and security threats:

- **Phishing Detector**: Looks for urgent language, credential requests, and spoofing indicators
- **URL Analyzer**: Examines domain structure, encoding, homograph attacks, and suspicious patterns
- **Social Engineering Detector**: Identifies manipulation tactics like urgency, authority appeals, and fear tactics
- **Credential Theft Detector**: Detects requests for passwords, PINs, and sensitive information
- **Malware Detector**: Flags suspicious file extensions, URL patterns, and malware indicators

### Risk Levels

- **🟢 LOW**: Content appears safe
- **🟡 MEDIUM**: Some warning signs detected
- **🟠 HIGH**: Likely malicious - don't interact
- **🔴 CRITICAL**: Almost certainly phishing/malware - avoid completely

## 🔐 Privacy & Security

### What We Don't Do
- ❌ Send your data to external servers
- ❌ Store any information you analyze
- ❌ Require login or accounts
- ❌ Use cookies or tracking
- ❌ Access files on your system

### What We Do
- ✅ Process everything locally on your device
- ✅ Use open-source, transparent code
- ✅ Provide clear explanations of our analysis
- ✅ Keep you in control of your data

## 🛠️ Development

### Adding New Detectors

Create a new file in `backend/detectors/`:

```python
class NewDetector:
    def __init__(self):
        self.confidence = 0.0
    
    def detect(self, content: str) -> bool:
        # Your detection logic here
        self.confidence = 0.5
        return self.confidence > 0.5
    
    def get_confidence(self) -> float:
        return min(1.0, self.confidence)
```

Then add it to `backend/main.py`.

### Improving Detection

The detection modules use pattern matching and heuristics. To improve detection:

1. Add new patterns to the keyword lists
2. Refine confidence scoring
3. Combine multiple indicators for better accuracy
4. Test with real phishing examples

## 📚 Learning Resources

- [NIST Cybersecurity Guide](https://www.nist.gov/)
- [FBI Phishing Alerts](https://www.fbi.gov/investigate/cyber)
- [Google Safe Browsing](https://safebrowsing.google.com/)
- [CISA Cyber Awareness](https://www.cisa.gov/)

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Better phishing detection algorithms
- Machine learning model integration
- More language support
- Additional threat detection types
- Improved UI/UX
- Mobile app versions

## 📄 License

This project is provided as-is for educational and personal use.

## ⚠️ Disclaimer

This tool is designed to help identify suspicious content, but it's not 100% accurate. Always:
- Use your judgment
- Be skeptical of unsolicited messages
- Report suspicious activities to your IT support
- Keep your passwords secure
- Never click links in suspicious emails

## 🆘 Support

If you encounter issues or have questions:
1. Check the error message in the console
2. Ensure backend is running on port 8000
3. Ensure frontend is running on port 3000
4. Check that both services can communicate

## 🎓 Educational Value

This project teaches:
- Web application security
- API design and development
- Frontend-backend integration
- Pattern matching and heuristics
- Risk assessment and communication
- Privacy-preserving design

---

**Made for students, by security-conscious developers** 🛡️
