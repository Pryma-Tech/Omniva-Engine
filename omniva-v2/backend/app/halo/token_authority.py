"""Scoped token issuance and validation."""

from __future__ import annotations

import secrets
from datetime import datetime, timedelta
from typing import Dict


class TokenAuthority:
    """
    Issues & validates scoped tokens for:
      - subsystems
      - Sanctum commands
      - Etherlink nodes
      - Plugin execution
    """

    def __init__(self) -> None:
        self.tokens: Dict[str, Dict[str, str]] = {}

    def issue(self, scope: str, ttl_minutes: int = 1440) -> str:
        token = secrets.token_hex(32)
        self.tokens[token] = {
            "scope": scope,
            "expires": (datetime.utcnow() + timedelta(minutes=ttl_minutes)).isoformat(),
        }
        return token

    def validate(self, token: str, scope: str) -> bool:
        meta = self.tokens.get(token)
        if not meta or meta["scope"] != scope:
            return False
        if datetime.fromisoformat(meta["expires"]) < datetime.utcnow():
            return False
        return True

    def list(self) -> Dict[str, Dict[str, str]]:
        return self.tokens
