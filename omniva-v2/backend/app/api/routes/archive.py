from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter(prefix="/archive", tags=["archive"])


@router.get("/timeline")
async def timeline():
    return registry.archive.timeline[-200:]


@router.get("/epochs")
async def epochs():
    return registry.archive.epochs


@router.get("/summary")
async def summary():
    return registry.archive.summary()
