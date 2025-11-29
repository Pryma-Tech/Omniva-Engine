"""Constellation engine enabling multi-agent collaboration."""

from __future__ import annotations

from typing import Dict

from .agent_roles import EditorAgent, RiskAgent, TrendAgent
from .cooperation_protocols import CooperationProtocols


class ConstellationEngine:
    """Multi-agent collaboration hub per project."""

    def __init__(self, registry) -> None:
        self.registry = registry
        self.protocols = CooperationProtocols(registry)

    def build_role_agents(self, project_id: int):
        return [TrendAgent(self.registry, project_id), RiskAgent(self.registry, project_id), EditorAgent(self.registry, project_id)]

    def collaborative_decision(self, project_id: int, decision_context: Dict) -> Dict:
        agents = self.build_role_agents(project_id)
        return self.protocols.negotiate(project_id, decision_context, agents)

    def cross_project_cooperation(self):
        federation = self.registry.get_subsystem("federation")
        if federation:
            return federation.shared_heuristics.get("niche_similarity", [])
        return []
