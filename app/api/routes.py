from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import ServiceContainer, get_container
from app.core.exceptions import InvalidProgressUpdateError, JourneyNotFoundError
from app.schemas.journey import JourneyOut, ProgressUpdateRequest
from app.schemas.onboarding import OnboardRequest, OnboardResponse
from app.schemas.session import AskRequest, AskResponse, SessionOut
from app.services.presenters import (
    present_ask_response,
    present_journey,
    present_onboard_response,
    present_session,
)

router = APIRouter(prefix="/api/v1", tags=["Compass"])


@router.post("/onboard", response_model=OnboardResponse, status_code=status.HTTP_201_CREATED)
def onboard(
    payload: OnboardRequest,
    container: ServiceContainer = Depends(get_container),
) -> OnboardResponse:
    journey = container.onboarding_service.onboard(payload)
    return present_onboard_response(journey)


@router.get("/journeys/{journey_id}", response_model=JourneyOut)
def get_journey(
    journey_id: UUID,
    container: ServiceContainer = Depends(get_container),
) -> JourneyOut:
    try:
        journey = container.journey_service.get_journey(journey_id)
    except JourneyNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return present_journey(journey)


@router.post("/journeys/{journey_id}/ask", response_model=AskResponse)
def ask_journey(
    journey_id: UUID,
    payload: AskRequest,
    container: ServiceContainer = Depends(get_container),
) -> AskResponse:
    try:
        journey = container.journey_service.get_journey(journey_id)
        session = container.session_service.get_session(journey_id)
    except JourneyNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    answer = container.ai_service.answer_question(journey=journey, session=session, question=payload.question)
    container.session_service.append_conversation(journey_id, payload.question, answer)
    return present_ask_response(
        answer=answer,
        citations=container.ai_service.build_citations(journey),
        legal_warning=container.ai_service.needs_legal_caution(journey, payload.question),
        recommended_next_step=container.ai_service.recommended_next_step(journey),
    )


@router.patch("/journeys/{journey_id}/progress", response_model=JourneyOut)
def update_journey_progress(
    journey_id: UUID,
    payload: ProgressUpdateRequest,
    container: ServiceContainer = Depends(get_container),
) -> JourneyOut:
    try:
        journey = container.journey_service.update_progress(journey_id, payload)
    except JourneyNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except InvalidProgressUpdateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return present_journey(journey)


@router.get("/sessions/{journey_id}", response_model=SessionOut)
def get_session(
    journey_id: UUID,
    container: ServiceContainer = Depends(get_container),
) -> SessionOut:
    try:
        journey = container.journey_service.get_journey(journey_id)
        session = container.session_service.get_session(journey_id)
    except JourneyNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return present_session(journey, session)
