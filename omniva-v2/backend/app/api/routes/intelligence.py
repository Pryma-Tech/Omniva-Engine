"""Intelligence engine API routes."""

from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter()


def _engine():
    return registry.get_subsystem("intelligence")


@router.get("/status")
async def get_status() -> dict:
    return _engine().status()


@router.post("/mode/{mode}")
async def set_mode(mode: str) -> dict:
    return _engine().set_mode(mode)


@router.get("/posting-time/{project_id}")
async def get_posting_time(project_id: int) -> dict:
    return _engine().choose_posting_time(project_id)
