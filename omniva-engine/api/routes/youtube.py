"""YouTube channel setup routes (placeholder)."""
# TODO: Add authentication, OAuth callbacks, and persistence.

from fastapi import APIRouter

from youtube.channel_manager import ChannelManager

router = APIRouter()
manager = ChannelManager()


@router.get("/setup")
async def setup_channel(keywords: str = ""):
    """Trigger placeholder channel setup flow."""
    kws = [k.strip() for k in keywords.split(",") if k.strip()]
    return manager.setup_new_channel(kws)


@router.post("/branding")
async def apply_branding(data: dict):
    """Placeholder API to apply branding to an existing channel."""
    setup = manager.setup
    return setup.apply_branding(
        data.get("channel_id"),
        data.get("logo_path"),
        data.get("banner_path"),
    )
