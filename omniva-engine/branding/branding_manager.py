"""Branding subsystem manager."""
# TODO: Integrate with image generation API (SDXL).

import os

from utils.logger import logger
from utils.storage import storage_manager

from .channel_name_generator import ChannelNameGenerator
from .prompt_generator import PromptGenerator


class BrandingManager:
    """Coordinate branding-related helpers and storage paths."""

    def __init__(self):
        self.name_gen = ChannelNameGenerator()
        self.prompt_gen = PromptGenerator()
        logger.info("BrandingManager initialized (placeholder).")

    def generate_channel_names(self, keywords: list):
        """Return placeholder channel names."""
        return self.name_gen.generate_names(keywords)

    def generate_branding_prompts(self, channel_name: str) -> dict:
        """Return logo and banner prompts."""
        return {
            "logo_prompt": self.prompt_gen.generate_logo_prompt(channel_name),
            "banner_prompt": self.prompt_gen.generate_banner_prompt(channel_name),
        }

    def branding_asset_paths(self, project_id: int) -> dict:
        """Return placeholder storage paths for branding assets."""
        base = storage_manager.project_dir(project_id)
        return {
            "logo": os.path.join(base, "logo.png"),
            "banner": os.path.join(base, "banner.png"),
        }
