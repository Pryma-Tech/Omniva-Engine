"""Branding routes for Omniva Engine."""
# TODO: Add authentication, persistence, and image generation integration.

from fastapi import APIRouter

from branding.branding_manager import BrandingManager

router = APIRouter()
manager = BrandingManager()


@router.get("/names")
async def get_channel_names(keywords: str = ""):
    """Return placeholder channel names based on keywords."""
    kws = [k.strip() for k in keywords.split(",") if k.strip()]
    return manager.generate_channel_names(kws)


@router.get("/prompts/{channel_name}")
async def get_prompts(channel_name: str):
    """Return placeholder prompts for branding assets."""
    return manager.generate_branding_prompts(channel_name)


@router.get("/assets/{project_id}")
async def asset_paths(project_id: int):
    """Return placeholder asset paths for a project."""
    return manager.branding_asset_paths(project_id)
