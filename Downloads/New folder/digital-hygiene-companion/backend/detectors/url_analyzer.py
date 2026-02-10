"""URL analysis module - identifies suspicious URLs and phishing indicators"""

import re
from urllib.parse import urlparse
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class URLAnalyzer:
    """Analyzes URLs for suspicious characteristics and phishing indicators"""

    def __init__(self):
        self.confidence = 0.0
        self.phishing_confidence = 0.0
        # Common phishing domains/patterns
        self.suspicious_tlds = [".tk", ".ml", ".ga", ".cf"]
        self.suspicious_keywords = [
            "secure", "verify", "confirm", "update", "account",
            "login", "authenticate", "validate", "steam", "apple", "amazon", "paypal"
        ]

    def analyze(self, url: str, context: str = "unknown") -> Dict:
        """
        Analyze URL for suspicious characteristics
        Returns dict with is_suspicious, confidence, and phishing_indicators
        """
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            path = parsed.path.lower()
            
            self.confidence = 0.0
            self.phishing_confidence = 0.0
            phishing_indicators = []

            # Check for missing protocol
            if not parsed.scheme:
                self.confidence += 0.2
                phishing_indicators.append("Missing protocol")

            # Check for suspicious TLD
            for tld in self.suspicious_tlds:
                if domain.endswith(tld):
                    self.confidence += 0.3
                    phishing_indicators.append(f"Suspicious TLD: {tld}")

            # Check for too many subdomains (common in phishing)
            subdomain_count = domain.count(".")
            if subdomain_count > 3:
                self.confidence += 0.15
                phishing_indicators.append("Excessive subdomains")

            # Check for IP address instead of domain
            if re.match(r"^\d+\.\d+\.\d+\.\d+", domain):
                self.confidence += 0.4
                self.phishing_confidence += 0.4
                phishing_indicators.append("Direct IP address used")

            # Check URL length (phishing URLs often very long)
            if len(url) > 100:
                self.confidence += 0.15
                phishing_indicators.append("Unusually long URL")

            # Check for suspicious keywords combined with domain mismatch
            keyword_found = False
            for keyword in self.suspicious_keywords:
                if keyword in path or keyword in domain:
                    keyword_found = True
                    if keyword in ["secure", "verify", "confirm", "login", "authenticate"]:
                        if not any(bank in domain for bank in ["secure.example", "login.official"]):
                            self.phishing_confidence += 0.2
                            phishing_indicators.append(f"Suspicious keyword: {keyword}")

            # Check for homograph attacks (similar looking domains)
            if re.search(r"(0=o|l=1|rn=m)", domain):
                self.confidence += 0.35
                phishing_indicators.append("Potential homograph attack")

            # Check for encoding/obfuscation
            if "%2e" in url or "%3a" in url:
                self.confidence += 0.3
                phishing_indicators.append("URL encoding detected")

            return {
                "is_suspicious": self.confidence > 0.3,
                "confidence": min(1.0, self.confidence),
                "phishing_indicators": phishing_indicators,
                "phishing_confidence": min(1.0, self.phishing_confidence),
                "domain": domain,
                "analysis_details": {
                    "has_protocol": bool(parsed.scheme),
                    "subdomain_count": subdomain_count,
                    "url_length": len(url),
                    "uses_ip": bool(re.match(r"^\d+\.\d+\.\d+\.\d+", domain))
                }
            }
        except Exception as e:
            logger.error(f"Error analyzing URL: {str(e)}")
            return {
                "is_suspicious": True,
                "confidence": 0.2,
                "phishing_indicators": ["Error parsing URL"],
                "phishing_confidence": 0.1,
                "domain": "",
                "analysis_details": {}
            }

    def get_confidence(self) -> float:
        """Get confidence score of last analysis"""
        return self.confidence
