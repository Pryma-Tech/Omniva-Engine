"""Infinity elastic autoscaling API routes."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/api/routes/infinity.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/infinity with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/infinity with cognitive telemetry.


from fastapi import APIRouter, Depends, Request

from app.core.registry import registry

router = APIRouter(prefix="/infinity", tags=["infinity"])


async def halo_infinity_guard(request: Request) -> None:
    await registry.guard.require(request, "nexus")


@router.get("/load", dependencies=[Depends(halo_infinity_guard)])
async def load():
    return {"load_score": registry.infinity.compute_current_load()}


@router.post("/scale", dependencies=[Depends(halo_infinity_guard)])
async def scale():
    return registry.infinity.scale_cycle()


@router.get("/snapshot", dependencies=[Depends(halo_infinity_guard)])
async def snapshot():
    return registry.infinity.infinity_snapshot()
