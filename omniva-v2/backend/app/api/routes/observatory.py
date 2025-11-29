"""Observatory analytics API routes."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/api/routes/observatory.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/observatory with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/observatory with cognitive telemetry.


from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter(prefix="/observatory", tags=["observatory"])


@router.get("/insights")
async def insights() -> dict:
    """Expose consolidated observatory insights."""
    return registry.observatory.gather()
