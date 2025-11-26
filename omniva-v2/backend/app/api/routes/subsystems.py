"""Subsystem status routes (placeholder)."""

from fastapi import APIRouter

from app.core.registry import list_subsystems

router = APIRouter()


@router.get("/status")
async def subsystem_status() -> dict:
    return {"subsystems": list_subsystems()}
