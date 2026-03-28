from pydantic import BaseModel
from typing import List, Optional

class UserProfile(BaseModel):
    state: str
    county: str
    situation: str
    goal: str
    language: Optional[str] = "English"
    age: Optional[int] = None
    has_ssn: Optional[bool] = None
    foreign_license_country: Optional[str] = None

class ChecklistStep(BaseModel):
    step: int
    title: str
    action: str
    documents: str
    cost: str
    location: str
    timeline: str
    tip: str

class JourneyResponse(BaseModel):
    journey_name: str
    disclaimer: str
    steps: List[ChecklistStep]

class AskRequest(BaseModel):
    user_profile: UserProfile
    journey_name: str
    checklist_context: str
    question: str