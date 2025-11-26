"""Configuration routes for Omniva Engine."""
# TODO: Serve runtime configuration and secrets management.

from fastapi import APIRouter

from config.settings import get_settings


router = APIRouter()
settings = get_settings()


@router.get("/")
async def read_config() -> dict:
    """Return sanitized configuration details (placeholder)."""
    return {
        "app": settings.APP_NAME,
        "env": settings.ENV,
        "message": "TODO: expand configuration endpoint",
    }
