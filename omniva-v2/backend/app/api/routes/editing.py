"""Editing subsystem API (placeholder)."""

from typing import Any, Dict

from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter()


@router.get("/status")
async def editing_status() -> Dict[str, Any]:
    subsystem = registry.get_subsystem("editing")
    return subsystem.status()


@router.post("/render")
async def render_clips(data: Dict[str, Any]) -> Dict[str, Any]:
    subsystem = registry.get_subsystem("editing")
    result = subsystem.render_candidates(data.get("candidates", []))
    return result
