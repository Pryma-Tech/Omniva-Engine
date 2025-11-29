"""Analysis subsystem API."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/api/routes/analysis.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/analysis with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/analysis with cognitive telemetry.


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
