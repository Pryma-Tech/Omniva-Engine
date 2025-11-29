"""Astral multi-world futures API routes."""

from fastapi import APIRouter, Depends, Request

from app.core.registry import registry

router = APIRouter(prefix="/astral", tags=["astral"])


async def halo_astral_guard(request: Request) -> None:
    await registry.guard.require(request, "nexus")


@router.get("/project/{project_id}", dependencies=[Depends(halo_astral_guard)])
async def future_branches(project_id: int):
    return registry.astral.alternate_futures(project_id)


@router.get("/snapshot", dependencies=[Depends(halo_astral_guard)])
async def snapshot():
    return registry.astral.astral_snapshot()
