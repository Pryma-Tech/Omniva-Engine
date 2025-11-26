"""Event message models (placeholder)."""

from pydantic import BaseModel


class EventMessage(BaseModel):
    event: str
    payload: dict
