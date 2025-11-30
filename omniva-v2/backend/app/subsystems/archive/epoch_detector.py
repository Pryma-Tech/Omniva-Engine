# DONE(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/archive/epoch_detector.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/archive/epoch_detector with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/archive/epoch_detector with cognitive telemetry.

from statistics import mean


class EpochDetector:
    """
    Creates 'epochs' based on:
      - emotional shifts
      - drift volatility
      - federated global changes
      - meta-learning transitions
    """

    def detect_epoch(self, history_window):
        if not history_window:
            return "genesis"

        avg_stress = mean([h["stress"] for h in history_window])
        avg_drift = mean([h["drift"] for h in history_window])

        if avg_stress > 0.7:
            return "epoch_of_tension"
        if avg_drift > 0.6:
            return "epoch_of_wandering"
        if avg_stress < 0.3 and avg_drift < 0.3:
            return "epoch_of_clarity"

        return "epoch_of_flux"
