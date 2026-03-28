from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from app.schemas.common import JourneyRecord, SessionRecord, SessionTurn


class JourneyRepository(ABC):
    @abstractmethod
    def create(self, journey: JourneyRecord) -> JourneyRecord:
        raise NotImplementedError

    @abstractmethod
    def get(self, journey_id: UUID) -> JourneyRecord | None:
        raise NotImplementedError

    @abstractmethod
    def update(self, journey: JourneyRecord) -> JourneyRecord:
        raise NotImplementedError


class SessionRepository(ABC):
    @abstractmethod
    def create(self, session: SessionRecord) -> SessionRecord:
        raise NotImplementedError

    @abstractmethod
    def get_by_journey_id(self, journey_id: UUID) -> SessionRecord | None:
        raise NotImplementedError

    @abstractmethod
    def append_turns(self, journey_id: UUID, turns: list[SessionTurn]) -> SessionRecord:
        raise NotImplementedError
