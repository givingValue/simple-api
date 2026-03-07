"""Application configuration loaded from environment variables."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_env_path = Path(__file__).resolve().parent / ".env"


class Settings(BaseSettings):
    """Application settings with sensible defaults."""

    model_config = SettingsConfigDict(
        env_file=str(_env_path),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False

    # API
    api_prefix: str = "/api/v1"
    debug: bool = False

    # Optional: CORS origins (comma-separated)
    cors_origins: str = "*"


settings = Settings()
