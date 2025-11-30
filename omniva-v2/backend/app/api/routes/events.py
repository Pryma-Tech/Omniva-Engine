"""Event log API."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/api/routes/events.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/events with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/events with cognitive telemetry.


from fastapi import APIRouter

from app.core.event_bus import event_bus

router = APIRouter()


@router.get("/log")
async def event_log() -> list:
    return event_bus.get_log()
