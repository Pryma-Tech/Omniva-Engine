"""Analysis subsystem API."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/api/routes/analysis.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/analysis with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/analysis with cognitive telemetry.

from __future__ import annotations

import logging
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.job_queue import job_queue
from app.core.registry import registry

logger = logging.getLogger(__name__)

router = APIRouter()


class AnalysisRequest(BaseModel):
    """Request payload for analysis runs."""

    filepath: str
    project_id: int = 0
    keywords: List[str] = []


@router.get("/status")
async def analysis_status() -> dict:
    """Return current analysis subsystem status."""
    subsystem = registry.get_subsystem("analysis")
    if not subsystem:
        payload = {"status": "unavailable"}
        logger.warning("analysis.status_unavailable", extra=payload)
        return payload

    status = subsystem.status()
    logger.info("analysis.status", extra={"status": status})
    return status


@router.post("/run")
async def run_analysis(request: AnalysisRequest) -> dict:
    """Queue an analysis job for the given file and project."""
    payload = request.dict()
    job_queue.enqueue("analyze", payload)
    logger.info(
        "analysis.run_queued",
        extra={
            "project_id": request.project_id,
            "filepath": request.filepath,
            "keywords_count": len(request.keywords),
        },
    )
    return {"queued": True, **payload}
