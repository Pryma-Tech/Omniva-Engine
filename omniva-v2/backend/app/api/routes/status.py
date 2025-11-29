"""System status routes (placeholder)."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/api/routes/status.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/status with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/status with cognitive telemetry.


from fastapi import APIRouter

from app.core.config import as_dict

router = APIRouter()


@router.get("/health")
async def health() -> dict:
    return {"status": "ok", "config": as_dict()}
