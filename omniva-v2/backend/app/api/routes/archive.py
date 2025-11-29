# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/api/routes/archive.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/archive with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/archive with cognitive telemetry.

from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter(prefix="/archive", tags=["archive"])


@router.get("/timeline")
async def timeline():
    return registry.archive.timeline[-200:]


@router.get("/epochs")
async def epochs():
    return registry.archive.epochs


@router.get("/summary")
async def summary():
    return registry.archive.summary()
