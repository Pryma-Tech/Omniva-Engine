"""Infrastructure health endpoints."""

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
