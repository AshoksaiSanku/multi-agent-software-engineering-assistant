from functools import lru_cache
from pathlib import Path

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables."""

    project_name: str = "Multi-Agent AI Software Engineering Assistant"
    app_env: str = "development"
    api_prefix: str = "/api/v1"
    secret_key: str = "development-only-change-this-secret"
    access_token_expire_minutes: int = 1440
    database_url: str = "sqlite+aiosqlite:///./assistant.db"
    cors_origins: str = "http://localhost:5173"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    ai_provider: str = "local"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5-coder:1.5b"
    github_token: str | None = None
    chroma_path: Path = Path("./data/chroma")
    ml_model_path: Path = Path("./models")
    max_repository_files: int = 180
    rate_limit_per_minute: int = 120

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    def create_directories(self) -> None:
        self.chroma_path.mkdir(parents=True, exist_ok=True)
        self.ml_model_path.mkdir(parents=True, exist_ok=True)

    @model_validator(mode="after")
    def validate_production_secret(self) -> "Settings":
        if self.app_env == "production" and self.secret_key.startswith("development-only"):
            raise ValueError("SECRET_KEY must be replaced in production")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
