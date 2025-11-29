"""Observatory analytics API routes."""

from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter(prefix="/observatory", tags=["observatory"])


@router.get("/insights")
async def insights() -> dict:
    """Expose consolidated observatory insights."""
    return registry.observatory.gather()
