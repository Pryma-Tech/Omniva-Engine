"""Zenith meta-layer API routes."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/api/routes/zenith.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/zenith with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/zenith with cognitive telemetry.


from fastapi import APIRouter, Depends, Request

from app.core.registry import registry

router = APIRouter(prefix="/zenith", tags=["zenith"])


async def halo_zenith_guard(request: Request) -> None:
    await registry.guard.require(request, "sanctum")


@router.get("/coherence", dependencies=[Depends(halo_zenith_guard)])
async def coherence():
    return registry.zenith.coherence_score()


@router.get("/reflect", dependencies=[Depends(halo_zenith_guard)])
async def reflect():
    return registry.zenith.reflection_report()


@router.get("/snapshot", dependencies=[Depends(halo_zenith_guard)])
async def snapshot():
    return registry.zenith.zenith_snapshot()
