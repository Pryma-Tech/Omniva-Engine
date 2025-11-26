"""Pipeline history routes."""
# TODO: Add authentication and pagination.

from fastapi import APIRouter, Depends, Request

from pipeline.history.manager import PipelineHistoryManager

router = APIRouter()


def get_history(request: Request) -> PipelineHistoryManager:
    return request.app.state.pipeline_history


@router.get("/")
async def list_all_runs(history: PipelineHistoryManager = Depends(get_history)) -> list:
    return [vars(r) for r in history.list()]


@router.get("/{project_id}")
async def list_runs_by_project(project_id: int, history: PipelineHistoryManager = Depends(get_history)) -> list:
    return [vars(r) for r in history.list_by_project(project_id)]
