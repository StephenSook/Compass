from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Annotated, Any
from uuid import UUID

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, StringConstraints, field_validator


NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
OptionalNonEmptyStr = Annotated[str | None, AfterValidator(lambda value: validate_optional_non_empty(value))]


class CompassBaseModel(BaseModel):
    model_config = ConfigDict(use_enum_values=True, populate_by_name=True, str_strip_whitespace=True)


class GoalEnum(str, Enum):
    GA_DRIVERS_LICENSE = "ga_drivers_license"
    PASSPORT_NEW = "passport_new"
    PASSPORT_RENEWAL = "passport_renewal"
    F1_OPT = "f1_opt"
    FAMILY_GREEN_CARD = "family_green_card"
    VISA_EXTENSION = "visa_extension"


class JourneyTypeEnum(str, Enum):
    DRIVERS_LICENSE = "drivers_license"
    PASSPORT = "passport"
    VISA = "visa"


class JourneyStatusEnum(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class ChatRoleEnum(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class FormInfo(CompassBaseModel):
    name: NonEmptyStr
    url: str | None = None

    @field_validator("url")
    @classmethod
    def validate_optional_url(cls, value: str | None) -> str | None:
        return validate_optional_non_empty(value)


class OfficeInfo(CompassBaseModel):
    name: NonEmptyStr
    address: NonEmptyStr
    hours: str | None = None
    appointment_url: str | None = None

    @field_validator("hours", "appointment_url")
    @classmethod
    def validate_optional_text_fields(cls, value: str | None) -> str | None:
        return validate_optional_non_empty(value)


class JourneyStep(CompassBaseModel):
    id: UUID
    title: NonEmptyStr
    description: NonEmptyStr
    status: JourneyStatusEnum = JourneyStatusEnum.NOT_STARTED
    documents: list[NonEmptyStr] = Field(default_factory=list)
    forms: list[FormInfo] = Field(default_factory=list)
    fee: str | None = None
    office: OfficeInfo | None = None
    timeline: str | None = None
    tip: str | None = None
    warning: str | None = None

    @field_validator("fee", "timeline", "tip", "warning")
    @classmethod
    def validate_optional_text_fields(cls, value: str | None) -> str | None:
        return validate_optional_non_empty(value)


class ProgressSummary(CompassBaseModel):
    total_steps: int = Field(ge=0)
    completed_steps: int = Field(ge=0)
    percent_complete: int = Field(ge=0, le=100)


class UserProfile(CompassBaseModel):
    state: NonEmptyStr
    county: str | None = None
    city: str | None = None
    language: NonEmptyStr = Field(default="en")
    goal: GoalEnum
    immigration_status: str | None = None
    age: int | None = Field(default=None, ge=0, le=130)
    has_ssn: bool | None = None
    has_us_license: bool | None = None
    has_foreign_license: bool | None = None
    foreign_license_country: str | None = None

    @field_validator("county", "city", "immigration_status", "foreign_license_country")
    @classmethod
    def validate_optional_text_fields(cls, value: str | None) -> str | None:
        return validate_optional_non_empty(value)


class JourneyRecord(CompassBaseModel):
    id: UUID
    user_id: UUID
    profile_id: UUID
    session_id: UUID
    title: NonEmptyStr
    journey_type: JourneyTypeEnum
    branch_key: NonEmptyStr
    summary: NonEmptyStr
    status: JourneyStatusEnum
    state: NonEmptyStr
    language: NonEmptyStr
    user_profile: UserProfile
    steps: list[JourneyStep]
    progress: ProgressSummary
    created_at: datetime
    updated_at: datetime


class SessionTurn(CompassBaseModel):
    id: UUID
    role: ChatRoleEnum
    message: NonEmptyStr
    created_at: datetime


class SessionRecord(CompassBaseModel):
    id: UUID
    journey_id: UUID
    title: NonEmptyStr
    turns: list[SessionTurn]
    created_at: datetime
    updated_at: datetime


def validate_optional_non_empty(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("Value cannot be empty or whitespace only.")
    return cleaned


def build_profile_summary(profile: UserProfile) -> dict[str, Any]:
    return {
        "state": profile.state,
        "county": profile.county,
        "city": profile.city,
        "language": profile.language,
        "goal": profile.goal.value if hasattr(profile.goal, "value") else profile.goal,
        "immigration_status": profile.immigration_status,
        "age": profile.age,
        "has_ssn": profile.has_ssn,
        "has_us_license": profile.has_us_license,
        "has_foreign_license": profile.has_foreign_license,
        "foreign_license_country": profile.foreign_license_country,
    }
