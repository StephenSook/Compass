from __future__ import annotations

from uuid import UUID

from pydantic import Field

from app.schemas.common import CompassBaseModel, JourneyRecord, SessionRecord, UserProfile


class OnboardRequest(UserProfile):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "state": "Georgia",
                    "county": "Fulton",
                    "city": "Atlanta",
                    "goal": "Georgia driver's license",
                    "preferred_language": "en",
                    "age": 24,
                    "has_ssn": True,
                    "has_us_license": False,
                    "foreign_license_country": "Brazil",
                    "immigration_status": "F-1 student",
                    "additional_context": {"needs_interpreter": "false"},
                }
            ]
        }
    }


class OnboardResponse(CompassBaseModel):
    journey_id: UUID
    session_id: UUID
    branch_key: str
    journey: JourneyRecord
    session: SessionRecord
    next_recommended_action: str = Field(
        default="Review the generated checklist and ask follow-up questions if anything is unclear."
    )
