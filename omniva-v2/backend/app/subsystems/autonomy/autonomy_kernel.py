"""Autonomy kernel implementing dual-loop self-governing cycles."""

from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Dict, List

from app.core.event_bus import event_bus


class AutonomyKernel:
    """Run micro/macro loops per project."""

    def __init__(self, registry, controller) -> None:
        self.registry = registry
        self.controller = controller
        self.running: Dict[int, bool] = {}
        self.paused: Dict[int, bool] = {}

    def start_project(self, project_id: int) -> Dict[str, str]:
        if self.running.get(project_id):
            return {"status": "already_running"}
        self.running[project_id] = True
        self.paused[project_id] = False
        asyncio.create_task(self.microloop(project_id))
        asyncio.create_task(self.macroloop(project_id))
        return {"status": "started"}

    def stop_project(self, project_id: int) -> Dict[str, str]:
        self.running[project_id] = False
        return {"status": "stopped"}

    def pause_project(self, project_id: int) -> Dict[str, str]:
        self.paused[project_id] = True
        return {"status": "paused"}

    def resume_project(self, project_id: int) -> Dict[str, str]:
        self.paused[project_id] = False
        return {"status": "resumed"}

    async def microloop(self, project_id: int) -> None:
        while self.running.get(project_id):
            if self.paused.get(project_id):
                await asyncio.sleep(1.0)
                continue
            delay = await self.registry.guardrails.safe_call(
                project_id, self.run_micro_iteration(project_id), "microloop"
            )
            await asyncio.sleep(delay or 1.0)

    async def macroloop(self, project_id: int) -> None:
        while self.running.get(project_id):
            if self.paused.get(project_id):
                await asyncio.sleep(1.0)
                continue
            delay = await self.registry.guardrails.safe_call(
                project_id, self.run_macro_iteration(project_id), "macroloop"
            )
            await asyncio.sleep(delay or 5.0)

    async def run_micro_iteration(self, project_id: int) -> float:
        intel = self.registry.get_subsystem("intelligence")
        if intel is None:
            return 1.0
        emotion = intel.emotion_model.get(project_id)
        drift = intel.cognition.drift.get(project_id)
        attention = intel.cognition.attention.get(project_id, 1.0)
        snapshot = {
            "loop": "micro",
            "time": datetime.utcnow().isoformat(),
            "emotion": emotion,
            "cognition": {"attention": attention, "drift": drift},
        }
        intel.cognition.push_memory(project_id, snapshot)
        event_bus.publish("autonomy_microloop_tick", {"project_id": project_id, **snapshot})
        micro_delay, _ = self.controller.get_timing(project_id, emotion, {"attention": attention})
        return micro_delay

    async def run_macro_iteration(self, project_id: int) -> float:
        intel = self.registry.get_subsystem("intelligence")
        project_manager = self.registry.get_subsystem("project_manager")
        if intel is None:
            return 5.0
        clips: List[Dict] = []
        if project_manager and hasattr(project_manager, "get_project_clips"):
            clips = project_manager.get_project_clips(project_id)
        if clips:
            decision = intel.brain_decide(project_id, clips)
            intel.cognition.push_memory(
                project_id, {"loop": "macro", "time": datetime.utcnow().isoformat(), "decision": decision}
            )
            event_bus.publish("autonomy_macroloop_decision", {"project_id": project_id, "decision": decision})
            federation = self.registry.get_subsystem("federation")
            if federation:
                federation.update_project_stats(project_id)
                federation.federated_update()
            meta = self.registry.get_subsystem("meta")
            if meta:
                meta.record_project_stats(project_id)
                meta.run_cycle()
        emotion = intel.emotion_model.get(project_id)
        cognition = {"attention": intel.cognition.attention.get(project_id, 1.0)}
        _, macro_delay = self.controller.get_timing(project_id, emotion, cognition)
        return macro_delay
