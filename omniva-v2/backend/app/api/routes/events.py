"""Event log API."""

from fastapi import APIRouter

from app.core.event_bus import event_bus

router = APIRouter()


@router.get("/log")
async def event_log() -> list:
    return event_bus.get_log()
