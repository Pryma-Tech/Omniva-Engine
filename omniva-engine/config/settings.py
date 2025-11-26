"""Settings module for Omniva Engine."""
# TODO: Load real secrets, API keys, and runtime configurations.

import json
import os

from pydantic import BaseSettings

from utils.logger import logger


class Settings(BaseSettings):
    """Application configuration loaded from the environment."""

    APP_NAME: str = "Omniva Engine"
    ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "info"
    DATA_DIR: str = "static"
    SECRETS_FILE: str = "config/secrets.json"

    class Config:
        env_file = ".env"

    def load_secrets(self) -> dict:
        """
        Load secret keys from JSON template.
        TODO: Add real secret handling + validation.
        """
        logger.info("Loading secrets (placeholder)")
        if not os.path.exists(self.SECRETS_FILE):
            return {}
        with open(self.SECRETS_FILE, encoding="utf-8") as file:
            return json.load(file)


settings = Settings()
