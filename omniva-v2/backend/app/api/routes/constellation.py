"""Constellation collaboration API."""

from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter(prefix="/constellation", tags=["constellation"])


@router.get("/consensus/{project_id}")
async def get_consensus(project_id: int) -> dict:
    intel = registry.get_subsystem("intelligence")
    context = {"priorities": []}
    return registry.constellation.collaborative_decision(project_id, context)


@router.get("/similarity")
async def get_similarity() -> dict:
    return {"niche_similarity": registry.constellation.cross_project_cooperation()}
