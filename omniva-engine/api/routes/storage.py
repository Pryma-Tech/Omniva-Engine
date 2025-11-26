"""Storage API routes (placeholder)."""
# TODO: Secure endpoints and integrate real file stats.

from fastapi import APIRouter, Depends, Request

from storage.manager import StorageManager

router = APIRouter()


def get_storage_manager(request: Request) -> StorageManager:
    return request.app.state.storage_manager


@router.get("/project/{project_id}")
async def project_storage(project_id: int, manager: StorageManager = Depends(get_storage_manager)) -> dict:
    return manager.get_dirs(project_id)


@router.get("/stats")
async def storage_stats(manager: StorageManager = Depends(get_storage_manager)) -> dict:
    return manager.storage_stats()
