from __future__ import annotations

from app.core.utils import new_uuid, utc_now
from app.repositories.base import JourneyRepository, SessionRepository
from app.rules.knowledge_base import get_journey_template
from app.rules.routing import build_session_title, route_onboarding
from app.schemas.common import ChatRoleEnum, JourneyRecord, SessionRecord, SessionTurn, UserProfile
from app.schemas.onboarding import OnboardRequest
from app.services.journey_builder import build_journey_record


class OnboardingService:
    def __init__(self, journey_repository: JourneyRepository, session_repository: SessionRepository) -> None:
        self.journey_repository = journey_repository
        self.session_repository = session_repository

    def onboard(self, payload: OnboardRequest) -> JourneyRecord:
        profile = UserProfile(**payload.model_dump())
        routing = route_onboarding(profile)
        user_id = new_uuid()
        profile_id = new_uuid()
        session_id = new_uuid()
        template = get_journey_template(routing.template_key)
        journey = build_journey_record(user_id, profile_id, session_id, routing, profile, template)
        self.journey_repository.create(journey)

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
