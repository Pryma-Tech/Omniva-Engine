"""Safety subsystem API routes (placeholder)."""

from fastapi import APIRouter

router = APIRouter(prefix="/safety", tags=["safety"])


@router.get("/")
async def safety_placeholder() -> dict:
    """
    TODO: Implement concrete safety endpoints.
    """
    return {"status": "safety routes not yet implemented"}
