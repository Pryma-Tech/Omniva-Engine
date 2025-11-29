"""Subsystem status routes (placeholder)."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/api/routes/subsystems.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/subsystems with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/subsystems with cognitive telemetry.


from fastapi import APIRouter

from app.core.registry import list_subsystems

router = APIRouter()


@router.get("/status")
async def subsystem_status() -> dict:
    return {"subsystems": list_subsystems()}
