from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.core.config import get_settings


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    debug=settings.app_debug,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "Health",
            "description": "Basic service health and readiness checks.",
        },
        {
            "name": "Compass",
            "description": "Onboarding, journeys, progress tracking, and contextual Q&A endpoints.",
        },
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"], summary="Health check", description="Simple readiness check.")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(api_router)
