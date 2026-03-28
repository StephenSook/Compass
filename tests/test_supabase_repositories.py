from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from app.core.config import get_settings
from app.core.dependencies import ServiceContainer, get_container
from app.core.utils import new_uuid, utc_now
from app.repositories.supabase import SupabaseJourneyRepository, SupabaseSessionRepository
from app.schemas.common import ChatRoleEnum, SessionTurn
from app.schemas.onboarding import OnboardRequest


class FakeResponse:
    def __init__(self, data):
        self.data = data


class FakeSupabaseTable:
    def __init__(self, store: list[dict]) -> None:
        self.store = store
        self._mode = "select"
        self._payload = None
        self._filters: list[tuple[str, str]] = []
        self._limit: int | None = None

    def select(self, _columns: str):
        self._mode = "select"
        return self

    def insert(self, payload: dict):
        self._mode = "insert"
        self._payload = payload
        return self

    def upsert(self, payload: dict):
        self._mode = "upsert"
        self._payload = payload
        return self

    def update(self, payload: dict):
        self._mode = "update"
        self._payload = payload
        return self

    def eq(self, column: str, value: str):
        self._filters.append((column, value))
        return self

    def limit(self, count: int):
        self._limit = count
        return self

    def execute(self):
        if self._mode in {"insert", "upsert"}:
            target_index = self._find_existing_row_index()
            if target_index is None:
                self.store.append(dict(self._payload))
            else:
                self.store[target_index] = dict(self._payload)
            return FakeResponse([dict(self._payload)])

        if self._mode == "update":
            updated = []
            for index, row in enumerate(self._filtered_rows(with_index=True)):
                row_index, current = row
                merged = {**current, **self._payload}
                self.store[row_index] = merged
                updated.append(dict(merged))
            return FakeResponse(updated)

        rows = [dict(row) for row in self._filtered_rows()]
        if self._limit is not None:
            rows = rows[: self._limit]
        return FakeResponse(rows)

    def _find_existing_row_index(self) -> int | None:
        if self._payload is None:
            return None
        for index, row in enumerate(self.store):
            if row.get("id") == self._payload.get("id"):
                return index
            if row.get("journey_id") and row.get("journey_id") == self._payload.get("journey_id"):
                return index
        return None

    def _filtered_rows(self, *, with_index: bool = False):
        results = []
        for index, row in enumerate(self.store):
            if all(str(row.get(column)) == str(value) for column, value in self._filters):
                results.append((index, row) if with_index else row)
        return results


class FakeSupabaseClient:
    def __init__(self) -> None:
        self.tables: dict[str, list[dict]] = {}

    def table(self, name: str) -> FakeSupabaseTable:
        table_store = self.tables.setdefault(name, [])
        return FakeSupabaseTable(table_store)


class SupabaseRepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = FakeSupabaseClient()
        self.journey_repository = SupabaseJourneyRepository(
            self.client,
            table_name="journeys",
            payload_column="payload",
        )
        self.session_repository = SupabaseSessionRepository(
            self.client,
            table_name="sessions",
            payload_column="payload",
        )
        container = ServiceContainer()
        self.journey = container.onboarding_service.onboard(
            OnboardRequest(
                state="GA",
                county="DeKalb",
                city="Atlanta",
                goal="ga_drivers_license",
                age=23,
                has_ssn=True,
                has_foreign_license=True,
                foreign_license_country="France",
            )
        )
        self.session = container.session_service.get_session(self.journey.id)

    def test_journey_repository_round_trips_records(self) -> None:
        self.journey_repository.create(self.journey)

        stored = self.journey_repository.get(self.journey.id)

        self.assertIsNotNone(stored)
        assert stored is not None
        self.assertEqual(stored.id, self.journey.id)
        self.assertEqual(stored.user_profile.county, "DeKalb")

        updated = stored.model_copy(update={"title": "Updated Georgia Driver's License"})
        self.journey_repository.update(updated)

        refreshed = self.journey_repository.get(self.journey.id)
        assert refreshed is not None
        self.assertEqual(refreshed.title, "Updated Georgia Driver's License")

    def test_session_repository_appends_turns(self) -> None:
        self.session_repository.create(self.session)

        updated_session = self.session_repository.append_turns(
            self.journey.id,
            [
                SessionTurn(
                    id=new_uuid(),
                    role=ChatRoleEnum.USER,
                    message="Where do I go?",
                    created_at=utc_now(),
                )
            ],
        )

        self.assertEqual(len(updated_session.turns), len(self.session.turns) + 1)
        fetched = self.session_repository.get_by_journey_id(self.journey.id)
        assert fetched is not None
        self.assertEqual(fetched.turns[-1].message, "Where do I go?")

    def test_service_container_can_switch_to_supabase_mode(self) -> None:
        get_container.cache_clear()
        get_settings.cache_clear()
        with patch.dict(
            os.environ,
            {
                "DATA_BACKEND": "supabase",
                "SUPABASE_URL": "https://example.supabase.co",
                "SUPABASE_SERVICE_KEY": "service-role-key",
            },
            clear=False,
        ):
            with patch("app.core.dependencies.create_supabase_client", return_value=self.client):
                container = ServiceContainer()
        get_settings.cache_clear()
        get_container.cache_clear()

        self.assertIsInstance(container.journey_repository, SupabaseJourneyRepository)
        self.assertIsInstance(container.session_repository, SupabaseSessionRepository)


if __name__ == "__main__":
    unittest.main()
