"""Job queue routes (placeholder)."""

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
    return {"job": job}
