# Architecture & Judge Summary

## Text-based architecture diagram

Client (Browser React + Vite)
  - UI components: Text Analyzer, Link Checker, QR/Link input
  - Consent prompt & client-side SHA-256 hashing (anonymization token)
  - Sends requests to backend `/api/analyze/*` endpoints

Backend (FastAPI + Uvicorn)
  - Endpoints: `/api/analyze/text`, `/api/analyze/url`, `/api/analyze/qr`, `/api/analyze/combined`
  - Detectors (rule-based heuristics): `backend/detectors/*`
  - Explainability: `backend/explainers/risk_explainer.py` produces summary, 3 reasons, and next steps
  - Privacy: server computes hash of inputs, stores only aggregated anonymous counters per label; no raw content persisted

ML/Models (Planned)
  - Optional scikit-learn / PyTorch models in `ml_models/` for improved detection
  - ROCm / AMD options documented in `TECHNOLOGY_STACK.md` for hardware acceleration

Data flow (simple):
  1. User consents in UI
  2. Client computes hashed token and sends content + `consent: true` to backend
  3. Backend runs detectors, scores risk, produces structured explanation
  4. Backend increments anonymous aggregate counters only
  5. UI renders score, label, up to 3 reasons, and 3 actionable next steps

## How this solves the brief (judge-friendly)
- Problem: Students and staff face phishing, malicious links, and social engineering.
- Approach: Local-first, explainable detectors detect risks across email, chat, URL, and QR links.
- Privacy: Explicit consent, client-side hashed tokens, and no raw-data persistence. Only aggregate counts stored.
- Explainability: All outputs include a simple summary, up to three plain-language reasons, and three next actions — ideal for judges seeking clarity and safety.
- Hackathon scope: Rule-based detectors for immediate accuracy and transparency; ML models are optional future improvements.

## Future scope & scalability (brief)
- Add lightweight on-device ML models for improved detection and retraining pipeline
- Add ROCm-enabled container images for AMD GPU training and inference
- Add telemetry toggle and secure opt-in telemetry for aggregated model improvement

---
Ready for the live demo; say if you want slides or a one-page judge PDF.
