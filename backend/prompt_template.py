"""
Prompt template builder for the Insurance Claims Triage Assistant.
In a production system this would be passed to an LLM API.
"""


def build_prompt(claim_text: str) -> str:
    return f"""You are an experienced insurance claims analyst. Analyse the following claim summary and return a structured triage report.

CLAIM SUMMARY:
{claim_text}

Provide your analysis in the following JSON structure:
{{
  "priority_level": "ROUTINE | URGENT | CRITICAL",
  "fraud_indicators": ["list of specific fraud indicators found, or empty list"],
  "recommended_actions": ["ordered list of recommended next steps"],
  "escalate": {{
    "required": true | false,
    "reason": "brief explanation of escalation decision"
  }}
}}

Guidelines:
- ROUTINE: Minor claims, clear liability, no injuries, no suspicious patterns
- URGENT: Injuries involved, hospitalisation, emergency financial needs, time-sensitive
- CRITICAL: Strong fraud indicators, high-value suspicious claims, multiple red flags
- Escalate if URGENT or CRITICAL, or if any fraud indicators are present
"""
