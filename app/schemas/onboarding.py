from __future__ import annotations

from typing import Any

from pydantic import Field

from app.schemas.common import CompassBaseModel, GoalEnum, NonEmptyStr, OptionalNonEmptyStr, UserProfile


class OnboardRequest(UserProfile):
    state: NonEmptyStr = Field(description="US state where the user is completing the process.")
    county: OptionalNonEmptyStr = Field(default=None, description="County relevant to the user's journey.")
    city: OptionalNonEmptyStr = Field(default=None, description="City relevant to the user's journey.")
    language: NonEmptyStr = Field(default="en", description="Preferred language code for responses.")
    goal: GoalEnum = Field(description="Primary guided process the user wants help with.")
    immigration_status: OptionalNonEmptyStr = Field(
        default=None,
        description="Current immigration status when relevant to the selected goal.",
    )
    age: int | None = Field(default=None, ge=0, le=130, description="User age if it affects branching.")
    has_ssn: bool | None = Field(default=None, description="Whether the user has a Social Security Number.")
    has_us_license: bool | None = Field(
        default=None,
        description="Whether the user currently holds a driver's license from another US state.",
    )
    has_foreign_license: bool | None = Field(
        default=None,
        description="Whether the user currently holds a driver's license issued outside the US.",
    )
    foreign_license_country: OptionalNonEmptyStr = Field(
        default=None,
        description="Country that issued the foreign driver's license, if applicable.",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "state": "Georgia",
                    "county": "Fulton",
                    "city": "Atlanta",
                    "language": "en",
                    "goal": "ga_drivers_license",
                    "immigration_status": "F-1 student",
                    "age": 24,
                    "has_ssn": True,
                    "has_us_license": False,
                    "has_foreign_license": True,
                    "foreign_license_country": "Brazil",
                }
            ]
        }
    }


class OnboardResponse(CompassBaseModel):
    user_id: NonEmptyStr = Field(description="Stable user identifier for the current onboarding result.")
    profile_id: NonEmptyStr = Field(description="Identifier for the stored onboarding profile.")
    journey_id: NonEmptyStr = Field(description="Identifier for the generated journey.")
    journey_type: NonEmptyStr = Field(description="High-level journey family selected for the user.")
    branch_summary: dict[str, Any] = Field(
        description="Structured summary of the branch decision and important profile signals."
    )
    next_action: NonEmptyStr = Field(description="Single best next action the frontend should emphasize.")
