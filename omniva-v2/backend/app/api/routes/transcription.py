"""Transcription subsystem API."""

from fastapi import APIRouter

from app.core.job_queue import job_queue
from app.core.registry import registry

router = APIRouter()


@router.get("/status")
async def transcription_status() -> dict:
    subsystem = registry.get_subsystem("transcription")
    return subsystem.status()


@router.post("/file")
async def transcribe_file(data: dict) -> dict:
    """
    Enqueue a transcription job for an existing media file.
    """
    filepath = data.get("filepath", "")
    project_id = data.get("project_id", 0)
    job_queue.enqueue("transcribe", {"filepath": filepath, "project_id": project_id})
    return {"queued": True, "filepath": filepath, "project_id": project_id}
