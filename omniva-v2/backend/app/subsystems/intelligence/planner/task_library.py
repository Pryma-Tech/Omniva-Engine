"""Task and method library definitions for HTN planning."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/intelligence/planner/task_library.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/intelligence/planner/task_library with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/intelligence/planner/task_library with cognitive telemetry.


from __future__ import annotations

from .htn_core import HTNMethod, HTNTask


def build_task_library():
    tasks = {
        "improve_growth": HTNTask("improve_growth"),
        "increase_consistency": HTNTask("increase_consistency"),
        "chase_trend": HTNTask("chase_trend"),
        "recover_drift": HTNTask("recover_drift"),
    }

    methods = [
        HTNMethod(
            "growth_spiral_method",
            "improve_growth",
            lambda ctx: ctx.get("personality") == "growth_spiral",
            [
                "chase_trend",
                "increase_consistency",
                "action:boost_upload_frequency",
            ],
        ),
        HTNMethod(
            "viral_strategy",
            "improve_growth",
            lambda ctx: ctx.get("personality") == "viral_hunter",
            [
                "chase_trend",
                "action:increase_trending_weight",
                "action:aggressive_posting",
            ],
        ),
        HTNMethod(
            "balanced_growth_method",
            "improve_growth",
            lambda ctx: ctx.get("personality") == "balanced",
            [
                "increase_consistency",
                "action:normal_posting",
            ],
        ),
        HTNMethod(
            "drift_recovery_method",
            "recover_drift",
            lambda ctx: ctx.get("drift_detected", False),
            [
                "action:ltm_snapshot",
                "action:reduce_trending_weight",
                "action:boost_semantic_weight",
            ],
        ),
        HTNMethod(
            "trend_engage",
            "chase_trend",
            lambda ctx: ctx.get("trend_score", 0) > 0.5,
            [
                "action:increase_trend_bias",
                "action:prioritize_trending_audio",
            ],
        ),
        HTNMethod(
            "consistency_method",
            "increase_consistency",
            lambda ctx: True,
            [
                "action:increase_keyword_weight",
                "action:stabilize_post_schedule",
            ],
        ),
    ]

    return tasks, methods
