"""Infinity elastic autoscaling API routes."""

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
