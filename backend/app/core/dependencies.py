from functools import lru_cache

from app.core.config import get_settings
from app.repositories.memory import InMemoryJourneyRepository, InMemorySessionRepository
from app.repositories.supabase import (
    SupabaseJourneyRepository,
    SupabaseSessionRepository,
    create_supabase_client,
)
from app.services.ai_service import MockCompassAIService
from app.services.journey_service import JourneyService
from app.services.knowledge_base import KnowledgeBaseService
from app.services.onboarding_service import OnboardingService
from app.services.session_service import SessionService


class ServiceContainer:
    def __init__(self) -> None:
        settings = get_settings()
        if settings.data_backend == "supabase":
            supabase_client = create_supabase_client(settings)
            self.journey_repository = SupabaseJourneyRepository(
                supabase_client,
                table_name=settings.supabase_journeys_table,
                payload_column=settings.supabase_payload_column,
            )
            self.session_repository = SupabaseSessionRepository(
                supabase_client,
                table_name=settings.supabase_sessions_table,
                payload_column=settings.supabase_payload_column,
            )
        else:
            self.journey_repository = InMemoryJourneyRepository()
            self.session_repository = InMemorySessionRepository()
        self.knowledge_base_service = KnowledgeBaseService()
        self.ai_service = MockCompassAIService(self.knowledge_base_service)
        self.journey_service = JourneyService(self.journey_repository)
        self.session_service = SessionService(self.session_repository)
        self.onboarding_service = OnboardingService(self.journey_service, self.session_repository)


@lru_cache
def get_container() -> ServiceContainer:
    return ServiceContainer()
