"""Master orchestrator API routes."""

from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter(prefix="/orchestrator", tags=["orchestrator"])


@router.post("/start_all")
async def orchestrator_start() -> dict:
    # TODO(omniva-v0.1): Require project scope and authorization context.
    # TODO(omniva-v0.2): Provide async job tracking for long-running start ops.
    return registry.orchestrator.start_all()


@router.post("/stop_all")
async def orchestrator_stop() -> dict:
    # TODO(omniva-v0.1): Allow selective stop via payload filters.
    # TODO(omniva-v0.2): Notify dashboard via websocket when stop completes.
    return registry.orchestrator.stop_all()


@router.get("/cycle")
async def orchestrator_cycle() -> dict:
    # TODO(omniva-v0.1): Support streaming/long-poll updates for continuous cycles.
    # TODO(omniva-v0.2): Cache results for short intervals to reduce load.
    return registry.orchestrator.global_cycle()


@router.get("/health")
async def orchestrator_health() -> dict:
    # TODO(omniva-v0.1): Include worker-level stats and queue depths.
    # TODO(omniva-v0.2): Add ability to filter by project or subsystem.
    return registry.health.system_health()
