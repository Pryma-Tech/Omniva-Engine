"""Download API endpoints."""

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
