from __future__ import annotations

from typing import Any
from uuid import UUID

from app.core.config import Settings
from app.repositories.base import JourneyRepository, SessionRepository
from app.schemas.common import JourneyRecord, SessionRecord, SessionTurn


def create_supabase_client(settings: Settings) -> Any:
    if not settings.supabase_url:
        raise ValueError("SUPABASE_URL is required when DATA_BACKEND='supabase'.")

    if settings.supabase_url.startswith(("postgres://", "postgresql://")):
        raise ValueError(
            "SUPABASE_URL must be the Supabase project HTTPS URL, not a Postgres connection string."
        )

    key = settings.supabase_service_key or settings.supabase_anon_key
    if not key:
        raise ValueError(
            "SUPABASE_SERVICE_KEY or SUPABASE_ANON_KEY is required when DATA_BACKEND='supabase'."
        )

    from supabase import create_client

    return create_client(settings.supabase_url, key)


class SupabaseJourneyRepository(JourneyRepository):
    def __init__(self, client: Any, *, table_name: str, payload_column: str) -> None:
        self.client = client
        self.table_name = table_name
        self.payload_column = payload_column

    def create(self, journey: JourneyRecord) -> JourneyRecord:
        self._upsert(journey)
        return journey

    def get(self, journey_id: UUID) -> JourneyRecord | None:
        response = (
            self.client.table(self.table_name)
            .select("*")
            .eq("id", str(journey_id))
            .limit(1)
            .execute()
        )
        if not response.data:
            return None
        return JourneyRecord(**response.data[0][self.payload_column])

    def update(self, journey: JourneyRecord) -> JourneyRecord:
        self._upsert(journey)
        return journey

    def _upsert(self, journey: JourneyRecord) -> None:
        row = {
            "id": str(journey.id),
            self.payload_column: journey.model_dump(mode="json"),
        }
        self.client.table(self.table_name).upsert(row).execute()


class SupabaseSessionRepository(SessionRepository):
    def __init__(self, client: Any, *, table_name: str, payload_column: str) -> None:
        self.client = client
        self.table_name = table_name
        self.payload_column = payload_column

    def create(self, session: SessionRecord) -> SessionRecord:
        self._upsert(session)
        return session

    def get_by_journey_id(self, journey_id: UUID) -> SessionRecord | None:
        response = (
            self.client.table(self.table_name)
            .select("*")
            .eq("journey_id", str(journey_id))
            .limit(1)
            .execute()
        )
        if not response.data:
            return None
        return SessionRecord(**response.data[0][self.payload_column])

    def append_turns(self, journey_id: UUID, turns: list[SessionTurn]) -> SessionRecord:
        session = self.get_by_journey_id(journey_id)
        if session is None:
            raise KeyError(f"Session for journey '{journey_id}' was not found.")
        updated_session = session.model_copy(update={"turns": [*session.turns, *turns]})
        self._upsert(updated_session)
        return updated_session

    def _upsert(self, session: SessionRecord) -> None:
        row = {
            "id": str(session.id),
            "journey_id": str(session.journey_id),
            self.payload_column: session.model_dump(mode="json"),
        }
        self.client.table(self.table_name).upsert(row).execute()
