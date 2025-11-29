from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter(prefix="/strategy", tags=["strategy"])


@router.get("/project/{project_id}")
async def project_strategy(project_id: int):
    return registry.strategy.generate_for_project(project_id)


@router.get("/map")
async def global_map():
    return registry.strategy.global_emergent_map()
