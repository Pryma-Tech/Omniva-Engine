"""Metadata packet primitives for Omniva Stardust."""

from __future__ import annotations

from datetime import datetime
import uuid
from typing import Dict, List, Optional


class MetadataPacket:
    """
    Atomic unit of metadata:
      - ID
      - type (action/event)
      - payload
      - timestamp
      - parent links
    """

    def __init__(self, ptype: str, payload: Dict, parents: Optional[List[str]] = None) -> None:
        self.id = str(uuid.uuid4())
        self.ptype = ptype
        self.payload = payload
        self.timestamp = datetime.utcnow().isoformat()
        self.parents = parents or []

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.ptype,
            "timestamp": self.timestamp,
            "payload": self.payload,
            "parents": self.parents,
        }
