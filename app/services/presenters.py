from __future__ import annotations

import re
from typing import Any

from app.schemas.common import JourneyRecord, JourneyStatusEnum, SessionRecord, build_profile_summary
from app.schemas.journey import JourneyOut, JourneyStepOut
from app.schemas.onboarding import OnboardResponse
from app.schemas.session import AskResponse, SessionOut


FEE_PATTERN = re.compile(r"\$([0-9]+(?:\.[0-9]{1,2})?)")
FORM_NUMBER_PATTERN = re.compile(r"\b([A-Z]{1,3}-\d{2,4})\b")


def present_onboard_response(journey: JourneyRecord) -> OnboardResponse:
    branch_summary = {
        "branch_key": journey.branch_key,
        "journey_type": _enum_value(journey.journey_type),
        "state": journey.state,
        "language": journey.language,
        **journey.branch_summary,
    }
    return OnboardResponse(
        user_id=str(journey.user_id),
        profile_id=str(journey.profile_id),
        journey_id=str(journey.id),
        journey_type=_enum_value(journey.journey_type),
        branch_summary=branch_summary,
        derived_flags=dict(journey.derived_flags),
        next_action="generate_journey",
    )


def present_journey(journey: JourneyRecord) -> JourneyOut:
    return JourneyOut(
        journey_id=str(journey.id),
        journey_type=_enum_value(journey.journey_type),
        title=journey.title,
        status=journey.status,
        progress=_progress_payload(journey),
        steps=[present_journey_step(step, index) for index, step in enumerate(journey.steps)],
        disclaimer=_disclaimer_for(journey),
    )


def present_journey_step(step, order_index: int) -> JourneyStepOut:
    first_form = step.forms[0] if step.forms else None
    return JourneyStepOut(
        step_id=str(step.id),
        order_index=order_index,
        title=step.title,
        action=step.description,
        documents=step.documents,
        form_number=_extract_form_number(first_form.name) if first_form else None,
        form_url=first_form.url if first_form else None,
        fee_usd=_extract_fee(step.fee),
        office_name=step.office.name if step.office else None,
        office_address=step.office.address if step.office else None,
        office_hours=step.office.hours if step.office else None,
        estimated_time=step.timeline,
        tip=step.tip,
        warning=step.warning,
        completed=step.status == JourneyStatusEnum.COMPLETED,
    )


def present_ask_response(
    *,
    answer: str,
    legal_warning: bool,
    citations: list[dict[str, str]],
    recommended_next_step: str | None,
) -> AskResponse:
    return AskResponse(
        answer=answer,
        citations=[dict(citation) for citation in citations],
        legal_warning=legal_warning,
        recommended_next_step=recommended_next_step,
    )


def present_session(journey: JourneyRecord, session: SessionRecord) -> SessionOut:
    return SessionOut(
        journey_id=str(journey.id),
        profile_summary=build_profile_summary(journey.user_profile),
        journey=present_journey(journey),
        chat_history=[
            {
                "id": str(turn.id),
                "role": _enum_value(turn.role),
                "message": turn.message,
                "created_at": turn.created_at.isoformat(),
            }
            for turn in session.turns
        ],
    )


def _progress_payload(journey: JourneyRecord) -> dict[str, Any]:
    return {
        "completed_steps": journey.progress.completed_steps,
        "total_steps": journey.progress.total_steps,
        "percent": journey.progress.percent_complete,
    }


def _disclaimer_for(journey: JourneyRecord) -> str:
    return "This tool provides guidance, not legal advice."


def _next_step_title(journey: JourneyRecord) -> str | None:
    for step in journey.steps:
        if step.status != JourneyStatusEnum.COMPLETED:
            return step.title
    return journey.steps[-1].title if journey.steps else None


def _extract_fee(value: str | None) -> float | None:
    if not value:
        return None
    match = FEE_PATTERN.search(value)
    return float(match.group(1)) if match else None


def _extract_form_number(value: str | None) -> str | None:
    if not value:
        return None
    match = FORM_NUMBER_PATTERN.search(value.upper())
    return match.group(1) if match else None


def _enum_value(value: Any) -> Any:
    return value.value if hasattr(value, "value") else value
