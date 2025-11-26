"""Authentication dependency placeholder."""
# TODO: Add real session cookie validation.

from fastapi import HTTPException, Request

from .session_manager import session_manager


def require_login(request: Request) -> None:
    """Ensure that a session token exists for protected routes."""
    token = request.cookies.get("session_token")
    if not token or not session_manager.get_session(token):
        raise HTTPException(status_code=401, detail="Not authenticated (placeholder)")
