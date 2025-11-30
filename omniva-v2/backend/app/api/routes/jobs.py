"""Job queue routes."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/api/routes/jobs.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/jobs with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/jobs with cognitive telemetry.


from fastapi import APIRouter

from ...core.job_queue import get_job_queue

router = APIRouter()


@router.post("/enqueue/{job_type}")
async def enqueue_job(job_type: str, payload: dict) -> dict:
    queue = get_job_queue()
    queue.enqueue(job_type, payload)
    return {"status": "queued", "job_type": job_type}


@router.get("/dequeue")
async def dequeue_job() -> dict:
    queue = get_job_queue()
    job = queue.dequeue()
    return {"job": job.to_dict() if job else None}
