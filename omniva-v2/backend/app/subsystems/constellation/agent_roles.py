"""Agent roles participating in the Constellation collaboration layer."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/constellation/agent_roles.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/constellation/agent_roles with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/constellation/agent_roles with cognitive telemetry.


from __future__ import annotations


class BaseAgentRole:
    """Parent class for specialized agents operating within a project."""

    def __init__(self, registry, project_id: int):
        self.registry = registry
        self.project_id = project_id

    def contribute(self, decision_context: dict):  # pragma: no cover - interface
        raise NotImplementedError


class TrendAgent(BaseAgentRole):
    """Examines global and local trend signals."""

    def contribute(self, decision_context: dict):
        federation = self.registry.get_subsystem("federation")
        trend = 0.0
        if federation:
            trend = federation.trend_scores.get(self.project_id, 0.0)
        return {"score": trend, "recommendation": {"boost_trending": trend > 0.5}}


class RiskAgent(BaseAgentRole):
    """Flags risk when stress/drift are elevated."""

    def contribute(self, decision_context: dict):
        intel = self.registry.get_subsystem("intelligence")
        if intel is None:
            return {"score": 0.0, "recommendation": {}}
        emotion = intel.emotion_model.get(self.project_id)
        drift = intel.cognition.drift.get(self.project_id)
        risk_score = (emotion.get("stress", 0.0) + drift.get("drift_strength", 0.0)) / 2
        return {"score": max(0.0, 1 - risk_score), "recommendation": {"avoid_posting": risk_score > 0.7}}


class EditorAgent(BaseAgentRole):
    """Provides editing style hints based on persona."""

    def contribute(self, decision_context: dict):
        intel = self.registry.get_subsystem("intelligence")
        persona = intel.persona.get_persona(self.project_id) if intel else {}
        style = persona.get("style_profile", persona.get("voice", "minimal"))
        return {"score": 0.5, "recommendation": {"editor_style": style}}
