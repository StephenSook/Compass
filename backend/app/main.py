import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai

from app.models import UserProfile, JourneyResponse, AskRequest
from app.prompts import SYSTEM_PROMPT
from app.kb import GA_DRIVERS_LICENSE_KB, VISA_PASSPORT_KB

from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

app = FastAPI(title="Compass API")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("Missing GEMINI_API_KEY in environment")

client = genai.Client(api_key=api_key)

def get_kb(goal: str) -> str:
    goal_lower = goal.lower()
    if "driver" in goal_lower or "license" in goal_lower:
        return GA_DRIVERS_LICENSE_KB
    if "passport" in goal_lower or "visa" in goal_lower or "opt" in goal_lower:
        return VISA_PASSPORT_KB
    return "No matching knowledge base found. Be cautious and avoid guessing."

def build_journey_prompt(profile: UserProfile, kb_context: str) -> str:
    return f"""
User Profile:
- State: {profile.state}
- County: {profile.county}
- Situation: {profile.situation}
- Goal: {profile.goal}
- Language: {profile.language}
- Age: {profile.age}
- Has SSN: {profile.has_ssn}
- Foreign License Country: {profile.foreign_license_country}

Knowledge Base Context:
{kb_context}

Generate the personalized checklist now.
Return ONLY valid JSON.
"""

@app.get("/")
def root():
    return {"message": "Compass backend is running"}

@app.post("/journey")
def generate_journey(profile: UserProfile):
    kb_context = get_kb(profile.goal)
    prompt = build_journey_prompt(profile, kb_context)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{SYSTEM_PROMPT}\n\n{prompt}"
        )

        raw_text = response.text.strip()

        # Clean common Gemini issues
        if raw_text.startswith("```"):
            raw_text = raw_text.replace("```json", "").replace("```", "").strip()

        try:
            parsed = json.loads(raw_text)
        except:
            print("RAW MODEL OUTPUT:", raw_text)  # DEBUG
            raise HTTPException(status_code=500, detail="Model returned invalid JSON")

        return parsed

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
def ask_followup(payload: AskRequest):
    try:
        followup_prompt = f"""
You are helping the same user continue their Compass journey.

User Profile:
- State: {payload.user_profile.state}
- County: {payload.user_profile.county}
- Situation: {payload.user_profile.situation}
- Goal: {payload.user_profile.goal}
- Language: {payload.user_profile.language}
- Age: {payload.user_profile.age}
- Has SSN: {payload.user_profile.has_ssn}
- Foreign License Country: {payload.user_profile.foreign_license_country}

Journey Name:
{payload.journey_name}

Checklist Context:
{payload.checklist_context}

User Follow-up Question:
{payload.question}

Answer clearly and practically.
Do not guess.
If this is immigration/legal territory, include:
"This is general guidance and not legal advice."
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=followup_prompt
        )

        return {"answer": response.text.strip()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))