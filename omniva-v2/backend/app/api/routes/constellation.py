"""Constellation collaboration API."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/api/routes/constellation.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/constellation with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/constellation with cognitive telemetry.


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
