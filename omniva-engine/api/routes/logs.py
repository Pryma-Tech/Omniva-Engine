"""Log viewing routes for Omniva Engine."""
# TODO: Add filtering, pagination, and authentication checks.

from fastapi import APIRouter, Depends, Request

from utils.logger import get_logs_tail, logger
from logs.manager import LogManager

router = APIRouter()


def get_log_manager(request: Request) -> LogManager:
    return request.app.state.log_manager


@router.get("/")
async def list_logs(manager: LogManager = Depends(get_log_manager)) -> list:
    """List all placeholder logs."""
    return [vars(log) for log in manager.list_all()]


@router.get("/{subsystem}")
async def list_logs_by_subsystem(subsystem: str, manager: LogManager = Depends(get_log_manager)) -> list:
    """Filter logs by subsystem."""
    return [vars(log) for log in manager.list_by_subsystem(subsystem)]


@router.get("/view")
async def view_logs(lines: int = 200) -> dict:
    """Tail logs from the unified file."""
    logger.info("TODO: Serve logs via API (last %s lines).", lines)
    return {"logs": get_logs_tail(lines)}
