from statistics import mean  # noqa: F401  # reserved for future composite metrics


class NoveltyRules:
    """
    Deterministic rules for generating novel, emergent creative strategies.
    Combines:
      - semantic clusters
      - constellation consensus patterns
      - trend accelerations
      - drift & emotional states
      - cross-project similarity signals
    """

    def synthesize_theme(self, semantic_similarities):
        """
        Given niche similarity pairs, derive a possible cross-niche theme.
        """
        if not semantic_similarities:
            return "general"

        # Pick the highest similarity pair
        top = max(semantic_similarities, key=lambda item: item.get("similarity", 0.0))

        # Generate deterministic hybrid theme
        a = top.get("a", "alpha")
        b = top.get("b", "beta")
        theme = f"fusion_{a}_{b}"
        return theme

    def synthesize_posting_tactic(self, trend_score, drift_val, emotion_stress):
        """
        Determine a tactical suggestion based on system-wide signals.
        """
        if trend_score > 0.7 and emotion_stress < 0.5:
            return "double_down_trending"

        if drift_val > 0.6:
            return "reset_focus_longform"

        if emotion_stress > 0.6:
            return "slow_posting_recovery"

        return "balanced_growth"

    def propose_collab(self, similarity_pairs):
        """
        If two projects are highly similar, propose a collaboration.
        """
        if not similarity_pairs:
            return None
        top = max(similarity_pairs, key=lambda item: item.get("similarity", 0.0))
        if top.get("similarity", 0.0) > 0.7:
            return {"projects": [top.get("a"), top.get("b")], "collab_type": "cross_niche_series"}
        return None
