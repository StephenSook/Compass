from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import ServiceContainer, get_container
from app.core.exceptions import InvalidProgressUpdateError, JourneyNotFoundError
from app.schemas.journey import JourneyResponse, ProgressUpdateRequest, ProgressUpdateResponse
from app.schemas.onboarding import OnboardRequest, OnboardResponse
from app.schemas.session import AskJourneyRequest, AskJourneyResponse, SessionResponse

router = APIRouter(prefix="/api/v1", tags=["Compass"])


@router.post("/onboard", response_model=OnboardResponse, status_code=status.HTTP_201_CREATED)
def onboard(
    payload: OnboardRequest,
    container: ServiceContainer = Depends(get_container),
) -> OnboardResponse:
    return container.onboarding_service.onboard(payload)


@router.get("/journeys/{journey_id}", response_model=JourneyResponse)
def get_journey(
    journey_id: UUID,
    container: ServiceContainer = Depends(get_container),
) -> JourneyResponse:
    try:
        journey = container.journey_service.get_journey(journey_id)
    except JourneyNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return JourneyResponse(journey=journey)


@router.post("/journeys/{journey_id}/ask", response_model=AskJourneyResponse)
def ask_journey(
    journey_id: UUID,
    payload: AskJourneyRequest,
    container: ServiceContainer = Depends(get_container),
) -> AskJourneyResponse:
    try:
        journey = container.journey_service.get_journey(journey_id)
        session = container.session_service.get_session(journey_id)
    except JourneyNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    answer = container.ai_service.answer_question(journey=journey, session=session, question=payload.question)
    updated_session = container.session_service.append_conversation(journey_id, payload.question, answer)
    return AskJourneyResponse(
        journey_id=journey_id,
        session_id=updated_session.id,
        answer=answer,
        session=updated_session,
    )


@router.patch("/journeys/{journey_id}/progress", response_model=ProgressUpdateResponse)
def update_journey_progress(
    journey_id: UUID,
    payload: ProgressUpdateRequest,
    container: ServiceContainer = Depends(get_container),
) -> ProgressUpdateResponse:
    try:
        journey = container.journey_service.update_progress(journey_id, payload)
    except JourneyNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except InvalidProgressUpdateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return ProgressUpdateResponse(journey_id=journey_id, progress=journey.progress, journey=journey)


@router.get("/sessions/{journey_id}", response_model=SessionResponse)
def get_session(
    journey_id: UUID,
    container: ServiceContainer = Depends(get_container),
) -> SessionResponse:
    try:
        session = container.session_service.get_session(journey_id)
    except JourneyNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return SessionResponse(session=session)
