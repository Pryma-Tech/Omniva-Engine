from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter(prefix="/soul", tags=["soul"])


@router.get("/codex")
async def codex():
    return registry.soul.get_codex()


@router.get("/journal")
async def journal():
    return registry.soul.get_journal()
