"""Negotiation and consensus logic for Constellation agents."""

from __future__ import annotations

from typing import Dict, List


class CooperationProtocols:
    """Implements negotiation rounds between agent roles."""

    def __init__(self, registry) -> None:
        self.registry = registry

    def negotiate(self, project_id: int, context: Dict, role_agents: List) -> Dict:
        contributions: List[Dict] = []
        for agent in role_agents:
            contributions.append(agent.contribute(context))
        total_score = sum(c.get("score", 0.0) for c in contributions) or 1.0
        consensus: Dict[str, float] = {}
        for contribution in contributions:
            weight = contribution.get("score", 0.0) / total_score
            for key, value in contribution.get("recommendation", {}).items():
                if isinstance(value, bool):
                    consensus[key] = consensus.get(key, 0.0) + (1.0 if value else 0.0) * weight
                else:
                    consensus[key] = consensus.get(key, 0.0) + value * weight
        final = {}
        for key, value in consensus.items():
            final[key] = value >= 0.5 if isinstance(value, float) else value
        return {"agent_votes": contributions, "consensus": final}
