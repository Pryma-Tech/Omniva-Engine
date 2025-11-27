"""Uploader subsystem API."""

from fastapi import APIRouter

from app.core.job_queue import job_queue
from app.core.registry import registry

router = APIRouter()


@router.get("/status")
async def uploader_status() -> dict:
    subsystem = registry.get_subsystem("uploader")
    return subsystem.status()


@router.post("/run")
async def run_upload(data: dict) -> dict:
    clips = data.get("clips", [])
    project_id = data.get("project_id", 0)
    job_queue.enqueue("upload_clip", {"clips": clips, "project_id": project_id})
    return {"queued": True, "clips": clips, "project_id": project_id}
