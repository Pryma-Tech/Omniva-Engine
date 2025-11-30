"""Multi-agent persona voting helpers."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/intelligence/persona/committee.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/intelligence/persona/committee with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/intelligence/persona/committee with cognitive telemetry.


from __future__ import annotations

from typing import Dict, List


class PersonaCommittee:
    """Aggregate clip votes across multiple persona temperaments."""

    def __init__(self, temperaments: Dict[str, Dict], voices: Dict[str, Dict]) -> None:
        self.temperaments = temperaments
        self.voices = voices

    def vote(self, persona_keys: List[str], scored_clips: List[Dict]) -> List[Dict]:
        if not persona_keys:
            return scored_clips

        votes: Dict[str, float] = {}
        clip_lookup = {clip.get("clip_id"): clip for clip in scored_clips}

        for persona in persona_keys:
            temperament = self.temperaments.get(persona)
            if not temperament:
                continue
            risk = temperament.get("risk_factor", 1.0)
            excitement = temperament.get("excitability", 0.0)

            for clip in scored_clips:
                clip_id = clip.get("clip_id")
                if clip_id is None:
                    continue
                base = float(clip.get("priority", 0.0))
                trending = float(clip.get("trending", 0.0))
                vote_score = base * risk + excitement * trending
                votes[clip_id] = votes.get(clip_id, 0.0) + vote_score

        results: List[Dict] = []
        if not votes:
            return scored_clips

        for clip_id, score in votes.items():
            clone = dict(clip_lookup.get(clip_id, {"clip_id": clip_id}))
            clone["priority"] = round(score, 6)
            clone["committee_score"] = score
            results.append(clone)

        results.sort(key=lambda entry: entry.get("priority", 0.0), reverse=True)
        return results
