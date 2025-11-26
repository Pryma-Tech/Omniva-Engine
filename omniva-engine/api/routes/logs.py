"""Log viewing routes for Omniva Engine."""
# TODO: Add filtering, pagination, and authentication checks.

from fastapi import APIRouter

from utils.logger import get_logs_tail, logger

router = APIRouter()


@router.get("/view")
async def view_logs(lines: int = 200) -> dict:
    """View last X lines of the logs (placeholder)."""
    logger.info("TODO: Serve logs via API (last %s lines).", lines)
    return {"logs": get_logs_tail(lines)}
