"""Lattice semantic fabric API routes."""

from fastapi import APIRouter, Depends, Request

from app.core.registry import registry

router = APIRouter(prefix="/lattice", tags=["lattice"])


async def halo_lattice_guard(request: Request) -> None:
    await registry.guard.require(request, "nexus")


@router.post("/update/{project_id}", dependencies=[Depends(halo_lattice_guard)])
async def update(project_id: int):
    return registry.lattice.update_project(project_id)


@router.get("/trace/{node_id}", dependencies=[Depends(halo_lattice_guard)])
async def trace(node_id: str):
    return registry.lattice.context_trace(node_id)


@router.get("/snapshot", dependencies=[Depends(halo_lattice_guard)])
async def snapshot():
    return registry.lattice.lattice_snapshot()
