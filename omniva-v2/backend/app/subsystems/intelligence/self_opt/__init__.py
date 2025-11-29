"""Meta-optimizer subsystem for the intelligence layer."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/intelligence/self_opt/__init__.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/intelligence/self_opt/__init__ with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/intelligence/self_opt/__init__ with cognitive telemetry.


from .optimizer_engine import MetaOptimizerEngine
from .opt_store import SelfOptStore

__all__ = ["MetaOptimizerEngine", "SelfOptStore"]
