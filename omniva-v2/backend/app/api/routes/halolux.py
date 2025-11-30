"""HaloLux interpretability API routes."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/api/routes/halolux.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/halolux with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/halolux with cognitive telemetry.


from fastapi import APIRouter, Depends, Request

from app.core.registry import registry

router = APIRouter(prefix="/halolux", tags=["halolux"])


async def halo_halolux_guard(request: Request) -> None:
    await registry.guard.require(request, "nexus")


@router.get("/illuminate", dependencies=[Depends(halo_halolux_guard)])
async def illuminate():
    return registry.halolux.illuminate()


@router.get("/explain/{project_id}", dependencies=[Depends(halo_halolux_guard)])
async def explain(project_id: int):
    return registry.halolux.explain_decision(project_id)


@router.get("/snapshot", dependencies=[Depends(halo_halolux_guard)])
async def snapshot():
    return registry.halolux.halolux_snapshot()
