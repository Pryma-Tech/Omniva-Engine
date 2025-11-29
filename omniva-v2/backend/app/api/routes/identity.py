from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter(prefix="/identity", tags=["identity"])


@router.get("/")
async def get_identity():
    return registry.selfmodel.get_identity()


@router.post("/recompute")
async def recompute_identity():
    registry.selfmodel.recompute_identity()
    return registry.selfmodel.get_identity()
