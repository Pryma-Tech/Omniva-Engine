"""Engine for agent strategy personalities."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/intelligence/personality/personality_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/intelligence/personality/personality_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/intelligence/personality/personality_engine with cognitive telemetry.


from __future__ import annotations

import json
import os
from typing import Dict, List

from .profiles import PERSONALITY_PROFILES


class PersonalityEngine:
    """Manage personality selection and apply strategy modifiers."""

    def __init__(self) -> None:
        self.profiles = PERSONALITY_PROFILES
        self.base = os.path.join("storage", "intelligence", "personalities")
        os.makedirs(self.base, exist_ok=True)
        self._cache: Dict[int, str] = {}

    # ------------------------------------------------------------------
    # Persistence helpers
    # ------------------------------------------------------------------
    def _path(self, project_id: int) -> str:
        return os.path.join(self.base, f"{project_id}.json")

    def _load_key(self, project_id: int) -> str:
        if project_id in self._cache:
            return self._cache[project_id]
        path = self._path(project_id)
        active = "balanced"
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as handle:
                    payload = json.load(handle)
                    active = payload.get("personality", active)
            except json.JSONDecodeError:
                active = "balanced"
        self._cache[project_id] = active if active in self.profiles else "balanced"
        return self._cache[project_id]

    def _save_key(self, project_id: int, key: str) -> None:
        self._cache[project_id] = key
        with open(self._path(project_id), "w", encoding="utf-8") as handle:
            json.dump({"project_id": project_id, "personality": key}, handle, indent=2)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def set_personality(self, project_id: int, key: str) -> Dict[str, object]:
        if key not in self.profiles:
            raise ValueError(f"Unknown personality: {key}")
        self._save_key(project_id, key)
        profile = dict(self.profiles[key])
        profile["key"] = key
        return profile

    def get_personality(self, project_id: int) -> Dict[str, object]:
        key = self._load_key(project_id)
        profile = dict(self.profiles.get(key, self.profiles["balanced"]))
        profile["key"] = key
        return profile

    def available_profiles(self) -> Dict[str, Dict[str, object]]:
        return self.profiles

    def apply_modifiers(self, project_id: int, scores: List[Dict[str, float]]) -> List[Dict[str, float]]:
        if not scores:
            return []

        key = self._load_key(project_id)
        profile = self.profiles.get(key, self.profiles["balanced"])
        mods = dict(profile.get("prio_mod", {}))
        niche_strictness = profile.get("niche_strictness", 0.5)

        if profile.get("adaptive") and scores:
            avg_priority = sum(entry.get("priority", 0.0) for entry in scores) / max(len(scores), 1)
            if avg_priority < 0.35:
                mods["trending"] = mods.get("trending", 1.0) * 1.15
                mods["keyword"] = mods.get("keyword", 1.0) * 1.05
            elif avg_priority > 0.7:
                mods["semantic"] = mods.get("semantic", 1.0) * 1.08

        results: List[Dict[str, float]] = []
        for entry in scores:
            semantic = float(entry.get("semantic", 0.0))
            keyword = float(entry.get("keyword", 0.0))
            trending = float(entry.get("trending", 0.0))
            audio = float(entry.get("audio", 0.0))

            semantic_component = semantic * mods.get("semantic", 1.0)
            keyword_component = keyword * mods.get("keyword", 1.0)
            trending_component = trending * mods.get("trending", 1.0)
            audio_component = audio * mods.get("audio", 1.0)

            combined = (semantic_component + keyword_component + trending_component + audio_component) / 4.0

            min_keyword = niche_strictness * 2.0
            if keyword < min_keyword:
                deficit = min_keyword - keyword
                penalty = max(0.6, 1 - deficit * 0.1)
                combined *= penalty
            else:
                surplus = keyword - min_keyword
                if surplus > 0:
                    combined *= 1 + min(0.15, surplus * 0.02)

            enriched = dict(entry)
            enriched["priority"] = round(combined, 6)
            enriched["personality_profile"] = key
            enriched["_personality_applied"] = True
            results.append(enriched)

        results.sort(key=lambda record: record.get("priority", 0.0), reverse=True)
        return results

    def drift_tolerance(self, project_id: int) -> float:
        return float(self.get_personality(project_id).get("drift_tolerance", 0.05))

    def post_aggression(self, project_id: int) -> float:
        return float(self.get_personality(project_id).get("post_aggression", 1.0))

    def niche_strictness(self, project_id: int) -> float:
        return float(self.get_personality(project_id).get("niche_strictness", 0.5))

    def editorial_style(self, project_id: int) -> str:
        return str(self.get_personality(project_id).get("editorial_style", "neutral"))
