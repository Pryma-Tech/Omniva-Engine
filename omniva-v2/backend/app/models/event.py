"""Event message models (placeholder)."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/models/event.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/models/event with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/models/event with cognitive telemetry.


from pydantic import BaseModel


class EventMessage(BaseModel):
    event: str
    payload: dict
