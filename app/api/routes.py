from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, status

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

ONBOARD_REQUEST_EXAMPLE = {
    "state": "GA",
    "county": "DeKalb",
    "city": "Atlanta",
    "language": "en",
    "goal": "ga_drivers_license",
    "immigration_status": "new_immigrant",
    "age": 23,
    "has_ssn": True,
    "has_us_license": False,
    "has_foreign_license": True,
    "foreign_license_country": "France",
}

ONBOARD_RESPONSE_EXAMPLE = {
    "user_id": "usr_123",
    "profile_id": "pro_123",
    "journey_id": "jrny_123",
    "journey_type": "ga_drivers_license",
    "branch_summary": {
        "license_path": "foreign_reciprocity_transfer",
        "testing_required": False,
        "ssn_path": "standard",
    },
    "next_action": "generate_journey",
}

JOURNEY_RESPONSE_EXAMPLE = {
    "journey_id": "jrny_123",
    "journey_type": "ga_drivers_license",
    "title": "Georgia Driver’s License",
    "status": "active",
    "progress": {
        "completed_steps": 2,
        "total_steps": 7,
        "percent": 29,
    },
    "steps": [
        {
            "step_id": "step_1",
            "order_index": 1,
            "title": "Gather documents",
            "action": "Bring passport, visa, I-94, SSN card, and two proofs of Georgia residency.",
            "documents": [
                "Passport",
                "Visa",
                "I-94 arrival record",
                "SSN card",
                "Utility bill",
                "Bank statement",
            ],
            "form_number": None,
            "form_url": None,
            "fee_usd": None,
            "office_name": None,
            "office_address": None,
            "office_hours": None,
            "estimated_time": "1 day to prepare",
            "tip": "Bring two residency proofs; one is often not enough.",
            "warning": None,
            "completed": False,
        }
    ],
    "disclaimer": "This tool provides guidance, not legal advice.",
}

ASK_REQUEST_EXAMPLE = {
    "question": "What if I don’t have a utility bill for proof of residency?"
}

ASK_RESPONSE_EXAMPLE = {
    "answer": (
        "You may still be able to prove residency with other accepted Georgia DDS documents "
        "such as a bank statement, lease, or official mail, depending on current DDS rules."
    ),
    "citations": [
        {
            "source_type": "knowledge_base",
            "source_key": "ga_dds_residency_docs",
        }
    ],
    "legal_warning": False,
    "recommended_next_step": "Review accepted residency document alternatives in Step 1.",
}

PROGRESS_REQUEST_EXAMPLE = {
    "step_id": "step_1",
    "completed": True,
}

PROGRESS_RESPONSE_EXAMPLE = {
    **JOURNEY_RESPONSE_EXAMPLE,
    "progress": {
        "completed_steps": 3,
        "total_steps": 7,
        "percent": 43,
    },
    "steps": [
        {
            **JOURNEY_RESPONSE_EXAMPLE["steps"][0],
            "completed": True,
        }
    ],
}

SESSION_RESPONSE_EXAMPLE = {
    "journey_id": "jrny_123",
    "profile_summary": {
        "state": "GA",
        "county": "DeKalb",
        "city": "Atlanta",
        "language": "en",
        "goal": "ga_drivers_license",
        "immigration_status": "new_immigrant",
        "age": 23,
        "has_ssn": True,
        "has_us_license": False,
        "has_foreign_license": True,
        "foreign_license_country": "France",
    },
    "journey": JOURNEY_RESPONSE_EXAMPLE,
    "chat_history": [
        {
            "role": "user",
            "content": "What if I don’t have a utility bill for proof of residency?",
        },
        {
            "role": "assistant",
            "content": ASK_RESPONSE_EXAMPLE["answer"],
        },
    ],
}


