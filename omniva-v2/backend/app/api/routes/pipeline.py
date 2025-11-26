"""Pipeline routes (placeholder)."""

from fastapi import APIRouter

from app.models.pipeline import PipelineRun, PipelineStep

router = APIRouter()


@router.get("/status/{project_id}")
async def get_pipeline_status(project_id: int) -> dict:
    steps = [
        PipelineStep(name="scrape", status="completed"),
        PipelineStep(name="download", status="pending"),
    ]
    return PipelineRun(project_id=project_id, steps=steps, status="running").dict()
