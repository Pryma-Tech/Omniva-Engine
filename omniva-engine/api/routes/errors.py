"""Error management routes (placeholder)."""
# TODO: Guard with auth and richer filtering.

from fastapi import APIRouter, Depends, Request

from errors.manager import ErrorManager

router = APIRouter()


def get_error_manager(request: Request) -> ErrorManager:
    return request.app.state.error_manager


@router.get("/")
async def list_errors(manager: ErrorManager = Depends(get_error_manager)) -> list:
    return [vars(err) for err in manager.list_all()]


@router.get("/{project_id}")
async def list_project_errors(project_id: int, manager: ErrorManager = Depends(get_error_manager)) -> list:
    return [vars(err) for err in manager.list_by_project(project_id)]


@router.post("/retry/{error_id}")
async def retry_error(error_id: int, manager: ErrorManager = Depends(get_error_manager)) -> dict | None:
    err = manager.retry(error_id)
    return vars(err) if err else None


@router.post("/resolve/{error_id}")
async def resolve_error(error_id: int, manager: ErrorManager = Depends(get_error_manager)) -> dict | None:
    err = manager.resolve(error_id)
    return vars(err) if err else None
