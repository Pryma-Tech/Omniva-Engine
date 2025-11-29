"""Strategic meta-learning API routes."""

from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter(prefix="/meta", tags=["meta"])


@router.get("/run")
async def run_meta() -> dict:
    return registry.meta.run_cycle() or {}
