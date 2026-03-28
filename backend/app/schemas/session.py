from __future__ import annotations

from typing import Any

from pydantic import Field

from app.schemas.common import CompassBaseModel, NonEmptyStr, OptionalNonEmptyStr
from app.schemas.journey import JourneyOut


class AskRequest(CompassBaseModel):
    question: NonEmptyStr = Field(
        min_length=3,
        max_length=2_000,
        description="Plain-language question asked in the context of a journey.",
    )


class AskResponse(CompassBaseModel):
    answer: NonEmptyStr = Field(description="Grounded answer returned to the user.")
    citations: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Supporting citations or references relevant to the answer.",
    )
    legal_warning: bool = Field(
        description="Whether the answer includes or requires additional legal caution."
    )
    recommended_next_step: OptionalNonEmptyStr = Field(
        default=None,
        description="Recommended next checklist step for the user, if one is available.",
    )


class SessionOut(CompassBaseModel):
    journey_id: NonEmptyStr = Field(description="Journey identifier associated with this session.")
    profile_summary: dict[str, Any] = Field(description="Summarized onboarding profile information.")
    journey: JourneyOut = Field(description="Current journey view tied to this session.")
    chat_history: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Chronological chat history for the journey session.",
    )
