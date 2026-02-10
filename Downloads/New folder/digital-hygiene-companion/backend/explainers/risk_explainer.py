"""Risk explanation module - generates simple language explanations of detected risks"""

from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class RiskExplainer:
    """Generates student-friendly explanations of security risks"""

    def __init__(self):
        self.risk_explanations = {
            "Phishing attempt": {
                "simple": "This looks like a fake email trying to trick you into giving away your password or personal information.",
                "why": "Phishing emails pretend to be from banks, social media, or other services to steal your login details.",
                "danger": "If scammers get your password, they can access your accounts and cause serious problems."
            },
            "Social engineering attempt": {
                "simple": "This message is using tricks and manipulation to try to get you to do something you shouldn't.",
                "why": "Scammers create fake urgency or appeal to your emotions to bypass your better judgment.",
                "danger": "You might give away personal info, download malware, or send money without thinking it through."
            },
            "Credential theft attempt": {
                "simple": "Someone is trying to trick you into typing your password or security code on a fake website.",
                "why": "Real companies like banks and social media rarely ask for passwords via email.",
                "danger": "If they get your credentials, they can pretend to be you and access your accounts."
            },
            "Suspicious URL": {
                "simple": "This link looks suspicious and might take you to a fake website.",
                "why": "Scammers create websites that look like real ones to trick you into logging in with your real password.",
                "danger": "Your login info would go directly to the scammers, not the real website."
            },
            "Phishing URL indicators": {
                "simple": "This URL has signs that it might be a phishing link.",
                "why": "The address looks like a real site but has been modified in sneaky ways.",
                "danger": "You might end up on a fake website controlled by scammers."
            },
            "Potential malware source": {
                "simple": "This link might download dangerous software (malware) to your device.",
                "why": "Some websites host malicious programs that can damage your files or steal your data.",
                "danger": "Malware can log your keystrokes, steal passwords, or lock your files for ransom."
            }
        }

        self.risk_level_explanations = {
            "LOW": "This content appears to be safe. No major red flags detected.",
            "MEDIUM": "⚠️ Be cautious with this content. Some warning signs detected.",
            "HIGH": "🚨 This content is likely malicious. Don't click links or provide information.",
            "CRITICAL": "🛑 CRITICAL ALERT: This is almost certainly a phishing or malware attempt. Do NOT interact with it."
        }

    def explain_risks(self, detected_risks: List[str], risk_level: str) -> str:
        """
        Generate a simple, student-friendly explanation of detected risks
        """
        if not detected_risks:
            return self.risk_level_explanations.get(risk_level, "Content analyzed - appears safe.")

        explanation_lines = [self.risk_level_explanations[risk_level], ""]

        for risk in detected_risks:
            if risk in self.risk_explanations:
                exp = self.risk_explanations[risk]
                explanation_lines.append(f"🔍 {risk}")
                explanation_lines.append(f"What it is: {exp['simple']}")
                explanation_lines.append(f"Why: {exp['why']}")
                explanation_lines.append("")

        return "\n".join(explanation_lines)

    def get_recommendations(self, detected_risks: List[str]) -> List[str]:
        """
        Generate specific recommendations based on detected risks
        """
        recommendations = []

        if not detected_risks:
            return [
                "✓ Content appears safe to interact with",
                "Always verify sender addresses before clicking links",
                "If something feels off, trust your instinct"
            ]

        # General recommendations
        recommendations.append("❌ Do NOT click any links in this message")
        recommendations.append("❌ Do NOT provide any personal information")
        recommendations.append("❌ Do NOT download any attachments")

        # Risk-specific recommendations
        if any("phishing" in risk.lower() for risk in detected_risks):
            recommendations.append("✓ Check the sender's email address carefully (not just the display name)")
            recommendations.append("✓ Go directly to the official website instead of clicking links")
            recommendations.append("✓ Report this email to your email provider")

        if any("url" in risk.lower() or "malware" in risk.lower() for risk in detected_risks):
            recommendations.append("✓ Hover over the link to see the real URL (don't click it)")
            recommendations.append("✓ Use a legitimate URL checker if you're curious about the link")

        if any("credential" in risk.lower() for risk in detected_risks):
            recommendations.append("✓ Legitimate services never ask for passwords via email")
            recommendations.append("✓ Always log in by typing the official website address yourself")

        if any("social engineering" in risk.lower() for risk in detected_risks):
            recommendations.append("✓ Take time to think - real emergencies rarely happen via email")
            recommendations.append("✓ Contact the organization directly using a number you know is real")

        # Final recommendations
        recommendations.append("")
        recommendations.append("📚 Learn more about staying safe online at your school's digital safety resources")
        recommendations.append("⚠️ If you've already clicked on something suspicious, tell a trusted adult or your IT support")

        return recommendations

    def explain_structured(self, detected_risks: List[str], risk_level: str) -> Dict[str, object]:
        """
        Return a structured explanation suitable for UI: summary, up to 3 plain-language reasons, and next steps.
        """
        if not detected_risks:
            return {
                "summary": self.risk_level_explanations.get(risk_level, "Content analyzed - appears safe."),
                "reasons": ["No major indicators of phishing, malware, or fraud detected."],
                "next_steps": [
                    "This content appears safe to interact with.",
                    "Always verify sender addresses before clicking links.",
                    "If something feels off, trust your instinct and ask for help."
                ]
            }

        reasons = []
        for risk in detected_risks:
            if risk in self.risk_explanations:
                exp = self.risk_explanations[risk]
                reasons.append(exp['simple'])

        # Limit reasons to 3 and make them plain-language bullets
        reasons = reasons[:3]

        # Compose next steps (short, actionable)
        next_steps = []
        if any('phishing' in r.lower() or 'credential' in r.lower() for r in detected_risks):
            next_steps.extend([
                "Do not click any links or enter credentials.",
                "Go to the official website by typing its address yourself.",
                "Report the message to your school's IT or email provider."
            ])

        if any('malware' in r.lower() or 'suspicious url' in r.lower() for r in detected_risks):
            next_steps.extend([
                "Do not download files from this source.",
                "Run an updated antivirus scan if you interacted with it.",
                "If in doubt, ask IT support before opening attachments." 
            ])

        if any('social engineering' in r.lower() for r in detected_risks):
            next_steps.extend([
                "Pause and verify the request with a known contact method.",
                "Do not act under pressure or urgency without confirmation.",
            ])

        # Fallback general tips
        if not next_steps:
            next_steps = [
                "Do not click suspicious links.",
                "Verify sender identity before sharing personal info.",
                "When unsure, ask your IT support or a trusted person."
            ]

        # Keep just 3 next steps
        next_steps = next_steps[:3]

        return {
            "summary": self.risk_level_explanations.get(risk_level, "Potential risk detected."),
            "reasons": reasons,
            "next_steps": next_steps
        }