@router.post(
    "/onboard",
    response_model=OnboardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create onboarding journey",
    description=(
        "Validate onboarding input, route the user deterministically, create a journey, "
        "persist checklist steps, and return the routing summary."
    ),
    responses={
        status.HTTP_201_CREATED: {
            "description": "Onboarding result with the routed journey summary.",
            "content": {
                "application/json": {
                    "example": ONBOARD_RESPONSE_EXAMPLE,
                }
            },
        }
    },
)
def onboard(
    payload: Annotated[
        OnboardRequest,
        Body(
            openapi_examples={
                "ga_foreign_license_transfer": {
                    "summary": "Georgia onboarding for a foreign license holder",
                    "description": (
                        "Demo payload for a new immigrant in Atlanta transferring from "
                        "an eligible foreign driver's license path."
                    ),
                    "value": ONBOARD_REQUEST_EXAMPLE,
                }
            }
        ),
    ],
    container: ServiceContainer = Depends(get_container),
) -> OnboardResponse:
    journey = container.onboarding_service.onboard(payload)
    return present_onboard_response(journey)


@router.get(
    "/journeys/{journey_id}",
    response_model=JourneyOut,
    summary="Get journey",
    description="Load a stored journey, recompute progress from saved steps, and return the checklist view.",
    responses={
        status.HTTP_200_OK: {
            "description": "Journey checklist with current progress and step details.",
            "content": {
                "application/json": {
                    "example": JOURNEY_RESPONSE_EXAMPLE,
                }
            },
        }
    },
)
def get_journey(
    journey_id: UUID,
    container: ServiceContainer = Depends(get_container),
) -> JourneyOut:
    try:
        journey = container.journey_service.get_journey(journey_id)
    except JourneyNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return present_journey(journey)


@router.post(
    "/journeys/{journey_id}/ask",
    response_model=AskResponse,
    summary="Ask journey question",
    description=(
        "Generate a contextual mock answer using journey type, step context, profile details, "
        "and question keywords, then append the exchange to session history."
    ),
    responses={
        status.HTTP_200_OK: {
            "description": "Grounded answer with citations and a suggested next step.",
            "content": {
                "application/json": {
                    "example": ASK_RESPONSE_EXAMPLE,
                }
            },
        }
    },
)
def ask_journey(
    journey_id: UUID,
    payload: Annotated[
        AskRequest,
        Body(
            openapi_examples={
                "residency_proof_question": {
                    "summary": "Residency proof follow-up",
                    "description": "Ask a practical question about acceptable Georgia residency documents.",
                    "value": ASK_REQUEST_EXAMPLE,
                }
            }
        ),
    ],
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


@router.patch(
    "/journeys/{journey_id}/progress",
    response_model=JourneyOut,
    summary="Update step progress",
    description="Update a single step completion state and return the refreshed journey progress summary.",
    responses={
        status.HTTP_200_OK: {
            "description": "Updated journey after marking one step complete or incomplete.",
            "content": {
                "application/json": {
                    "example": PROGRESS_RESPONSE_EXAMPLE,
                }
            },
        }
    },
)
def update_journey_progress(
    journey_id: UUID,
    payload: Annotated[
        ProgressUpdateRequest,
        Body(
            openapi_examples={
                "complete_first_step": {
                    "summary": "Mark a step complete",
                    "description": "Toggle the first checklist step to completed.",
                    "value": PROGRESS_REQUEST_EXAMPLE,
                }
            }
        ),
    ],
    container: ServiceContainer = Depends(get_container),
) -> JourneyOut:
    try:
        journey = container.journey_service.update_progress(journey_id, payload)
    except JourneyNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except InvalidProgressUpdateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return present_journey(journey)


@router.get(
    "/sessions/{journey_id}",
    response_model=SessionOut,
    summary="Get session context",
    description="Return the profile summary, current journey view, and stored chat history for a journey.",
    responses={
        status.HTTP_200_OK: {
            "description": "Session context for the journey, including journey snapshot and chat history.",
            "content": {
                "application/json": {
                    "example": SESSION_RESPONSE_EXAMPLE,
                }
            },
        }
    },
)
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
