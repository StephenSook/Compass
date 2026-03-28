from __future__ import annotations

from uuid import UUID

from app.core.utils import utc_now
from app.repositories.base import JourneyRepository, SessionRepository
from app.schemas.common import JourneyRecord, SessionRecord, SessionTurn


class InMemoryJourneyRepository(JourneyRepository):
    def __init__(self) -> None:
        self._journeys: dict[UUID, JourneyRecord] = {}

    def create(self, journey: JourneyRecord) -> JourneyRecord:
        self._journeys[journey.id] = journey
        return journey

    def get(self, journey_id: UUID) -> JourneyRecord | None:
        return self._journeys.get(journey_id)

    def update(self, journey: JourneyRecord) -> JourneyRecord:
        updated_journey = journey.model_copy(update={"updated_at": utc_now()})
        self._journeys[journey.id] = updated_journey
        return updated_journey


class InMemorySessionRepository(SessionRepository):
    def __init__(self) -> None:
        self._sessions_by_journey_id: dict[UUID, SessionRecord] = {}

    def create(self, session: SessionRecord) -> SessionRecord:
        self._sessions_by_journey_id[session.journey_id] = session
        return session

    def get_by_journey_id(self, journey_id: UUID) -> SessionRecord | None:
        return self._sessions_by_journey_id.get(journey_id)

    def append_turns(self, journey_id: UUID, turns: list[SessionTurn]) -> SessionRecord:
        session = self._sessions_by_journey_id[journey_id]
        updated_session = session.model_copy(
            update={"turns": [*session.turns, *turns], "updated_at": utc_now()}
        )
        self._sessions_by_journey_id[journey_id] = updated_session
        return updated_session
