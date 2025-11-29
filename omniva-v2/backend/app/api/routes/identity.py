# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/api/routes/identity.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/identity with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/identity with cognitive telemetry.

from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter(prefix="/identity", tags=["identity"])


@router.get("/")
async def get_identity():
    return registry.selfmodel.get_identity()


@router.post("/recompute")
async def recompute_identity():
    registry.selfmodel.recompute_identity()
    return registry.selfmodel.get_identity()
