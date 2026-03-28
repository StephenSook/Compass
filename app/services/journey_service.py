from __future__ import annotations

from uuid import UUID

from app.core.exceptions import InvalidProgressUpdateError, JourneyNotFoundError
from app.repositories.base import JourneyRepository
from app.schemas.common import JourneyRecord, JourneyStatusEnum
from app.schemas.journey import ProgressUpdateRequest
from app.services.journey_builder import build_progress_summary, determine_journey_status


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
        try:
            target_step_id = UUID(payload.step_id)
        except ValueError as exc:
            raise InvalidProgressUpdateError("step_id must be a valid UUID string.") from exc

        updated_steps = []
        step_found = False
        for step in journey.steps:
            if step.id == target_step_id:
                step_found = True
                status = JourneyStatusEnum.COMPLETED if payload.completed else JourneyStatusEnum.NOT_STARTED
                updated_steps.append(step.model_copy(update={"status": status}))
            else:
                updated_steps.append(step)

        if not step_found:
            raise InvalidProgressUpdateError(f"Unknown step id for this journey: {payload.step_id}.")

        if updated_steps and not all(step.status == JourneyStatusEnum.COMPLETED for step in updated_steps):
            updated_steps = [
                step.model_copy(update={"status": JourneyStatusEnum.NOT_STARTED})
                if step.status == JourneyStatusEnum.IN_PROGRESS
                else step
                for step in updated_steps
            ]
            for index, step in enumerate(updated_steps):
                if step.status != JourneyStatusEnum.COMPLETED:
                    updated_steps[index] = step.model_copy(update={"status": JourneyStatusEnum.IN_PROGRESS})
                    break

        updated_journey = journey.model_copy(
            update={
                "steps": updated_steps,
                "progress": build_progress_summary(updated_steps),
                "status": determine_journey_status(updated_steps),
            }
        )
        return self.journey_repository.update(updated_journey)
