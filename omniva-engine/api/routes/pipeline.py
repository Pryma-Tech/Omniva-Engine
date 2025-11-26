"""Pipeline orchestration routes."""
# TODO: Tie into real background jobs and persistence.

from fastapi import APIRouter

from fastapi import APIRouter, Depends, Request

from pipeline.orchestrator import ClipPipelineOrchestrator

router = APIRouter()


def get_orchestrator(request: Request) -> ClipPipelineOrchestrator:
    return request.app.state.clip_orchestrator


@router.post("/run/{project_id}")
async def run_pipeline(project_id: int, orchestrator: ClipPipelineOrchestrator = Depends(get_orchestrator)) -> dict:
    """Trigger placeholder pipeline."""
    return orchestrator.run_pipeline(project_id)
