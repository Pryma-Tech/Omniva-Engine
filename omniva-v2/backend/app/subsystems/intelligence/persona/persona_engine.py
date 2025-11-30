"""Persona engine coordinating temperament, voice, and committees."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/intelligence/persona/persona_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/intelligence/persona/persona_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/intelligence/persona/persona_engine with cognitive telemetry.


from __future__ import annotations

from typing import Dict, List

from .committee import PersonaCommittee
from .temperaments import TEMPERAMENTS
from .voices import VOICES


class PersonaEngine:
    """Manage persona configuration per project."""

    def __init__(self) -> None:
        self.temperaments = TEMPERAMENTS
        self.voices = VOICES
        self.committee = PersonaCommittee(self.temperaments, self.voices)
        self.active: Dict[int, Dict[str, List[str]]] = {}

    def set_persona(self, project_id: int, temperament, voice: str | None = None, committee: List[str] | None = None):
        if isinstance(temperament, dict):
            config = temperament
            temperament = config.get("temperament", "calm")
            voice = config.get("voice", "minimal")
            committee = config.get("committee", [])
        if temperament not in self.temperaments:
            raise ValueError("Unknown temperament")
        voice = voice or "minimal"
        if voice not in self.voices:
            raise ValueError("Unknown voice")
        committee = committee or []
        for member in committee:
            if member not in self.temperaments:
                raise ValueError(f"Unknown committee temperament: {member}")
        self.active[project_id] = {
            "temperament": temperament,
            "voice": voice,
            "committee": committee,
        }
        return self.active[project_id]

    def get_persona(self, project_id: int) -> Dict[str, List[str]]:
        return self.active.get(
            project_id,
            {
                "temperament": "calm",
                "voice": "minimal",
                "committee": [],
            },
        )

    # ------------------------------------------------------------------
    # Influence hooks
    # ------------------------------------------------------------------
    def apply_temperament(self, project_id: int, priority_list: List[Dict]) -> List[Dict]:
        if not priority_list:
            return []
        persona = self.get_persona(project_id)
        temperament = self.temperaments.get(persona["temperament"], self.temperaments["calm"])
        risk = temperament.get("risk_factor", 1.0)
        stability = temperament.get("stability_bonus", 0.0)

        adjusted: List[Dict] = []
        for clip in priority_list:
            priority = float(clip.get("priority", 0.0))
            semantic = float(clip.get("semantic", 0.0))
            new_priority = priority * risk + stability * semantic
            clone = dict(clip)
            clone["priority"] = round(new_priority, 6)
            clone["temperament"] = persona["temperament"]
            adjusted.append(clone)

        adjusted.sort(key=lambda item: item.get("priority", 0.0), reverse=True)
        return adjusted

    def committee_vote(self, project_id: int, scored_clips: List[Dict]) -> List[Dict]:
        persona = self.get_persona(project_id)
        committee = persona.get("committee") or []
        if not committee:
            return scored_clips
        return self.committee.vote(committee, scored_clips)

    def apply_voice(self, project_id: int, explanation: Dict) -> Dict:
        persona = self.get_persona(project_id)
        voice = self.voices.get(persona["voice"], self.voices["minimal"])
        verbosity = voice.get("verbosity", 0.5)
        if verbosity < 0.4:
            return {
                "reason": explanation.get("reason"),
                "score": explanation.get("score"),
            }
        if verbosity > 0.8:
            enriched = dict(explanation)
            enriched["style"] = voice.get("style")
            return enriched
        return explanation
