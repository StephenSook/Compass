from __future__ import annotations

from uuid import UUID

from pydantic import Field

from app.schemas.common import CompassBaseModel, JourneyRecord, ProgressSummary


class JourneyResponse(CompassBaseModel):
    journey: JourneyRecord


class StepProgressUpdate(CompassBaseModel):
    step_id: UUID
    completed: bool = True


class ProgressUpdateRequest(CompassBaseModel):
    step_updates: list[StepProgressUpdate] = Field(min_length=1)


class ProgressUpdateResponse(CompassBaseModel):
    journey_id: UUID
    progress: ProgressSummary
    journey: JourneyRecord
