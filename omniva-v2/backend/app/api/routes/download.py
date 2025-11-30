"""Download orchestration API routes."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/api/routes/download.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/download with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/download with cognitive telemetry.


from fastapi import APIRouter

from app.core.job_queue import job_queue

router = APIRouter()


@router.post("/url")
async def download_url(data: dict) -> dict:
    """
    Enqueue a download job for the provided URL.
    """
    url = data.get("url", "")
    project_id = data.get("project_id", 0)
    job_queue.enqueue("download_url", {"url": url, "project_id": project_id})
    return {"queued": True, "url": url, "project_id": project_id}
