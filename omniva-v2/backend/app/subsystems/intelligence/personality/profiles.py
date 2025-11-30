"""Static definitions for agent personality strategy profiles."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/intelligence/personality/profiles.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/intelligence/personality/profiles with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/intelligence/personality/profiles with cognitive telemetry.


PERSONALITY_PROFILES = {
    "balanced": {
        "description": "Hybrid mode — stable and reliable.",
        "prio_mod": {"semantic": 1.0, "keyword": 1.0, "trending": 1.0, "audio": 1.0},
        "post_aggression": 1.0,
        "niche_strictness": 0.5,
        "drift_tolerance": 0.05,
        "editorial_style": "neutral",
    },
    "viral_hunter": {
        "description": "Aggressive viral-seeking mode.",
        "prio_mod": {"semantic": 0.9, "keyword": 1.2, "trending": 1.4, "audio": 1.3},
        "post_aggression": 1.5,
        "niche_strictness": 0.3,
        "drift_tolerance": 0.1,
        "editorial_style": "flashy",
    },
    "evergreen": {
        "description": "Stable, timeless content focus.",
        "prio_mod": {"semantic": 1.3, "keyword": 1.1, "trending": 0.8, "audio": 0.8},
        "post_aggression": 0.7,
        "niche_strictness": 0.8,
        "drift_tolerance": 0.03,
        "editorial_style": "timeless",
    },
    "brand_guardian": {
        "description": "Strong niche identity and brand consistency.",
        "prio_mod": {"semantic": 1.1, "keyword": 1.3, "trending": 0.9, "audio": 0.7},
        "post_aggression": 0.8,
        "niche_strictness": 0.9,
        "drift_tolerance": 0.02,
        "editorial_style": "premium",
    },
    "growth_spiral": {
        "description": "Adaptive personality that evolves with performance.",
        "prio_mod": {"semantic": 1.0, "keyword": 1.0, "trending": 1.0, "audio": 1.0},
        "post_aggression": 1.2,
        "niche_strictness": 0.4,
        "drift_tolerance": 0.05,
        "editorial_style": "experimental",
        "adaptive": True,
    },
}
