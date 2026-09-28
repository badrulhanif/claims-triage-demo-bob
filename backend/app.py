"""
app.py — Insurance Claims Triage Assistant
Flask backend with a keyword-based mock LLM analyser.
"""

import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from prompt_template import build_prompt

app = Flask(__name__)
CORS(app)

# ---------------------------------------------------------------------------
# Keyword lists for mock triage logic
# ---------------------------------------------------------------------------

FRAUD_KEYWORDS = [
    "third claim",
    "no witness",
    "no witnesses",
    "luxury",
    "inconsistent",
    "disputes",
    "dispute",
    "jewellery",
    "jewelry",
    "prior claim",
    "multiple claims",
    "uncooperative",
    "no police report",
    "forced entry",
]

URGENT_KEYWORDS = [
    "hospital",
    "hospitalised",
    "hospitalized",
    "injury",
    "injuries",
    "emergency",
    "spinal",
    "intensive care",
    "life-threatening",
    "fatality",
    "fatal",
    "surgery",
    "ambulance",
    "medical bills",
    "settlement advance",
]

FRAUD_INDICATOR_MAP = {
    "third claim":    "Multiple claims filed within a short period — possible pattern of abuse.",
    "no witness":     "No independent witnesses to corroborate the claimant's account.",
    "no witnesses":   "No independent witnesses to corroborate the claimant's account.",
    "luxury":         "High-value luxury items claimed without adequate proof of ownership.",
    "inconsistent":   "Inconsistencies detected between the claimant's statement and submitted evidence.",
    "disputes":       "A third party disputes the claimant's version of events.",
    "dispute":        "A third party disputes the claimant's version of events.",
    "jewellery":      "High-value jewellery claimed — requires independent valuation and proof of ownership.",
    "jewelry":        "High-value jewelry claimed — requires independent valuation and proof of ownership.",
    "prior claim":    "Prior claims history warrants additional scrutiny.",
    "multiple claims":"Multiple claims on record — potential indicator of abuse.",
    "uncooperative":  "Claimant has been uncooperative during follow-up — raises concern.",
    "no police report":"No police report filed despite the nature of the alleged incident.",
    "forced entry":   "No signs of forced entry detected — inconsistent with reported break-in.",
}


def _hits(text: str, keywords: list) -> list:
    text_lower = text.lower()
    return [kw for kw in keywords if re.search(r"\b" + re.escape(kw) + r"\b", text_lower)]


def _build_fraud_indicators(hits: list) -> list:
    seen, result = set(), []
    for hit in hits:
        label = FRAUD_INDICATOR_MAP.get(hit, f"Suspicious keyword detected: '{hit}'.")
        if label not in seen:
            seen.add(label)
            result.append(label)
    return result


def mock_triage(claim_text: str) -> dict:
    """Keyword-based triage — simulates LLM output for the prototype."""
    fraud_hits = _hits(claim_text, FRAUD_KEYWORDS)
    urgent_hits = _hits(claim_text, URGENT_KEYWORDS)

    if fraud_hits:
        return {
            "priority_level": "CRITICAL",
            "fraud_indicators": _build_fraud_indicators(fraud_hits),
            "recommended_actions": [
                "Place claim on hold pending a formal fraud investigation.",
                "Flag the case in the fraud management system immediately.",
                "Request original receipts and independent valuations for all claimed items.",
                "Obtain a signed statutory declaration from the claimant.",
                "Cross-reference full claims history for patterns.",
                "Schedule an in-person interview with the claimant.",
                "Notify the Fraud Investigation Unit within 24 hours.",
            ],
            "escalate": {
                "required": True,
                "reason": "Multiple fraud indicators detected. This case must be reviewed by the Fraud Investigation Unit before any settlement proceeds.",
            },
        }

    if urgent_hits:
        return {
            "priority_level": "URGENT",
            "fraud_indicators": [],
            "recommended_actions": [
                "Assign a dedicated senior claims handler immediately.",
                "Contact the claimant or next of kin within 2 hours.",
                "Verify medical reports and hospital admission records.",
                "Assess eligibility for an emergency settlement advance.",
                "Coordinate with the medical liaison officer if injuries are severe.",
                "Set a 24-hour progress review checkpoint.",
            ],
            "escalate": {
                "required": True,
                "reason": "Claimant has reported serious injury or hospitalisation requiring urgent attention and possible emergency financial support.",
            },
        }

    return {
        "priority_level": "ROUTINE",
        "fraud_indicators": [],
        "recommended_actions": [
            "Send claim acknowledgement and confirmation to claimant.",
            "Request any outstanding supporting documents (photos, police report, receipts).",
            "Assign to the standard processing queue.",
            "Complete liability assessment within standard SLA (5 business days).",
            "Obtain repair or replacement quotes from approved suppliers.",
            "Issue settlement offer once assessment is complete.",
        ],
        "escalate": {
            "required": False,
            "reason": "No urgent or suspicious indicators detected. Standard processing applies.",
        },
    }


# ---------------------------------------------------------------------------
# API endpoint
# ---------------------------------------------------------------------------

@app.route("/api/triage", methods=["POST"])
def triage():
    body = request.get_json(silent=True)
    if not body or not body.get("claim_text", "").strip():
        return jsonify({"error": "claim_text is required"}), 400

    claim_text = body["claim_text"].strip()

    # In production: pass build_prompt(claim_text) to your LLM and parse the result.
    # For the prototype we use the mock analyser directly.
    _ = build_prompt(claim_text)  # kept so the import is exercised
    result = mock_triage(claim_text)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
