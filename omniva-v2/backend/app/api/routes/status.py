"""System status routes.

These endpoints provide coarse-grained information about the running
process and configuration. They are intended primarily for internal
dashboards and uptime checks.
"""

# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/status with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/status with cognitive telemetry.


from fastapi import APIRouter

from app.core.config import as_dict

router = APIRouter()


@router.get("/health", summary="Quick liveness check")
async def health() -> dict:
    """Return a minimal liveness signal plus basic config metadata."""

    return {"status": "ok", "config": as_dict()}
