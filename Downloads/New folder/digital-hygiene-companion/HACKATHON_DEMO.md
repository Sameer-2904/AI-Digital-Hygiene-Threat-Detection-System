# Hackathon Demo: AI Digital Hygiene & Threat Detection System

Quick checklist to run the MVP locally and demo cases for judges.

## Run locally

Backend (from repo root):
```bash
python -m pip install -r backend/requirements.txt
python backend/main.py
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` to view the UI.

## Demo Script (3–5 minutes)
1. Landing: Introduce the problem and privacy-first design.
2. Show consent: point out the consent prompt before analysis.
3. Demo cases (below): run each case and explain the output, reasons (max 3), and next steps.
4. Show QR flow: paste a QR-extracted URL into the Link Checker.
5. Show how only aggregated stats are kept (no raw inputs) and mention hashing.

## Demo Test Cases

- Safe Email (Expected: SAFE)
  - Content: "Welcome to campus! Your course schedule is available at https://university.edu/portal"

- Suspicious Link (Expected: SUSPICIOUS)
  - Content: "Your account needs verification: http://university-login.example.com/login"

- Phishing Email (Expected: UNSAFE)
  - Content: "URGENT: Your account will be locked. Click https://secure-univ.example.com and enter credentials now."

- Malware Link (Expected: UNSAFE)
  - Link: "http://malware-download.example.com/file.exe"

- Chat Scam (Expected: SUSPICIOUS/UNSAFE)
  - Content: "Hey, can you pay this invoice? Send $200 to 0xABC... I'll pay you back ASAP."

- QR Link (Expected: depends on URL)
  - Paste the URL extracted from a QR code into the Link Safety Checker.

## What judges should look for
- Clear risk score (0–100) and label (SAFE / SUSPICIOUS / UNSAFE)
- Human-friendly reasons (≤3 bullets) and concise next steps
- Consent flow and local-first privacy design
- Clean UI and easy-to-follow demo steps

---
If you'd like, I can prepare a short slide or one-page README summarizing the architecture for judges.
