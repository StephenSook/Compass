from __future__ import annotations

from app.core.utils import new_uuid, utc_now
from app.schemas.common import (
    FormInfo,
    JourneyRecord,
    JourneyStatusEnum,
    JourneyStep,
    JourneyTypeEnum,
    OfficeInfo,
    ProgressSummary,
    UserProfile,
)


def build_progress_summary(steps: list[JourneyStep]) -> ProgressSummary:
    total_steps = len(steps)
    completed_steps = sum(1 for step in steps if step.status == JourneyStatusEnum.COMPLETED)
    percent_complete = int((completed_steps / total_steps) * 100) if total_steps else 0
    return ProgressSummary(
        total_steps=total_steps,
        completed_steps=completed_steps,
        percent_complete=percent_complete,
    )


def determine_journey_status(steps: list[JourneyStep]) -> JourneyStatusEnum:
    if not steps:
        return JourneyStatusEnum.NOT_STARTED
    if all(step.status == JourneyStatusEnum.COMPLETED for step in steps):
        return JourneyStatusEnum.COMPLETED
    if any(step.status in {JourneyStatusEnum.IN_PROGRESS, JourneyStatusEnum.COMPLETED} for step in steps):
        return JourneyStatusEnum.IN_PROGRESS
    return JourneyStatusEnum.NOT_STARTED


def build_journey_record(
    user_id,
    profile_id,
    session_id,
    branch_key: str,
    profile: UserProfile,
    template: dict[str, object],
) -> JourneyRecord:
    steps = [
        JourneyStep(
            id=new_uuid(),
            title=step_template["title"],
            description=step_template["description"],
            documents=step_template.get("documents", []),
            forms=[FormInfo(**form) for form in step_template.get("forms", [])],
            fee=step_template.get("fee"),
            office=OfficeInfo(**step_template["office"]) if step_template.get("office") else None,
            timeline=step_template.get("timeline"),
            tip=step_template.get("tip"),
        )
        for step_template in template["steps"]
    ]
    if steps:
        steps[0] = steps[0].model_copy(update={"status": JourneyStatusEnum.IN_PROGRESS})

    timestamp = utc_now()
    return JourneyRecord(
        id=new_uuid(),
        user_id=user_id,
        profile_id=profile_id,
        session_id=session_id,
        title=template["title"],
        journey_type=JourneyTypeEnum(template["journey_type"]),
        branch_key=branch_key,
        summary=template["summary"],
        status=determine_journey_status(steps),
        state=profile.state,
        language=profile.language,
        user_profile=profile,
        steps=steps,
        progress=build_progress_summary(steps),
        created_at=timestamp,
        updated_at=timestamp,
    )
