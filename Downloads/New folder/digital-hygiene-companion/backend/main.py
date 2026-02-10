"""
Digital Hygiene Companion - FastAPI Backend
AI-powered detector for phishing, suspicious URLs, social engineering, credential theft, and malware
with local-first privacy architecture
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import hashlib
from fastapi import Header

from auth import validate_api_key, check_rate_limit
from detectors.phishing_detector import PhishingDetector
from detectors.url_analyzer import URLAnalyzer
from detectors.social_engineering_detector import SocialEngineeringDetector
from detectors.credential_theft_detector import CredentialTheftDetector
from detectors.malware_detector import MalwareDetector
from explainers.risk_explainer import RiskExplainer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Digital Hygiene Companion API",
    description="AI-powered security detector for students with privacy-first design",
    version="1.0.0"
)

# Add CORS middleware for multi-platform support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize detectors (all run locally)
phishing_detector = PhishingDetector()
url_analyzer = URLAnalyzer()
social_engineering_detector = SocialEngineeringDetector()
credential_theft_detector = CredentialTheftDetector()
malware_detector = MalwareDetector()
risk_explainer = RiskExplainer()

# In-memory aggregated anonymous stats (counts per safety label)
aggregated_stats: Dict[str, int] = {"SAFE": 0, "SUSPICIOUS": 0, "UNSAFE": 0}


def hash_input(value: str) -> str:
    """Returns SHA-256 hex digest of the input (used for anonymization)."""
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def map_confidence_to_score_and_label(confidence: float) -> (int, str):
    """Map 0.0-1.0 confidence to 0-100 score and safety label.
    Thresholds: 0-30 SAFE, 31-70 SUSPICIOUS, 71-100 UNSAFE
    """
    score = int(round(confidence * 100))
    if score <= 30:
        label = "SAFE"
    elif score <= 70:
        label = "SUSPICIOUS"
    else:
        label = "UNSAFE"
    return score, label


class TextAnalysisRequest(BaseModel):
    """Request model for analyzing text content"""
    content: str
    content_type: str = "email"  # email, message, post, etc.


class URLAnalysisRequest(BaseModel):
    """Request model for analyzing URLs"""
    url: str
    context: str = "unknown"  # email, chat, web, etc.


class RiskAnalysisResponse(BaseModel):
    """Response model with risk detection results"""
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    confidence: float  # 0.0 to 1.0
    risk_score: int  # 0-100
    safety_label: str  # SAFE, SUSPICIOUS, UNSAFE
    detected_risks: List[str]  # List of identified risks
    explanation: str  # Simple language explanation (summary + reasons)
    recommendations: List[str]  # What the user should do


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "digital-hygiene-companion"}


@app.post("/api/analyze/text", response_model=RiskAnalysisResponse)
async def analyze_text(
    request: TextAnalysisRequest,
    authorization: Optional[str] = Header(None),
    api_key: Optional[str] = Header(None)
):
    """
    Analyze text content for phishing, social engineering, and credential theft risks.
    All processing happens locally on this device.
    Optional: Include 'Authorization: Bearer <api_key>' or 'api-key: <key>' header for authentication.
    """
    try:
        # Validate API key (optional if not configured)
        key = validate_api_key(authorization, api_key)
        # Check rate limit
        check_rate_limit(key)

        detected_risks = []
        risk_scores = {}

        # Run all detectors
        if phishing_detector.detect(request.content):
            detected_risks.append("Phishing attempt")
            risk_scores["phishing"] = phishing_detector.get_confidence()

        if social_engineering_detector.detect(request.content):
            detected_risks.append("Social engineering attempt")
            risk_scores["social_engineering"] = social_engineering_detector.get_confidence()

        if credential_theft_detector.detect(request.content, request.content_type):
            detected_risks.append("Credential theft attempt")
            risk_scores["credential_theft"] = credential_theft_detector.get_confidence()

        # Calculate overall risk
        if not detected_risks:
            risk_level = "LOW"
            avg_confidence = 0.0
        else:
            avg_confidence = sum(risk_scores.values()) / len(risk_scores) if risk_scores else 0
            if avg_confidence > 0.7:
                risk_level = "CRITICAL"
            elif avg_confidence > 0.5:
                risk_level = "HIGH"
            elif avg_confidence > 0.3:
                risk_level = "MEDIUM"
            else:
                risk_level = "LOW"

        # Generate explanation and recommendations
        # Structured explanation (summary, reasons, next steps)
        structured = risk_explainer.explain_structured(detected_risks, risk_level)
        explanation_text = structured['summary'] + "\n\nReasons:\n- " + "\n- ".join(structured['reasons'])
        recommendations = structured['next_steps']

        # Map to 0-100 and safety label
        risk_score, safety_label = map_confidence_to_score_and_label(avg_confidence)

        # Anonymize input and only store aggregated stats (no raw inputs saved)
        try:
            hashed = hash_input(request.content)
            aggregated_stats[safety_label] = aggregated_stats.get(safety_label, 0) + 1
        except Exception:
            # In case hashing fails, avoid storing raw content — skip aggregation
            pass

        return RiskAnalysisResponse(
            risk_level=risk_level,
            confidence=avg_confidence,
            risk_score=risk_score,
            safety_label=safety_label,
            detected_risks=detected_risks,
            explanation=explanation_text,
            recommendations=recommendations
        )

    except Exception as e:
        logger.error(f"Error analyzing text: {str(e)}")
        raise HTTPException(status_code=500, detail="Analysis failed")


@app.post("/api/analyze/url", response_model=RiskAnalysisResponse)
async def analyze_url(
    request: URLAnalysisRequest,
    authorization: Optional[str] = Header(None),
    api_key: Optional[str] = Header(None)
):
    """
    Analyze URL for suspicious characteristics, phishing, and malware indicators.
    All processing happens locally on this device.
    Optional: Include 'Authorization: Bearer <api_key>' or 'api-key: <key>' header for authentication.
    """
    try:
        # Validate API key (optional if not configured)
        key = validate_api_key(authorization, api_key)
        # Check rate limit
        check_rate_limit(key)

        detected_risks = []
        risk_scores = {}

        # Analyze URL
        url_analysis = url_analyzer.analyze(request.url, request.context)

        if url_analysis["is_suspicious"]:
            detected_risks.append("Suspicious URL")
            risk_scores["url_suspicious"] = url_analysis["confidence"]

        if url_analysis["phishing_indicators"]:
            detected_risks.append("Phishing URL indicators")
            risk_scores["url_phishing"] = url_analysis["phishing_confidence"]

        if malware_detector.check_url_reputation(request.url):
            detected_risks.append("Potential malware source")
            risk_scores["malware"] = malware_detector.get_confidence()

        # Calculate overall risk
        if not detected_risks:
            risk_level = "LOW"
            avg_confidence = 0.0
        else:
            avg_confidence = sum(risk_scores.values()) / len(risk_scores) if risk_scores else 0
            if avg_confidence > 0.7:
                risk_level = "CRITICAL"
            elif avg_confidence > 0.5:
                risk_level = "HIGH"
            elif avg_confidence > 0.3:
                risk_level = "MEDIUM"
            else:
                risk_level = "LOW"

        # Generate explanation and recommendations
        structured = risk_explainer.explain_structured(detected_risks, risk_level)
        explanation_text = structured['summary'] + "\n\nReasons:\n- " + "\n- ".join(structured['reasons'])
        recommendations = structured['next_steps']

        # Map to 0-100 and safety label
        risk_score, safety_label = map_confidence_to_score_and_label(avg_confidence)

        # Anonymize input and only store aggregated stats (no raw inputs saved)
        try:
            hashed = hash_input(request.url)
            aggregated_stats[safety_label] = aggregated_stats.get(safety_label, 0) + 1
        except Exception:
            pass

        return RiskAnalysisResponse(
            risk_level=risk_level,
            confidence=avg_confidence,
            risk_score=risk_score,
            safety_label=safety_label,
            detected_risks=detected_risks,
            explanation=explanation_text,
            recommendations=recommendations
        )

    except Exception as e:
        logger.error(f"Error analyzing URL: {str(e)}")
        raise HTTPException(status_code=500, detail="Analysis failed")


@app.post("/api/analyze/combined")
async def analyze_combined(text_request: TextAnalysisRequest, url_request: URLAnalysisRequest = None):
    """
    Combined analysis of text and optional URL.
    Useful for analyzing emails with links, messages with URLs, etc.
    """
    try:
        text_result = await analyze_text(text_request)
        
        results = {"text_analysis": text_result}
        
        if url_request:
            url_result = await analyze_url(url_request)
            results["url_analysis"] = url_result
            
            # Combine results if both have risks
            if text_result.detected_risks or url_result.detected_risks:
                combined_risks = list(set(text_result.detected_risks + url_result.detected_risks))
                combined_confidence = max(text_result.confidence, url_result.confidence)
                combined_risk_level = max([text_result.risk_level, url_result.risk_level],
                                        key=lambda x: {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}[x])
                
                results["combined"] = {
                    "risk_level": combined_risk_level,
                    "confidence": combined_confidence,
                    "detected_risks": combined_risks
                }
        
        return results

    except Exception as e:
        logger.error(f"Error in combined analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Analysis failed")


@app.post("/api/analyze/qr", response_model=RiskAnalysisResponse)
async def analyze_qr(
    payload: Dict[str, Any],
    authorization: Optional[str] = Header(None),
    api_key: Optional[str] = Header(None)
):
    """
    Analyze QR content. Expects JSON: { "qr_data": "<text or url>", "context": "email|chat|web|unknown" }
    For this MVP we accept the QR data as text (often a URL) and analyze the contained link.
    Optional: Include 'Authorization: Bearer <api_key>' or 'api-key: <key>' header for authentication.
    """
    try:
        # Validate API key (optional if not configured)
        key = validate_api_key(authorization, api_key)
        # Check rate limit
        check_rate_limit(key)

        qr_data = payload.get("qr_data") if isinstance(payload, dict) else None
        context = payload.get("context", "unknown") if isinstance(payload, dict) else "unknown"

        if not qr_data:
            raise HTTPException(status_code=400, detail="Missing qr_data in payload")

        # If qr_data looks like a URL, forward to URL analyzer
        if isinstance(qr_data, str) and qr_data.startswith("http"):
            url_req = URLAnalysisRequest(url=qr_data, context=context)
            return await analyze_url(url_req)

        # Otherwise, we don't attempt image decoding server-side in this MVP
        raise HTTPException(status_code=400, detail="qr_data must contain a URL for this demo")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing QR data: {str(e)}")
        raise HTTPException(status_code=500, detail="QR analysis failed")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
