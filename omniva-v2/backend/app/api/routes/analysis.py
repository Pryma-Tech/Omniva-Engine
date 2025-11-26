"""Analysis subsystem API (placeholder)."""

from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter()


@router.get("/status")
async def analysis_status() -> dict:
    subsystem = registry.get_subsystem("analysis")
    return subsystem.status()


@router.post("/run")
async def run_analysis(data: dict) -> list:
    subsystem = registry.get_subsystem("analysis")
    candidates = subsystem.analyze_transcript(
        project_id=data.get("project_id"),
        transcript=data.get("transcript"),
    )
    return [c.dict() for c in candidates]
