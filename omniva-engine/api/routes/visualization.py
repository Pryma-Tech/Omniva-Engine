"""Pipeline visualization routes (placeholder)."""
# TODO: Enforce auth and return live status.

from fastapi import APIRouter, Depends, Request

from pipeline.visualization.manager import PipelineVisualizationManager

router = APIRouter()


def get_visualizer(request: Request) -> PipelineVisualizationManager:
    return request.app.state.pipeline_visualizer


@router.get("/structure")
async def get_pipeline_structure(visualizer: PipelineVisualizationManager = Depends(get_visualizer)) -> dict:
    return visualizer.get_structure()
