"""Social engineering detection module - identifies manipulation and social engineering tactics"""

import re
from typing import List
import logging

logger = logging.getLogger(__name__)


class SocialEngineeringDetector:
    """Detects social engineering attacks and manipulation tactics"""

    def __init__(self):
        self.confidence = 0.0
        # Social engineering tactics
        self.pressure_tactics = [
            r"(?:act\s+now|urgent|immediately|limited\s+time|expire|deadline)",
            r"(?:last\s+chance|don't?(?:\s+|\W)miss|only\s+today)",
        ]
        self.authority_tactics = [
            r"(?:from|behalf\s+of)\s+(?:your\s+)?(?:bank|paypal|apple|microsoft|admin|it)",
            r"(?:official|authorized|verified)\s+(?:account|representative)",
        ]
        self.trust_building = [
            r"don't\s+(?:worry|be\s+concerned)",
            r"trust\s+(?:me|us|this)",
            r"(?:safe|secure|confidential|private)",
        ]
        self.fear_tactics = [
            r"(?:account|access|funds|data)\s+(?:suspended|locked|disabled|compromised)",
            r"(?:risky|dangerous|problem|attack)",
            r"(?:unusual|suspicious)\s+activity",
        ]
        self.reward_tactics = [
            r"(?:claim|receive|get|won?)\s+(?:prize|reward|refund|money|gift)",
            r"(?:exclusive|special)\s+(?:offer|deal|opportunity)",
        ]

    def detect(self, content: str) -> bool:
        """
        Detect social engineering tactics in content
        Returns True if manipulation detected
        """
        content_lower = content.lower()
        self.confidence = 0.0
        tactics_found = 0

        # Check for pressure tactics
        for pattern in self.pressure_tactics:
            if re.search(pattern, content_lower):
                tactics_found += 1
                self.confidence += 0.15

        # Check for authority appeals
        for pattern in self.authority_tactics:
            if re.search(pattern, content_lower):
                tactics_found += 1
                self.confidence += 0.18

        # Check for trust building (especially combined with requests)
        trust_keywords_count = sum(1 for pattern in self.trust_building
                                  if re.search(pattern, content_lower))
        if trust_keywords_count > 0:
            if any(word in content_lower for word in ["click", "confirm", "verify", "send", "provide"]):
                tactics_found += 1
                self.confidence += 0.2

        # Check for fear/scarcity tactics
        for pattern in self.fear_tactics:
            if re.search(pattern, content_lower):
                tactics_found += 1
                self.confidence += 0.15

        # Check for reward/incentive tactics
        for pattern in self.reward_tactics:
            if re.search(pattern, content_lower):
                tactics_found += 1
                self.confidence += 0.12

        # Multiple tactics combined = higher confidence
        if tactics_found >= 2:
            self.confidence = min(0.9, self.confidence * 1.2)

        # Check for personalization (attempts to seem genuine)
        if any(word in content_lower for word in ["dear", "valued", "dear customer", "friend"]):
            if tactics_found >= 1:
                self.confidence += 0.1

        return self.confidence > 0.5

    def get_confidence(self) -> float:
        """Get the confidence score of the last detection"""
        return min(1.0, self.confidence)
