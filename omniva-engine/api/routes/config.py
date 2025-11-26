"""Configuration routes for Omniva Engine."""
# TODO: Serve runtime configuration and secrets management.

from fastapi import APIRouter

from config.config_manager import ConfigManager
from config.settings import settings


router = APIRouter()


@router.get("/")
async def read_config() -> dict:
    """Return sanitized configuration details (placeholder)."""
    return {
        "app": settings.APP_NAME,
        "env": settings.ENV,
        "message": "TODO: expand configuration endpoint",
    }


@router.get("/runtime")
async def get_runtime_config() -> dict:
    """
    Get runtime configuration.
    TODO: Add real data.
    """
    return settings.dict()


@router.get("/secrets")
async def get_secrets() -> dict:
    """
    Get secrets placeholder.
    """
    return settings.load_secrets()


@router.post("/secrets")
async def update_secrets(data: dict) -> dict:
    """
    Update secrets placeholder.
    TODO: Validate and secure secrets.
    """
    manager = ConfigManager(settings.SECRETS_FILE)
    manager.save(data)
    return {"status": "updated (placeholder)"}


@router.get("/project-config")
async def get_project_config() -> dict:
    """Retrieve stored project configuration."""
    manager = ConfigManager()
    return manager.load()


@router.post("/project-config")
async def save_project_config(data: dict) -> dict:
    """Save project configuration."""
    manager = ConfigManager()
    return manager.save(data)
