"""Stable Diffusion prompt generator (placeholder)."""
# TODO: Implement dynamic prompt creation for branding assets.

from utils.logger import logger


class PromptGenerator:
    """Generate placeholder prompts for branding assets."""

    def generate_logo_prompt(self, channel_name: str) -> str:
        logger.info("Generating placeholder logo prompt...")
        return f"Logo for YouTube channel '{channel_name}' in modern minimalist style"

    def generate_banner_prompt(self, channel_name: str) -> str:
        logger.info("Generating placeholder banner prompt...")
        return f"Channel banner featuring '{channel_name}' with clean futuristic design"
