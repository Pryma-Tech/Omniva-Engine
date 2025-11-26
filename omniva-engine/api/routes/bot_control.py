"""Bot control endpoints for Omniva Engine."""
# TODO: Expose bot start, stop, and status controls.

from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def get_bot_status() -> dict:
    """Report current automation bot status (placeholder)."""
    return {"message": "TODO: report bot status"}
