"""Configuration manager for Omniva Engine."""
# TODO: Add persistence, encryption, credential validation.

import json
import os

from utils.logger import logger


class ConfigManager:
    """Load and persist configuration payloads."""

    def __init__(self, path: str = "config/config.json") -> None:
        self.path = path
        logger.info("ConfigManager initialized for %s", path)

    def load(self) -> dict:
        """Load configuration from disk."""
        if not os.path.exists(self.path):
            logger.info("No config.json found (placeholder)")
            return {}
        with open(self.path, encoding="utf-8") as file:
            return json.load(file)

    def save(self, data: dict) -> dict:
        """Persist configuration to disk."""
        logger.info("Saving config (placeholder): %s", data)
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        return data
