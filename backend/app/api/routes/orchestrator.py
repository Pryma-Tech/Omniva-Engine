"""Master orchestrator API routes."""

from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter(prefix="/orchestrator", tags=["orchestrator"])


@router.post("/start_all")
async def orchestrator_start() -> dict:
    return registry.orchestrator.start_all()


@router.post("/stop_all")
async def orchestrator_stop() -> dict:
    return registry.orchestrator.stop_all()


@router.get("/cycle")
async def orchestrator_cycle() -> dict:
    return registry.orchestrator.global_cycle()


@router.get("/health")
async def orchestrator_health() -> dict:
    return registry.health.system_health()
