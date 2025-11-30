"""Federated intelligence API routes."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/api/routes/federation.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/federation with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/federation with cognitive telemetry.


from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter(prefix="/federation", tags=["federation"])


@router.get("/shared")
async def get_shared() -> dict:
    return registry.federation.shared_heuristics or {}
