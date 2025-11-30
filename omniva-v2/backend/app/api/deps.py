"""Shared FastAPI dependencies for control-plane routes (v2)."""

from __future__ import annotations

import os
from typing import List, Optional

from fastapi import Header, HTTPException

CONTROL_HEADER = "X-Omniva-Control-Token"
SCOPE_HEADER = "X-Omniva-Project-Scope"
CONTROL_TOKEN_ENV = "OMNIVA_CONTROL_TOKEN"


def require_control_token(token: str | None = Header(None, alias=CONTROL_HEADER)) -> str:
    """Enforce that callers supply the expected control token header."""
    if not token:
        raise HTTPException(status_code=401, detail="missing control token")
    expected = os.getenv(CONTROL_TOKEN_ENV)
    if expected and token != expected:
        raise HTTPException(status_code=403, detail="invalid control token")
    return token


def parse_project_scope(scope_header: str | None = Header(None, alias=SCOPE_HEADER)) -> Optional[List[int]]:
    """Parse a comma-separated project scope header into a list of ints."""
    if not scope_header:
        return None
    try:
        return [int(pid.strip()) for pid in scope_header.split(",") if pid.strip()]
    except ValueError as exc:  # pragma: no cover - defensive branch
        raise HTTPException(status_code=400, detail="invalid project scope header") from exc

