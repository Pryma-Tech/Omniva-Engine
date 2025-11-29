"""Temperament profiles for Omniva personas."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/intelligence/persona/temperaments.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/intelligence/persona/temperaments with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/intelligence/persona/temperaments with cognitive telemetry.


TEMPERAMENTS = {
    "calm": {
        "tone": "Calm and measured.",
        "risk_factor": 0.8,
        "excitability": 0.3,
        "stability_bonus": 0.2,
    },
    "energetic": {
        "tone": "Fast, hype, and energetic.",
        "risk_factor": 1.2,
        "excitability": 0.9,
        "stability_bonus": 0.0,
    },
    "analytical": {
        "tone": "Highly logical and detail-oriented.",
        "risk_factor": 0.9,
        "excitability": 0.2,
        "stability_bonus": 0.3,
    },
    "aggressive": {
        "tone": "Direct, bold, and decisive.",
        "risk_factor": 1.4,
        "excitability": 0.7,
        "stability_bonus": 0.0,
    },
    "playful": {
        "tone": "Light-hearted, curious, and creative.",
        "risk_factor": 1.0,
        "excitability": 1.0,
        "stability_bonus": 0.1,
    },
}
