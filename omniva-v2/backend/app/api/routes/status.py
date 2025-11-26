"""System status routes (placeholder)."""

from fastapi import APIRouter

from ...core.config import as_dict

router = APIRouter()


@router.get("/health")
async def health() -> dict:
    return {"status": "ok", "config": as_dict()}
