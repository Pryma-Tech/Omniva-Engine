"""Settings module for Omniva Engine."""
# TODO: Describe environment variables and defaults.

from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from the environment."""

    APP_NAME: str = "Omniva Engine"
    ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "info"
    # TODO: Add API tokens, database URLs, and other secret settings.

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance for reuse."""
    return Settings()
