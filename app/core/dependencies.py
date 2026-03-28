from functools import lru_cache

from app.repositories.memory import InMemoryJourneyRepository, InMemorySessionRepository
from app.services.ai_service import MockCompassAIService
from app.services.journey_service import JourneyService
from app.services.onboarding_service import OnboardingService
from app.services.session_service import SessionService


class ServiceContainer:
    def __init__(self) -> None:
        self.journey_repository = InMemoryJourneyRepository()
        self.session_repository = InMemorySessionRepository()
        self.ai_service = MockCompassAIService()
        self.journey_service = JourneyService(self.journey_repository)
        self.session_service = SessionService(self.session_repository)
        self.onboarding_service = OnboardingService(self.journey_service, self.session_repository)


@lru_cache
def get_container() -> ServiceContainer:
    return ServiceContainer()
