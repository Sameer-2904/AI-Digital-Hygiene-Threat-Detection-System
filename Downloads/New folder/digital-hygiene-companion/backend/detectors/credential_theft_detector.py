"""Credential theft detection module - identifies attempts to steal credentials"""

import re
from typing import List
import logging

logger = logging.getLogger(__name__)


class CredentialTheftDetector:
    """Detects credential theft attempts and account compromise tactics"""

    def __init__(self):
        self.confidence = 0.0
        # Password/credential related patterns
        self.credential_keywords = [
            r"password", r"(?:user)?name", r"pin\s+code", r"security\s+code",
            r"token", r"secret\s+(?:question|answer)", r"date\s+of\s+birth",
            r"(?:social\s+)?security\s+(?:number|code)",
        ]
        self.action_keywords = [
            r"(?:verify|confirm|update|change|reset)\s+(?:password|account|credentials)",
            r"(?:enter|provide|submit|send)\s+(?:password|pin|security\s+code|account\s+details)",
            r"(?:please\s+)?(?:click|confirm|verify)",
        ]

    def detect(self, content: str, content_type: str = "email") -> bool:
        """
        Detect credential theft attempts
        Returns True if credential theft tactic detected
        """
        content_lower = content.lower()
        self.confidence = 0.0

        # Count credential-related keywords
        credentials_mentioned = 0
        for pattern in self.credential_keywords:
            if re.search(pattern, content_lower):
                credentials_mentioned += 1
                self.confidence += 0.12

        # Count action keywords (requests to provide credentials)
        actions_requested = 0
        for pattern in self.action_keywords:
            if re.search(pattern, content_lower):
                actions_requested += 1
                self.confidence += 0.15

        # High alert: requesting password via email/unsolicited
        if content_type in ["email", "message", "sms"]:
            if "password" in content_lower and any(word in content_lower for word in ["send", "provide", "enter", "submit"]):
                self.confidence = min(0.9, self.confidence + 0.3)

        # Links combined with credential requests
        if re.search(r"https?://\S+", content) and credentials_mentioned > 0:
            self.confidence += 0.15

        # Urgency + credential request = very suspicious
        urgency_words = ["urgent", "immediate", "act now", "must", "required"]
        if any(word in content_lower for word in urgency_words) and credentials_mentioned > 0:
            self.confidence = min(0.95, self.confidence + 0.25)

        # Multiple action requests
        if actions_requested >= 2:
            self.confidence = min(0.9, self.confidence + 0.2)

        # Check for "verify your account" patterns
        if re.search(r"verify\s+(?:your|my|account)", content_lower):
            self.confidence = min(0.85, self.confidence + 0.2)

        return self.confidence > 0.5

    def get_confidence(self) -> float:
        """Get the confidence score of the last detection"""
        return min(1.0, self.confidence)
