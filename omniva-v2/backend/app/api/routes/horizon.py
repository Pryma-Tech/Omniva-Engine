"""Horizon long-horizon vision API routes."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/api/routes/horizon.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/horizon with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/horizon with cognitive telemetry.


from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from app.core.registry import registry

router = APIRouter(prefix="/horizon", tags=["horizon"])


class GoalRequest(BaseModel):
    goals: dict


class VisionAdjustRequest(BaseModel):
    weights: dict


async def halo_horizon_guard(request: Request) -> None:
    await registry.guard.require(request, "nexus")


@router.post("/epoch-goal", dependencies=[Depends(halo_horizon_guard)])
async def set_epoch_goals(body: GoalRequest):
    return registry.horizon.set_epoch_goal(body.goals)


@router.get("/epoch-goal", dependencies=[Depends(halo_horizon_guard)])
async def get_epoch_goals():
    return registry.horizon.get_epoch_goal()


@router.get("/vision", dependencies=[Depends(halo_horizon_guard)])
async def vision():
    return registry.horizon.vision()


@router.get("/alignment", dependencies=[Depends(halo_horizon_guard)])
async def alignment():
    return registry.horizon.alignment_report()


@router.post("/vision-adjust", dependencies=[Depends(halo_horizon_guard)])
async def adjust_vision(body: VisionAdjustRequest):
    return registry.horizon.adjust_vision(body.weights)


@router.get("/snapshot", dependencies=[Depends(halo_horizon_guard)])
async def snapshot():
    return registry.horizon.horizon_snapshot()
