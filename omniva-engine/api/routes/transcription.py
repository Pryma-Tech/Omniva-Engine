"""Transcription manager routes (placeholder)."""
# TODO: Secure endpoints and validate inputs.

from fastapi import APIRouter, Depends, Request

from transcription.manager import TranscriptionManager

router = APIRouter()


def get_manager(request: Request) -> TranscriptionManager:
    return request.app.state.transcription_manager


@router.post("/run")
async def run_transcription(data: dict, manager: TranscriptionManager = Depends(get_manager)) -> dict:
    project_id = data.get("project_id")
    video_path = data.get("video_path", "unknown.mp4")
    job = manager.transcribe(project_id, video_path)
    return vars(job)


@router.get("/")
async def list_jobs(manager: TranscriptionManager = Depends(get_manager)) -> list:
    return [vars(job) for job in manager.list_all()]


@router.get("/{project_id}")
async def list_for_project(project_id: int, manager: TranscriptionManager = Depends(get_manager)) -> list:
    return [vars(job) for job in manager.list_by_project(project_id)]
