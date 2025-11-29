"""HaloGuard middleware dependency."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/halo/halo_guard.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/halo/halo_guard with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/halo/halo_guard with cognitive telemetry.


from __future__ import annotations

from fastapi import HTTPException, Request


class HaloGuard:
    """
    Injected into FastAPI routes as a dependency.
    Verifies tokens according to the route's required scope.
    """

    def __init__(self, halo) -> None:
        self.halo = halo

    async def require(self, request: Request, scope: str) -> None:
        token = request.headers.get("X-Omniva-Token") or request.query_params.get("token")
        if not token or not self.halo.validate(token, scope):
            raise HTTPException(status_code=401, detail="invalid_or_missing_token")
