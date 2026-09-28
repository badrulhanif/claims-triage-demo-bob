# Insurance Claims Triage Assistant

A lightweight web prototype that analyses insurance claim summaries and returns a structured triage report — including a priority level, fraud indicators, recommended actions, and an escalation decision.

Built as a hackathon prototype. The backend uses a keyword-based mock analyser so **no LLM API key is required**.

---

## Project Structure

```
claims-triage/
├── backend/
│   ├── app.py               # Flask API server
│   ├── prompt_template.py   # LLM prompt builder (ready for real integration)
│   └── requirements.txt
├── frontend/
│   ├── index.html           # Claim input form
│   ├── result.html          # Triage results page
│   └── style.css
├── mock_claims/
│   ├── routine.json
│   ├── urgent.json
│   └── fraud_risk.json
└── README.md
```

---

## Running the Backend

```bash
# 1. Navigate to the backend directory
cd backend

# 2. (Optional) create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate.bat       # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the Flask server
flask --app app run --debug
```

The API will be available at `http://127.0.0.1:5000`.

### Endpoint

| Method | Path         | Description                  |
|--------|--------------|------------------------------|
| POST   | `/api/triage`| Analyse a claim (JSON body)  |

**Request body:**
```json
{ "claim_text": "…your claim summary…" }
```

**Response:**
```json
{
  "priority_level": "ROUTINE | URGENT | CRITICAL",
  "fraud_indicators": ["…"],
  "recommended_actions": ["…"],
  "escalate": {
    "required": true,
    "reason": "…"
  }
}
```

---

## Opening the Frontend

Simply open `frontend/index.html` in your browser.  
Make sure the Flask backend is running first so API calls succeed.

> **Tip:** Use the "Load a demo scenario" dropdown to auto-fill the textarea with one of the three mock claims.

---

## Mock Claim Scenarios

| Scenario | File | Description |
|---|---|---|
| **Routine** | `mock_claims/routine.json` | Minor rear-end collision in a car park. Single vehicle, police report filed, no injuries, clear liability, claimant's first claim in 5 years. Expected result: **ROUTINE**, no escalation. |
| **Urgent** | `mock_claims/urgent.json` | Multi-vehicle motorway accident. Claimant hospitalised with spinal injury, family involved, emergency settlement advance requested, time-critical medical decisions required. Expected result: **URGENT**, escalation required. |
| **Fraud Risk** | `mock_claims/fraud_risk.json` | High-value home contents theft claim. Third claim in 6 months, luxury electronics and jewellery alleged stolen, no witnesses, receipt dates inconsistent with theft date, neighbour disputes account, no signs of forced entry. Expected result: **CRITICAL**, fraud investigation required. |

---

## Upgrading to a Real LLM

The mock analyser in `app.py` can be swapped for a real LLM call with minimal changes:

1. In `app.py`, replace the `mock_triage()` call in the `/api/triage` route with a call to your preferred LLM API (e.g. IBM watsonx, OpenAI).
2. Pass the string returned by `build_prompt(claim_text)` from `prompt_template.py` as the user message.
3. Parse the JSON returned by the LLM and return it from the endpoint.

---

## Tech Stack

| Layer    | Technology                        |
|----------|-----------------------------------|
| Backend  | Python 3 · Flask · flask-cors     |
| Frontend | HTML5 · CSS3 · Vanilla JavaScript |
| Storage  | None (stateless per request)      |
