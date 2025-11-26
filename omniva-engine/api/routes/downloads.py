"""Download manager routes (placeholder)."""
# TODO: Authenticate and validate inputs.

from fastapi import APIRouter, Depends, Request

from downloads.manager import DownloadManager

router = APIRouter()


def get_download_manager(request: Request) -> DownloadManager:
    return request.app.state.download_manager


@router.post("/run")
async def run_download(data: dict, manager: DownloadManager = Depends(get_download_manager)) -> dict:
    project_id = data.get("project_id")
    platform = data.get("platform", "tiktok")
    source = data.get("source", "unknown")
    job = manager.download(project_id, platform, source)
    return vars(job)


@router.get("/")
async def list_downloads(manager: DownloadManager = Depends(get_download_manager)) -> list:
    return [vars(job) for job in manager.list_all()]


@router.get("/{project_id}")
async def list_for_project(project_id: int, manager: DownloadManager = Depends(get_download_manager)) -> list:
    return [vars(job) for job in manager.list_by_project(project_id)]
