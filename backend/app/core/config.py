from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Compass API"
    app_env: str = "development"
    app_debug: bool = True
    api_v1_prefix: str = "/api/v1"
    allowed_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]
    )
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"
    data_backend: Literal["memory", "supabase"] = "memory"
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_key: str = ""
    supabase_journeys_table: str = "journeys"
    supabase_sessions_table: str = "sessions"
    supabase_payload_column: str = "payload"
    postgres_dsn: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
