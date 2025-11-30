"""Master orchestrator API routes."""

from __future__ import annotations

import asyncio
import json
from typing import List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query, Response
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

from app.api.deps import parse_project_scope, require_control_token
from app.core.registry import registry

router = APIRouter(prefix="/orchestrator", tags=["orchestrator"])


class StopPayload(BaseModel):
    project_ids: Optional[List[int]] = None
    drain: bool = True


def _orchestrator():
    orchestrator = getattr(registry, "orchestrator", None)
    if orchestrator is None:
        raise HTTPException(status_code=503, detail="orchestrator unavailable")
    return orchestrator


@router.post("/start_all")
async def orchestrator_start(
    _: str = Depends(require_control_token),
    project_scope: List[int] | None = Depends(parse_project_scope),
) -> dict:
    """Start all (or scoped) projects via the orchestrator."""
    orchestrator = _orchestrator()
    return orchestrator.start_all(project_scope)


@router.post("/stop_all")
async def orchestrator_stop(
    payload: StopPayload = Body(default=StopPayload()),
    _: str = Depends(require_control_token),
) -> dict:
    """Stop all (or filtered) projects with optional drain."""
    orchestrator = _orchestrator()
    return orchestrator.stop_all(payload.project_ids, drain=payload.drain)


@router.get("/cycle")
async def orchestrator_cycle(
    stream: bool = Query(False, description="Stream multiple cycle snapshots"),
    iterations: int = Query(1, ge=1, le=20),
    delay: float = Query(0.0, ge=0.0, le=5.0),
) -> Response:
    """Run a global cycle once or stream repeated snapshots."""
    orchestrator = _orchestrator()
    if not stream:
        return JSONResponse(orchestrator.global_cycle())

    async def _stream():
        for _ in range(iterations):
            payload = orchestrator.global_cycle()
            yield json.dumps(payload) + "\n"
            if delay:
                await asyncio.sleep(delay)

    return StreamingResponse(_stream(), media_type="application/json")


@router.get("/health")
async def orchestrator_health(include_workers: bool = Query(True)) -> dict:
    """Return orchestrator health plus optional worker summaries."""
    health_report = registry.health.system_health()
    workers = {}
    if include_workers:
        autonomy = getattr(registry, "autonomy", None)
        intel = registry.get_subsystem("intelligence")
        if autonomy:
            workers["running"] = [pid for pid, status in autonomy.running.items() if status]
            workers["paused"] = [pid for pid, status in autonomy.paused.items() if status]
        if intel:
            queue_depths = {
                pid: len(intel.cognition.recent_memory(pid)) for pid in health_report.get("projects", {})
            }
            workers["queue_depths"] = queue_depths
    response = {
        "projects": health_report.get("projects", {}),
        "health": health_report,
    }
    if workers:
        response["workers"] = workers
    return response
