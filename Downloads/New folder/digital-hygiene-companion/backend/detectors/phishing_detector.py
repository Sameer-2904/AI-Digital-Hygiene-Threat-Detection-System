"""Phishing detection module - identifies phishing attempts in text content"""

import re
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class PhishingDetector:
    """Detects phishing attempts using pattern matching and linguistic analysis"""

    def __init__(self):
        self.confidence = 0.0
        # Common phishing keywords and patterns
        self.phishing_keywords = [
            r"verify\s+(?:your|my|account|identity|password)",
            r"(?:urgent|immediate|action\s+required|act\s+now)",
            r"(?:confirm|validate|update)\s+(?:password|account|information)",
            r"suspended|locked|disabled|limited|restricted",
            r"unusual\s+activity",
            r"(?:click\s+here|confirm\s+identity|verify\s+account)",
            r"bank|paypal|amazon|apple|microsoft",
        ]
        #Social engineering keywords
        self.social_engineering_keywords = [
            r"trust\s+me",
            r"(?:private|confidential)\s+information",
            r"(?:only\s+you|just\s+between\s+us)",
        ]

    def detect(self, content: str) -> bool:
        """
        Detect if content contains phishing indicators
        Returns True if phishing detected
        """
        content_lower = content.lower()
        self.confidence = 0.0

        # Check for phishing keywords
        matched_keywords = 0
        for pattern in self.phishing_keywords:
            if re.search(pattern, content_lower, re.IGNORECASE):
                matched_keywords += 1

        # Check for urgency indicators combined with action requests
        has_urgency = bool(re.search(r"urgent|immediate|act\s+now", content_lower))
        has_action = bool(re.search(r"click|confirm|verify|update", content_lower))

        # Check for suspicious sender attempts or email spoofing patterns
        has_spoofing_indicators = bool(
            re.search(r"(?:from|on\s+behalf\s+of)\s+\w+@\w+", content_lower)
        )

        # Calculate confidence score
        if matched_keywords >= 2:
            self.confidence = min(0.9, 0.3 + (matched_keywords * 0.15))

        if has_urgency and has_action:
            self.confidence = max(self.confidence, 0.7)

        if has_spoofing_indicators and self.confidence > 0.3:
            self.confidence = min(0.95, self.confidence + 0.2)

        return self.confidence > 0.5

    def get_confidence(self) -> float:
        """Get the confidence score of the last detection"""
        return min(1.0, self.confidence)
