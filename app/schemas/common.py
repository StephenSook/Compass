from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CompassBaseModel(BaseModel):
    model_config = ConfigDict(use_enum_values=True, populate_by_name=True)


class StepStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class FormInfo(CompassBaseModel):
    name: str
    url: str | None = None


class OfficeInfo(CompassBaseModel):
    name: str
    address: str
    hours: str | None = None
    appointment_url: str | None = None


class JourneyStep(CompassBaseModel):
    id: UUID
    title: str
    description: str
    status: StepStatus = StepStatus.NOT_STARTED
    documents: list[str] = Field(default_factory=list)
    forms: list[FormInfo] = Field(default_factory=list)
    fee: str | None = None
    office: OfficeInfo | None = None
    timeline: str | None = None
    tip: str | None = None


class ProgressSummary(CompassBaseModel):
    total_steps: int
    completed_steps: int
    percent_complete: int


class UserProfile(CompassBaseModel):
    state: str
    county: str
    city: str | None = None
    goal: str
    preferred_language: str = "en"
    age: int | None = None
    has_ssn: bool | None = None
    has_us_license: bool | None = None
    foreign_license_country: str | None = None
    immigration_status: str | None = None
    passport_application_type: str | None = None
    visa_goal: str | None = None
    additional_context: dict[str, str] = Field(default_factory=dict)


class JourneyRecord(CompassBaseModel):
    id: UUID
    session_id: UUID
    title: str
    journey_type: str
    branch_key: str
    summary: str
    state: str
    preferred_language: str
    user_profile: UserProfile
    steps: list[JourneyStep]
    progress: ProgressSummary
    created_at: datetime
    updated_at: datetime


class SessionTurn(CompassBaseModel):
    id: UUID
    role: str
    message: str
    created_at: datetime


class SessionRecord(CompassBaseModel):
    id: UUID
    journey_id: UUID
    title: str
    turns: list[SessionTurn]
    created_at: datetime
    updated_at: datetime
