from __future__ import annotations

from typing import Any

from pydantic import Field

from app.schemas.common import CompassBaseModel, JourneyTypeEnum, NonEmptyStr


class RoutingDecision(CompassBaseModel):
    journey_type: JourneyTypeEnum
    template_key: NonEmptyStr
    branch_key: NonEmptyStr
    branch_summary: dict[str, Any] = Field(default_factory=dict)
    derived_flags: dict[str, Any] = Field(default_factory=dict)
