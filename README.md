# Compass

AI-powered guide for navigating US government processes, built with a FastAPI backend designed for future Supabase and Gemini integrations.

## Backend Overview

This repository now includes a production-style FastAPI backend for Compass with:

- FastAPI on Python 3.11+
- Pydantic v2 schemas
- In-memory repositories for journeys and sessions, with optional Supabase-backed repositories
- Deterministic onboarding and mock grounded Q&A flows
- CORS configured for local frontend development
- UUID-based identifiers throughout

The app runs directly from the repository root with:

```bash
uvicorn app.main:app --reload
```

## File Tree

```text
.
├── README.md
├── requirements.txt
├── .env.example
└── app
    ├── __init__.py
    ├── main.py
    ├── api
    │   ├── __init__.py
    │   └── routes.py
    ├── core
    │   ├── __init__.py
    │   ├── config.py
    │   ├── dependencies.py
    │   ├── exceptions.py
    │   └── utils.py
    ├── repositories
    │   ├── __init__.py
    │   ├── base.py
    │   └── memory.py
    ├── rules
    │   ├── __init__.py
    │   ├── knowledge_base.py
    │   └── routing.py
    ├── schemas
    │   ├── __init__.py
    │   ├── common.py
    │   ├── journey.py
    │   ├── onboarding.py
    │   └── session.py
    └── services
        ├── __init__.py
        ├── ai_service.py
        ├── journey_builder.py
        ├── journey_service.py
        ├── onboarding_service.py
        ├── presenters.py
        └── session_service.py
```

## Quick Start

1. Create and activate a Python 3.11+ virtual environment.
2. Install dependencies.
3. Copy `.env.example` to `.env` if you want to customize settings.
4. Start the API server.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Once the server is running:

- API base URL: `http://127.0.0.1:8000`
- OpenAPI docs: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

## Environment Variables

`.env.example` includes the current settings used by the backend:

- `APP_NAME`: API display name
- `APP_ENV`: environment label returned by `/health`
- `APP_DEBUG`: FastAPI debug mode
- `API_V1_PREFIX`: reserved for versioned API configuration
- `ALLOWED_ORIGINS`: JSON array of local frontend origins allowed by CORS
- `GEMINI_API_KEY`: reserved for future Gemini integration
- `GEMINI_MODEL`: default Gemini model name for future use
- `DATA_BACKEND`: `memory` or `supabase`
- `SUPABASE_URL`: Supabase project HTTPS URL
- `SUPABASE_ANON_KEY`: optional public key
- `SUPABASE_SERVICE_KEY`: recommended server-side key for backend persistence
- `SUPABASE_JOURNEYS_TABLE`: table used for journey records
- `SUPABASE_SESSIONS_TABLE`: table used for session records
- `SUPABASE_PAYLOAD_COLUMN`: JSON column used to store the serialized record
- `POSTGRES_DSN`: reserved for future direct PostgreSQL access

## API Endpoints

### `GET /health`

Simple health response:

```json
{
  "status": "ok",
  "environment": "development"
}
```

### `POST /api/v1/onboard`

Creates a journey and session from onboarding answers.

Example request:

```json
{
  "state": "Georgia",
  "county": "Fulton",
  "city": "Atlanta",
  "language": "en",
  "goal": "ga_drivers_license",
  "age": 24,
  "has_ssn": true,
  "has_us_license": false,
  "has_foreign_license": true,
  "foreign_license_country": "Brazil",
  "immigration_status": "F-1 student"
}
```

### `GET /api/v1/journeys/{journey_id}`

Returns the full journey, including steps and progress summary.

### `POST /api/v1/journeys/{journey_id}/ask`

Accepts a follow-up question and stores a user/assistant turn in the session.

Example request:

```json
{
  "question": "Can I use a foreign license while I wait for the Georgia appointment?"
}
```

### `PATCH /api/v1/journeys/{journey_id}/progress`

Updates checklist completion state for a single step.

Example request:

```json
{
  "step_id": "11111111-1111-1111-1111-111111111111",
  "completed": true
}
```

### `GET /api/v1/sessions/{journey_id}`

Returns the in-memory session history for a journey.

## Current Behavior

- Launch journeys are included for Georgia driver's license, US passport, and visa-related flows from the product brief.
- Onboarding branches users into realistic mock journeys based on their answers.
- Follow-up answers are grounded in the stored journey context and add cautionary language for immigration-sensitive topics.
- By default, data is stored only in memory, so restarting the server resets all journeys and sessions.

## Supabase Mode

To enable Supabase-backed persistence:

1. Set `DATA_BACKEND="supabase"` in `.env`.
2. Set `SUPABASE_URL` to your project URL, for example `https://your-project-ref.supabase.co`.
3. Set `SUPABASE_SERVICE_KEY` for server-side access.
4. Make sure your Supabase tables match the configured names.

The current repository layer expects:

- A `journeys` table with an `id` text-or-uuid primary key column and a `payload` JSON/JSONB column.
- A `sessions` table with `id`, `journey_id`, and `payload` columns, where `journey_id` is unique for each journey session.

Each row stores the full serialized Pydantic record in the configured payload column, which keeps the backend schema simple and lets the FastAPI models remain the source of truth.

## Future Integration Path

The codebase is organized so you can keep using the current API routes and services while switching between in-memory and Supabase-backed repositories through configuration.
