"""Bot control endpoints for Omniva Engine."""
# TODO: Expose bot start, stop, and status controls.

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from database import get_db
from utils.logger import logger
from workers.manager import WorkerManager


router = APIRouter()


def _get_manager(request: Request) -> WorkerManager:
    """Retrieve shared worker manager instance."""
    manager = getattr(request.app.state, "worker_manager", None)
    if manager is None:
        manager = WorkerManager()
        request.app.state.worker_manager = manager
    return manager


@router.get("/")
async def get_bot_status() -> dict:
    """Report current automation bot status (placeholder)."""
    logger.info("TODO: Report bot status.")
    return {"message": "TODO: report bot status"}


@router.post("/schedule/{project_id}")
async def schedule_upload(
    project_id: int,
    data: dict,
    request: Request,
    db: Session = Depends(get_db),
) -> dict:
    """
    Schedule daily upload for a project.
    TODO: Validate details & integrate scheduler.
    """
    logger.info("TODO: Schedule upload for project %s.", project_id)
    manager = _get_manager(request)
    hour = data.get("hour", 12)
    minute = data.get("minute", 0)
    schedule_job = manager.start_scheduler_job(project_id, hour, minute)
    return {
        "project_id": project_id,
        "hour": hour,
        "minute": minute,
        "status": "schedule placeholder",
        "job": schedule_job,
    }


@router.post("/scheduler/run")
async def run_scheduler_tick(
    request: Request,
    db: Session = Depends(get_db),
) -> dict:
    """
    Run a single scheduler tick.
    TODO: Trigger worker manager tick.
    """
    logger.info("TODO: Run scheduler tick via API.")
    manager = _get_manager(request)
    tick_result = manager.run_scheduler_tick()
    return {"status": "scheduler tick placeholder", "result": tick_result}


@router.post("/run")
async def run_jobs(request: Request) -> dict:
    """
    Run all pending jobs.
    TODO: Connect to real worker manager.
    """
    logger.info("TODO: Run jobs via API.")
    manager = _get_manager(request)
    return {"result": manager.run_all_pending()}


@router.post("/enqueue-test")
async def enqueue_test(request: Request) -> dict:
    """
    Enqueue a test job to verify WorkerManager.
    """
    logger.info("TODO: Enqueue test job via API.")
    manager = _get_manager(request)
    job = manager.queue_scrape(1, {"platform": "tiktok"})
    return {"queued": job}
