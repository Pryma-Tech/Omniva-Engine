"""Safety subsystem API routes."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/api/routes/safety.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/safety with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/safety with cognitive telemetry.

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.core.registry import registry

router = APIRouter(prefix="/safety", tags=["safety"])


def _safety_engine():
    engine = getattr(registry, "safety", None)
    if engine is None:
        raise HTTPException(status_code=503, detail="safety subsystem unavailable")
    return engine


def _crisis_engine():
    crisis = getattr(registry, "crisis", None)
    if crisis is None:
        raise HTTPException(status_code=503, detail="crisis subsystem unavailable")
    return crisis


@router.get("/status")
async def safety_status() -> dict:
    """Return high-level safety subsystem status."""
    engine = _safety_engine()
    return {"name": "safety", "engine": engine.__class__.__name__}


@router.get("/crises/{project_id}")
async def list_crises(project_id: int) -> dict:
    """List recorded crises for a project."""
    crisis = _crisis_engine()
    return {"project_id": project_id, "crises": crisis.get_crises(project_id)}


@router.post("/validate/clip/{project_id}")
async def validate_clip(project_id: int, clip: dict) -> dict:
    """Validate a clip payload against basic safety rules."""
    engine = _safety_engine()
    ok, reason = engine.validate_clip(project_id, clip or {})
    return {"project_id": project_id, "ok": ok, "reason": reason}


@router.post("/validate/action/{project_id}")
async def validate_action(project_id: int, action: dict) -> dict:
    """Validate a higher-level action (including chosen clip)."""
    engine = _safety_engine()
    ok, reason = engine.validate_action(project_id, action or {})
    return {"project_id": project_id, "ok": ok, "reason": reason}
