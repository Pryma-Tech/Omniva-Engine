"""YouTube Channel Setup (Placeholder)."""
# TODO: Integrate OAuth flow, channel creation, branding uploads.

from utils.logger import logger


class YouTubeChannelSetup:
    """Placeholder helper for YouTube channel creation workflows."""

    def __init__(self):
        logger.info("YouTubeChannelSetup initialized (placeholder).")

    def create_channel(self, name: str, description: str = "") -> dict:
        """Return dummy object representing channel creation."""
        logger.info("(Placeholder) Creating YouTube channel: %s", name)
        return {
            "channel_id": "placeholder_channel_id",
            "name": name,
            "description": description,
            "status": "created (placeholder)",
        }

    def apply_branding(self, channel_id: str, logo_path: str, banner_path: str) -> dict:
        """Placeholder method for branding uploads."""
        logger.info("(Placeholder) Applying branding to channel %s", channel_id)
        return {
            "channel_id": channel_id,
            "logo": logo_path,
            "banner": banner_path,
            "status": "branding applied (placeholder)",
        }

    def set_channel_config(self, channel_id: str, config: dict) -> dict:
        """Placeholder configuration setter."""
        logger.info("(Placeholder) Setting config for channel %s", channel_id)
        return {
            "channel_id": channel_id,
            "config": config,
            "status": "config applied (placeholder)",
        }
