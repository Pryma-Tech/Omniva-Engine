# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/api/routes/strategy.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/strategy with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/strategy with cognitive telemetry.

from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter(prefix="/strategy", tags=["strategy"])


@router.get("/project/{project_id}")
async def project_strategy(project_id: int):
    return registry.strategy.generate_for_project(project_id)


@router.get("/map")
async def global_map():
    return registry.strategy.global_emergent_map()
