"""Editing subsystem API."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/api/routes/editing.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/editing with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/editing with cognitive telemetry.


from typing import Any, Dict

from fastapi import APIRouter

from app.core.job_queue import job_queue
from app.core.registry import registry

router = APIRouter()


@router.get("/status")
async def editing_status() -> Dict[str, Any]:
    subsystem = registry.get_subsystem("editing")
    return subsystem.status()


@router.post("/run")
async def run_editing(data: Dict[str, Any]) -> Dict[str, Any]:
    job_queue.enqueue(
        "edit_clip",
        {
            "analysis_filepath": data.get("analysis_filepath", ""),
            "project_id": data.get("project_id", 0),
            "top_n": data.get("top_n", 1),
        },
    )
    return {"queued": True}
