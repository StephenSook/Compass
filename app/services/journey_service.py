from __future__ import annotations

from uuid import UUID

from app.core.exceptions import InvalidProgressUpdateError, JourneyNotFoundError
from app.repositories.base import JourneyRepository
from app.schemas.common import JourneyRecord, StepStatus
from app.schemas.journey import ProgressUpdateRequest
from app.services.journey_builder import build_progress_summary


class JourneyService:
    def __init__(self, journey_repository: JourneyRepository) -> None:
        self.journey_repository = journey_repository

    def get_journey(self, journey_id: UUID) -> JourneyRecord:
        journey = self.journey_repository.get(journey_id)
        if journey is None:
            raise JourneyNotFoundError(f"Journey '{journey_id}' was not found.")
        return journey

    def update_progress(self, journey_id: UUID, payload: ProgressUpdateRequest) -> JourneyRecord:
        journey = self.get_journey(journey_id)
        updates_by_step_id = {update.step_id: update.completed for update in payload.step_updates}

        if len(updates_by_step_id) != len(payload.step_updates):
            raise InvalidProgressUpdateError("Duplicate step ids are not allowed in one progress update.")

        known_step_ids = {step.id for step in journey.steps}
        unknown_step_ids = [str(step_id) for step_id in updates_by_step_id if step_id not in known_step_ids]
        if unknown_step_ids:
            raise InvalidProgressUpdateError(
                f"Unknown step ids for this journey: {', '.join(unknown_step_ids)}."
            )

        updated_steps = []
        for step in journey.steps:
            if step.id in updates_by_step_id:
                status = StepStatus.COMPLETED if updates_by_step_id[step.id] else StepStatus.NOT_STARTED
                updated_steps.append(step.model_copy(update={"status": status}))
            else:
                updated_steps.append(step)

        if updated_steps and all(step.status != StepStatus.IN_PROGRESS for step in updated_steps):
            for index, step in enumerate(updated_steps):
                if step.status != StepStatus.COMPLETED:
                    updated_steps[index] = step.model_copy(update={"status": StepStatus.IN_PROGRESS})
                    break

        updated_journey = journey.model_copy(
            update={
                "steps": updated_steps,
                "progress": build_progress_summary(updated_steps),
            }
        )
        return self.journey_repository.update(updated_journey)
