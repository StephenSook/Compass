from __future__ import annotations

from app.core.utils import new_uuid, utc_now
from app.repositories.base import SessionRepository
from app.rules.routing import build_session_title, route_onboarding
from app.schemas.common import ChatRoleEnum, JourneyRecord, SessionRecord, SessionTurn, UserProfile
from app.schemas.onboarding import OnboardRequest
from app.services.journey_service import JourneyService


class OnboardingService:
    def __init__(self, journey_service: JourneyService, session_repository: SessionRepository) -> None:
        self.journey_service = journey_service
        self.session_repository = session_repository

    def onboard(self, payload: OnboardRequest) -> JourneyRecord:
        profile = UserProfile(**payload.model_dump())
        routing = route_onboarding(profile)
        user_id = new_uuid()
        profile_id = new_uuid()
        session_id = new_uuid()
        journey = self.journey_service.create_journey(
            user_id=user_id,
            profile_id=profile_id,
            session_id=session_id,
            profile=profile,
            routing=routing,
        )

        timestamp = utc_now()
        session = SessionRecord(
            id=session_id,
            journey_id=journey.id,
            title=build_session_title(profile, routing.branch_key),
            turns=[
                SessionTurn(
                    id=new_uuid(),
                    role=ChatRoleEnum.SYSTEM,
                    message=(
                        f"Journey created for {journey.title}. The user goal is '{profile.goal}' "
                        f"and the current branch is '{routing.branch_key}'."
                    ),
                    created_at=timestamp,
                )
            ],
            created_at=timestamp,
            updated_at=timestamp,
        )
        self.session_repository.create(session)
        return journey
