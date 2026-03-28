from __future__ import annotations

from typing import Any

from pydantic import Field

from app.schemas.common import CompassBaseModel, JourneyStatusEnum, NonEmptyStr, OptionalNonEmptyStr


class JourneyStepOut(CompassBaseModel):
    step_id: NonEmptyStr = Field(description="Step identifier.")
    order_index: int = Field(ge=0, description="Zero-based step ordering within the journey.")
    title: NonEmptyStr = Field(description="Short title for the step.")
    action: NonEmptyStr = Field(description="Primary action the user should take for this step.")
    documents: list[NonEmptyStr] = Field(default_factory=list, description="Documents needed for this step.")
    form_number: OptionalNonEmptyStr = Field(default=None, description="Relevant form number if one applies.")
    form_url: OptionalNonEmptyStr = Field(default=None, description="Direct link to the relevant form or resource.")
    fee_usd: float | None = Field(default=None, ge=0, description="Estimated fee in US dollars.")
    office_name: OptionalNonEmptyStr = Field(default=None, description="Office name associated with this step.")
    office_address: OptionalNonEmptyStr = Field(default=None, description="Office address associated with this step.")
    office_hours: OptionalNonEmptyStr = Field(default=None, description="Office hours for the relevant office.")
    estimated_time: OptionalNonEmptyStr = Field(default=None, description="Expected processing or completion time.")
    tip: OptionalNonEmptyStr = Field(default=None, description="Helpful practical tip to avoid common mistakes.")
    warning: OptionalNonEmptyStr = Field(default=None, description="Optional warning or caution for this step.")
    completed: bool = Field(description="Whether the user has completed this step.")


class JourneyOut(CompassBaseModel):
    journey_id: NonEmptyStr = Field(description="Journey identifier.")
    journey_type: NonEmptyStr = Field(description="High-level journey family.")
    title: NonEmptyStr = Field(description="Journey title.")
    status: JourneyStatusEnum = Field(description="Overall journey state.")
    progress: dict[str, Any] = Field(description="Progress summary for the journey.")
    steps: list[JourneyStepOut] = Field(description="Ordered steps for the journey.")
    disclaimer: NonEmptyStr = Field(description="Important disclaimer shown with the journey.")


class ProgressUpdateRequest(CompassBaseModel):
    step_id: NonEmptyStr = Field(description="Step identifier to update.")
    completed: bool = Field(description="Whether the step should be marked complete.")
