"""Oracle foresight API routes."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/api/routes/oracle.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/oracle with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/oracle with cognitive telemetry.


from fastapi import APIRouter, Depends, Request

from app.core.registry import registry

router = APIRouter(prefix="/oracle", tags=["oracle"])


async def halo_oracle_guard(request: Request) -> None:
    await registry.guard.require(request, "nexus")


@router.get("/project/{project_id}", dependencies=[Depends(halo_oracle_guard)])
async def project_forecast(project_id: int):
    return registry.oracle.project_forecast(project_id)


@router.get("/resonance", dependencies=[Depends(halo_oracle_guard)])
async def resonance():
    return registry.oracle.global_resonance()


@router.get("/foresight", dependencies=[Depends(halo_oracle_guard)])
async def foresight():
    return registry.oracle.foresight_snapshot()
