"""Paradox consistency API routes."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/api/routes/paradox.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/paradox with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/paradox with cognitive telemetry.


from fastapi import APIRouter, Depends, Request

from app.core.registry import registry

router = APIRouter(prefix="/paradox", tags=["paradox"])


async def halo_paradox_guard(request: Request) -> None:
    await registry.guard.require(request, "nexus")


@router.get("/check/{project_id}", dependencies=[Depends(halo_paradox_guard)])
async def check(project_id: int):
    return {
        "project": registry.paradox.check_project(project_id),
        "astral": registry.paradox.check_astral(project_id),
    }


@router.post("/reconcile/{project_id}", dependencies=[Depends(halo_paradox_guard)])
async def reconcile(project_id: int):
    return {
        "project": registry.paradox.reconcile_project(project_id),
        "astral": registry.paradox.reconcile_astral(project_id),
        "infinity": registry.paradox.reconcile_infinity(),
    }


@router.get("/snapshot", dependencies=[Depends(halo_paradox_guard)])
async def snapshot():
    return registry.paradox.paradox_snapshot()
