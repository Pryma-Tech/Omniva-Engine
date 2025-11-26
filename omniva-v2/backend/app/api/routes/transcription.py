"""Transcription subsystem API (placeholder)."""

from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter()


@router.get("/status")
async def transcription_status() -> dict:
    subsystem = registry.get_subsystem("transcription")
    return subsystem.status()


@router.post("/run")
async def run_transcription(data: dict) -> dict:
    subsystem = registry.get_subsystem("transcription")
    # Placeholder response until transcription engine is wired up.
    return {"status": "transcription requested (placeholder)", "payload": data}
