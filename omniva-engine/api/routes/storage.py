"""Storage information routes for Omniva Engine."""
# TODO: Add auth, file listings, and management operations.

from fastapi import APIRouter

from utils.storage import storage_manager

router = APIRouter()


@router.get("/info")
async def storage_info() -> dict:
    """Return storage description."""
    return storage_manager.describe()
