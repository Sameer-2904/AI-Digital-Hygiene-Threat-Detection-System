# Technology Stack

This document summarizes the core technology stack used by the Digital Hygiene Companion and optional AMD-based hardware/software choices for ML acceleration and deployment.

## Overview
- Backend: Python + FastAPI (ASGI)
- Frontend: React + Vite + Tailwind CSS
- ML/Detectors: rule-based currently; optional ML models (scikit-learn, TensorFlow, PyTorch)

## Languages & Runtimes
- Python 3.x (backend)
- JavaScript (ESM) / React (frontend)
- Node (for frontend tooling / Vite)

## Backend
- Framework: FastAPI
- Server: uvicorn (ASGI)
- Validation: pydantic
- HTTP client / env: requests, python-dotenv
- Location: `backend/` (see `backend/requirements.txt` and `backend/main.py`)

## Frontend
- Framework / bundler: React + Vite (`@vitejs/plugin-react`)
- Styling: Tailwind CSS (PostCSS + autoprefixer)
- HTTP client: axios
- Location: `frontend/` (see `frontend/package.json`)

## ML & Models
- Current: rule-based detectors stored under `backend/detectors/` (fast, local-first)
- Planned / optional: scikit-learn, TensorFlow, or PyTorch models stored in `ml_models/` (see `ml_models/README.md`)
- Recommended model formats: `.joblib`, `.pkl`, `.h5`, `.pth` depending on framework

## AMD Options (Hardware & Software)
The project is designed to run locally; AMD hardware can be used for ML training and accelerated inference. Below are recommended options and considerations.

### Hardware
- AMD GPUs (Instinct family — e.g., MI100/MI200) for high-performance training/inference
- AMD Ryzen / EPYC CPUs for high-throughput CPU inference or data processing

### Software & Drivers
- ROCm: AMD's platform for GPU-accelerated compute (Linux focused). Use ROCm to run PyTorch/TensorFlow builds that target AMD GPUs.
- MIOpen: AMD's deep learning library for performance primitives (used by ROCm-backed frameworks).
- CPU-optimized libraries: AOCL or OpenBLAS / BLIS for faster CPU numerical ops on AMD processors.

Notes on Windows: ROCm primarily targets Linux. On Windows, use a Linux host or WSL2 (with GPU passthrough where supported) for ROCm-based GPU acceleration. Alternatively, run AMD-accelerated workloads in a Linux VM or container on a Linux host.

### Docker / Containers
- Use official ROCm-enabled images for reproducible environments (example base names: `rocm/pytorch` or `rocm/tensorflow`); pick the image matching the ROCm version supported by your GPU/driver.
- Example Docker base (replace `X.Y` with ROCm version):
```
FROM rocm/pytorch:rocmX.Y
```

### Framework integration
- PyTorch (ROCm builds) — preferred for GPU training on AMD; obtain ROCm wheels or use ROCm Docker images
- TensorFlow (ROCm support available via special builds) — check upstream ROCm TF build instructions
- For CPU-only inference on AMD, ensure numeric backends use AOCL/OpenBLAS for best performance

## Dev / Tooling
- Backend package manager: pip (`backend/requirements.txt`)
- Frontend: npm / yarn (see `frontend/package.json`)
- Linting: ESLint referenced in `frontend/package.json`
- Containerization: `Dockerfile`, `docker-compose.yml` available at repo root

## Quick Run (local dev)
```bash
# Backend
python -m pip install -r backend/requirements.txt
python backend/main.py

# Frontend
cd frontend
npm install
npm run dev
```

## AMD-specific notes and recommendations
- If you plan to add GPU-accelerated training or inference, prefer developing on a Linux machine with ROCm-compatible AMD GPUs (Instinct or recent RDNA GPUs where supported).
- Use ROCm Docker images to avoid driver/library mismatches.
- When adding model dependencies, document ROCm version and required wheel names in `ml_models/README.md` or a new `requirements-rocm.txt`.

## Where to add changes
- Documented stack summary: `TECHNOLOGY_STACK.md` (this file)
- ML model artifacts: `ml_models/`
- Backend code: `backend/`
- Frontend code: `frontend/`

---
If you want, I can also add example `Dockerfile` snippets or a `requirements-rocm.txt` with guidance for ROCm-enabled PyTorch/TensorFlow installations.
