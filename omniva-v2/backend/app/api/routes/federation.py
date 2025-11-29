"""Federated intelligence API routes."""

from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter(prefix="/federation", tags=["federation"])


@router.get("/shared")
async def get_shared() -> dict:
    return registry.federation.shared_heuristics or {}
