"""Pantheon governance API routes."""

from fastapi import APIRouter, Depends, Request

from app.core.registry import registry

router = APIRouter(prefix="/pantheon", tags=["pantheon"])


async def halo_pantheon_guard(request: Request) -> None:
    await registry.guard.require(request, "nexus")


@router.get("/consensus", dependencies=[Depends(halo_pantheon_guard)])
async def consensus():
    return registry.pantheon.compute_consensus()


@router.post("/weight/{name}", dependencies=[Depends(halo_pantheon_guard)])
async def set_weight(name: str, weight: float):
    return registry.pantheon.adjust_weight(name, weight)


@router.get("/snapshot", dependencies=[Depends(halo_pantheon_guard)])
async def snapshot():
    return registry.pantheon.pantheon_snapshot()
