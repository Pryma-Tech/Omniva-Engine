"""Event inspector routes (placeholder)."""

from fastapi import APIRouter

from app.core.event_bus import event_bus
from app.models.event import EventMessage

router = APIRouter()


@router.get("/history")
async def event_history() -> list:
    return event_bus.get_history()


@router.get("/status")
async def event_status() -> dict:
    return event_bus.status()


@router.post("/emit")
async def emit_event(msg: EventMessage) -> dict:
    return event_bus.publish(msg.event, msg.payload)
