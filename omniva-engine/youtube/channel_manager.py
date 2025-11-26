"""High-level orchestration for YouTube channel setup."""
# TODO: Wire together naming, branding, and API logic.

from utils.logger import logger
from branding.branding_manager import BrandingManager
from .channel_setup import YouTubeChannelSetup


class ChannelManager:
    """Coordinate placeholder channel setup activities."""

    def __init__(self):
        self.branding = BrandingManager()
        self.setup = YouTubeChannelSetup()

    def setup_new_channel(self, keywords: list) -> dict:
        """Orchestrate placeholder channel creation + branding."""
        names = self.branding.generate_channel_names(keywords)
        chosen = names[0] if names else "default_channel"
        logger.info("Chosen placeholder channel name: %s", chosen)
        channel = self.setup.create_channel(chosen, "TODO: description")
        prompts = self.branding.generate_branding_prompts(chosen)
        return {
            "chosen_name": chosen,
            "channel_info": channel,
            "branding_prompts": prompts,
            "status": "channel setup (placeholder)",
        }
