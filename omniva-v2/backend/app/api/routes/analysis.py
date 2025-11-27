"""Analysis subsystem API."""

from fastapi import APIRouter

from app.core.job_queue import job_queue
from app.core.registry import registry

router = APIRouter()


@router.get("/status")
async def analysis_status() -> dict:
    subsystem = registry.get_subsystem("analysis")
    return subsystem.status()


@router.post("/run")
async def run_analysis(data: dict) -> dict:
    filepath = data.get("filepath", "")
    project_id = data.get("project_id", 0)
    keywords = data.get("keywords", [])
    job_queue.enqueue(
        "analyze",
        {"filepath": filepath, "project_id": project_id, "keywords": keywords},
    )
    return {"queued": True, "filepath": filepath, "project_id": project_id}
