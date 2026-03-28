from __future__ import annotations

from uuid import UUID

from app.core.exceptions import JourneyNotFoundError
from app.core.utils import new_uuid, utc_now
from app.repositories.base import SessionRepository
from app.schemas.common import SessionRecord, SessionTurn


class SessionService:
    def __init__(self, session_repository: SessionRepository) -> None:
        self.session_repository = session_repository

    def get_session(self, journey_id: UUID) -> SessionRecord:
        session = self.session_repository.get_by_journey_id(journey_id)
        if session is None:
            raise JourneyNotFoundError(f"Session for journey '{journey_id}' was not found.")
        return session

    def append_conversation(self, journey_id: UUID, question: str, answer: str) -> SessionRecord:
        timestamp = utc_now()
        turns = [
            SessionTurn(id=new_uuid(), role="user", message=question, created_at=timestamp),
            SessionTurn(id=new_uuid(), role="assistant", message=answer, created_at=timestamp),
        ]
        return self.session_repository.append_turns(journey_id, turns)
