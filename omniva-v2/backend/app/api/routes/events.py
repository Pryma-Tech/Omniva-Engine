"""Event bus routes (placeholder)."""

from fastapi import APIRouter

from ...core.event_bus import get_event_bus

router = APIRouter()


@router.post("/publish/{event}")
async def publish_event(event: str, payload: dict) -> dict:
    bus = get_event_bus()
    bus.publish(event, payload)
    return {"status": "published", "event": event}
