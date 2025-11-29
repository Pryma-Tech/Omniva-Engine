"""Infrastructure health endpoints."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/api/routes/health.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/health with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/health with cognitive telemetry.


from fastapi import APIRouter

from app.core.health import check_jobs, check_storage, check_uploader

router = APIRouter()


@router.get("/")
async def health_summary() -> dict:
    return {
        "storage": check_storage(),
        "jobs": check_jobs(),
        "uploader": check_uploader(),
    }
