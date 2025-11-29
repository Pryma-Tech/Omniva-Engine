"""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/intelligence/intelligence_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/intelligence/intelligence_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/intelligence/intelligence_engine with cognitive telemetry.

Intelligence layer controller for Omniva Engine.
"""

from app.core.event_bus import event_bus
from app.core.registry import registry


class IntelligenceEngine:
    """Coordinates predictors and strategy modes."""

    name = "intelligence"

    def __init__(self) -> None:
        from .predictors.audio_trends import AudioTrendMatcher
        from .predictors.semantic_ranker import SemanticRanker
        from .predictors.keyword_ranker import KeywordRanker
        from .predictors.posting_time import PostingTimePredictor
        from .modes.balanced import BalancedMode
        from .modes.evergreen import EvergreenMode
        from .modes.viral_first import ViralFirstMode
        from .ghost_run.ghost_run_engine import GhostRunEngine
        from .behavior.tree_engine import BehaviorTreeEngine
        from .personality.personality_engine import PersonalityEngine
        from .persona.persona_engine import PersonaEngine
        from .emotion.emotion_model import EmotionModel
        from .emotion.emotional_engine import EmotionalEngine
        from .cognition.cognitive_engine import CognitiveEngine
        from .ltm.ltm_engine import LongTermMemoryEngine
        from .ltm.ltm_store import LTMStore
        from .self_opt.optimizer_engine import MetaOptimizerEngine
        from .planner.planner_engine import PlannerEngine
        from .deliberation.deliberation_engine import DeliberationEngine
        from .brain.brain_engine import UnifiedAgentBrain
        from .prioritizer.prioritizer_engine import ClipPrioritizer

        self.posting_time = PostingTimePredictor()
        self.keyword_ranker = KeywordRanker()
        self.audio_trends = AudioTrendMatcher()
        self.semantic_ranker = SemanticRanker()
        self.prioritizer = ClipPrioritizer()
        self.ghost = GhostRunEngine()
        self.optimizer = MetaOptimizerEngine()
        self.ltm_store = LTMStore()
        self.ltm = LongTermMemoryEngine(self.ltm_store)
        self.personality = PersonalityEngine()
        self.bt = BehaviorTreeEngine()
        self.persona = PersonaEngine()
        self.emotion_model = EmotionModel()
        self.emotion = EmotionalEngine(self.emotion_model)
        self.cognition = CognitiveEngine()
        self.planner = PlannerEngine()
        self.deliberation = DeliberationEngine(registry)
        self.brain = UnifiedAgentBrain(registry)

        self.modes = {
            "viral": ViralFirstMode(self),
            "evergreen": EvergreenMode(self),
            "balanced": BalancedMode(self),
        }
        self.current_mode = "balanced"

    def initialize(self) -> dict:
        return {"status": "intelligence engine initialized"}

    def set_mode(self, mode: str) -> dict:
        if mode in self.modes:
            self.current_mode = mode
            event_bus.publish("intelligence_mode_changed", {"mode": mode})
            return {"mode": mode}
        return {"error": "unknown mode", "available": list(self.modes.keys())}

    def choose_posting_time(self, project_id: int) -> dict:
        return self.posting_time.predict_best_time(project_id)

    def rank_clips(self, project_id: int, clip_candidates: list) -> list:
        return self.keyword_ranker.rank(project_id, clip_candidates)

    def match_audio(self, project_id: int, clip_meta: dict) -> dict:
        return self.audio_trends.match(project_id, clip_meta)

    def apply_mode(self, project_id: int, context: dict) -> dict:
        mode = self.modes[self.current_mode]
        return mode.apply(project_id, context)

    def get_posting_stats(self, project_id: int) -> dict:
        return self.posting_time.store.load(project_id)

    def get_trending_keywords(self, project_id: int) -> dict:
        return self.keyword_ranker.store.get_trends(project_id)

    def semantic_rank(self, project_id: int, clips: list) -> list:
        return self.semantic_ranker.rank(project_id, clips)

    def get_audio_trends(self, project_id: int) -> dict:
        return self.audio_trends.store.get_trending(project_id)

    def prioritize_clips(self, project_id: int, semantic: list, keyword: list, audio: list):
        return self.prioritizer.fuse(project_id, semantic, keyword, audio)

    def prioritize_with_personality(self, project_id: int, semantic: list, keyword: list, audio: list):
        self.cognition.init_project(project_id)
        persona_profile = self.persona.get_persona(project_id)
        temperament = persona_profile.get("temperament", "calm")
        trend_score = 0.0
        if keyword:
            trend_score = sum(entry.get("trend_score", 0.0) for entry in keyword) / max(len(keyword), 1)
        ltm_state = self.ltm_report(project_id)
        drift_log = ltm_state.get("drift_log", [])
        drift_detected = bool(drift_log and drift_log[-1].get("drift_detected"))
        self.cognition.update_focus(project_id, temperament, trend_score, drift_detected)
        base = self.prioritizer.fuse(project_id, semantic, keyword, audio)
        prio = self.personality.apply_modifiers(project_id, base)
        prio = self.persona.apply_temperament(project_id, prio)
        prio = self.persona.committee_vote(project_id, prio)
        attention = self.cognition.attention.get(project_id, 1.0)
        attention_scaled = []
        for entry in prio:
            clone = dict(entry)
            clone["priority"] = round(clone.get("priority", 0.0) * attention, 6)
            clone["attention"] = attention
            attention_scaled.append(clone)
        attention_scaled.sort(key=lambda item: item.get("priority", 0.0), reverse=True)
        emotion_ctx = {
            "trend_score": max([clip.get("trending", 0.0) for clip in attention_scaled] or [0.0]),
            "drift_strength": self.cognition.drift.get(project_id).get("drift_strength", 0.0),
            "attention": attention,
            "temperament": persona_profile.get("temperament", "calm"),
        }
        emotion_state = self.emotion.compute(project_id, emotion_ctx)
        final = self.emotion.influence_priority(project_id, attention_scaled)
        self.cognition.push_memory(project_id, {"type": "emotion_state", "state": emotion_state})
        self.cognition.push_memory(
            project_id,
            {"type": "prioritization", "attention": attention, "top_candidates": final[:3]},
        )
        return final

    def recommend_clips(self, project_id: int, priority: list, limit: int = 3) -> list:
        """
        Simple recommender that surfaces the top-N prioritized clips.
        """
        if priority and not priority[0].get("_personality_applied"):
            priority = self.personality.apply_modifiers(project_id, priority)

        recommendations = []
        active_profile = self.personality.get_personality(project_id).get("key", "balanced")
        for entry in priority[:limit]:
            explanation = (
                f"priority={entry.get('priority', 0):.3f} "
                f"semantic={entry.get('semantic', 0):.3f} "
                f"keyword={entry.get('keyword', 0)} "
                f"trending={entry.get('trending', 0)} "
                f"audio={entry.get('audio', 0)}"
            )
            voice_payload = {"reason": explanation, "score": entry.get("priority", 0)}
            voice_explanation = self.persona.apply_voice(project_id, voice_payload)
            recommendations.append(
                {
                    "clip_id": entry.get("clip_id"),
                    "explanation": explanation,
                    "voice_explanation": voice_explanation,
                    "project_id": project_id,
                    "final_score": entry.get("priority", 0),
                    "personality": active_profile,
                }
            )
        self.cognition.push_memory(
            project_id,
            {"type": "recommendations", "items": recommendations, "personality": active_profile},
        )
        return recommendations

    def get_prioritizer_weights(self):
        return self.prioritizer.get_weights()

    def set_prioritizer_weights(self, weights: dict):
        return self.prioritizer.set_weights(weights)

    def ghost_run(self, project_id: int, clips: list, rounds: int = 1):
        return self.ghost.simulate_cycle(project_id, clips, rounds)

    def self_optimize(self, project_id: int, clips: list, rounds: int, ghost_rounds: int):
        return self.optimizer.run(project_id, clips, rounds, ghost_rounds)

    def get_self_opt_history(self, project_id: int):
        return self.optimizer.get_history(project_id)

    def ltm_snapshot(self, project_id: int):
        return self.ltm.snapshot(project_id)

    def ltm_detect_drift(self, project_id: int):
        return self.ltm.detect_drift(project_id)

    def ltm_consolidate(self, project_id: int):
        return self.ltm.consolidate(project_id)

    def ltm_report(self, project_id: int):
        return self.ltm.memory_report(project_id)

    def run_behavior_tree(self, project_id: int, ctx: dict):
        result = self.bt.run(project_id, ctx)
        self.cognition.push_memory(
            project_id,
            {"type": "behavior_tree", "success": result.get("success"), "trace": result.get("context", {}).get("trace", [])},
        )
        return result

    def plan(self, project_id: int, goal: str | None = None):
        result = self.planner.plan(project_id, goal)
        ctx = result.get("context", {})
        drift_strength = self.cognition.drift.get(project_id).get("drift_strength", 0.0)
        emotion_ctx = {
            "trend_score": ctx.get("trend_score", 0.5),
            "drift_strength": drift_strength,
            "attention": self.cognition.attention.get(project_id, 1.0),
            "temperament": self.persona.get_persona(project_id).get("temperament", "calm"),
        }
        emotion_state = self.emotion.compute(project_id, emotion_ctx)
        plan_actions = list(result.get("plan", []))
        if emotion_state.get("curiosity", 0) > 0.7 and "action:explore_new_clip" not in plan_actions:
            plan_actions.append("action:explore_new_clip")
        if emotion_state.get("stress", 0) > 0.6:
            plan_actions.insert(0, "action:stabilize_focus")
        result["plan"] = plan_actions
        result["emotion"] = emotion_state
        self.cognition.push_memory(
            project_id,
            {"type": "plan", "goal": result.get("goal"), "plan": plan_actions, "emotion": emotion_state},
        )
        return result

    def deliberate(self, project_id: int, scored_clips: list):
        return self.deliberation.deliberate(project_id, scored_clips)

    def brain_decide(self, project_id: int, clips: list):
        return self.brain.decide(project_id, clips)

    def status(self) -> dict:
        return {
            "mode": self.current_mode,
            "available_modes": list(self.modes.keys()),
            "available_personalities": list(self.personality.available_profiles().keys()),
        }
