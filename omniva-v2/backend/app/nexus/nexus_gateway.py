"""Unified API façade and response normalizer for Omniva."""

from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse


class NexusGateway:
    """
    Unified API gateway consolidating all composable endpoints
    and standardizing response structures.
    """

    def __init__(self, registry, composer) -> None:
        self.registry = registry
        self.composer = composer
        self.router = APIRouter(prefix="/nexus", tags=["nexus"])
        self.router.get("/snapshot", dependencies=[Depends(self._guard("nexus"))])(self.full_snapshot)
        self.router.get("/project/{project_id}", dependencies=[Depends(self._guard("nexus"))])(self.project_brief)
        self.router.get("/health", dependencies=[Depends(self._guard("nexus"))])(self.health_check)

    def _guard(self, scope: str):
        async def guard_dependency(request: Request):
            await self.registry.guard.require(request, scope)

        return guard_dependency

    def _projects(self) -> Optional[Any]:
        return (
            self.registry.get_subsystem("project_manager")
            or self.registry.get_subsystem("projects")
            or getattr(self.registry, "projects", None)
        )

    async def full_snapshot(self):
        try:
            result = self.composer.full_system_snapshot()
            return JSONResponse({"ok": True, "data": result})
        except Exception as exc:  # pragma: no cover - defensive serialization
            return JSONResponse({"ok": False, "error": str(exc)}, status_code=500)

    async def project_brief(self, project_id: int):
        try:
            result = self.composer.project_brief(project_id)
            return JSONResponse({"ok": True, "data": result})
        except Exception as exc:  # pragma: no cover - defensive serialization
            return JSONResponse({"ok": False, "error": str(exc)}, status_code=500)

    async def health_check(self):
        """
        Lightweight global status probe.
        """
        heartbeat = getattr(self.registry.heartbeat, "running", False)
        projects = self._projects()
        project_total = len(projects.get_all_project_ids()) if projects and hasattr(projects, "get_all_project_ids") else 0
        archive = self.registry.archive if hasattr(self.registry, "archive") else None
        epochs = len(getattr(archive, "epochs", []) or []) if archive else 0

        return {
            "heartbeat_running": heartbeat,
            "project_count": project_total,
            "epochs_recorded": epochs,
            "status": "ok" if heartbeat else "standby",
        }
