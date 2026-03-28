from __future__ import annotations

from app.core.utils import new_uuid, utc_now
from app.schemas.common import FormInfo, JourneyRecord, JourneyStep, OfficeInfo, ProgressSummary, UserProfile


def build_progress_summary(steps: list[JourneyStep]) -> ProgressSummary:
    total_steps = len(steps)
    completed_steps = sum(1 for step in steps if step.status == "completed")
    percent_complete = int((completed_steps / total_steps) * 100) if total_steps else 0
    return ProgressSummary(
        total_steps=total_steps,
        completed_steps=completed_steps,
        percent_complete=percent_complete,
    )


def build_journey_record(
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
        steps[0] = steps[0].model_copy(update={"status": "in_progress"})

    timestamp = utc_now()
    return JourneyRecord(
        id=new_uuid(),
        session_id=session_id,
        title=template["title"],
        journey_type=template["journey_type"],
        branch_key=branch_key,
        summary=template["summary"],
        state=profile.state,
        preferred_language=profile.preferred_language,
        user_profile=profile,
        steps=steps,
        progress=build_progress_summary(steps),
        created_at=timestamp,
        updated_at=timestamp,
    )
