from __future__ import annotations

from uuid import UUID

from pydantic import Field

from app.schemas.common import CompassBaseModel, SessionRecord, SessionTurn


class AskJourneyRequest(CompassBaseModel):
    question: str = Field(min_length=3, max_length=2_000)


class AskJourneyResponse(CompassBaseModel):
    journey_id: UUID
    session_id: UUID
    answer: str
    session: SessionRecord


class SessionResponse(CompassBaseModel):
    session: SessionRecord
