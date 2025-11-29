"""Subsystem registry (placeholder)."""
# TODO: Add lifecycle management and plugin discovery.

import logging
import os
from typing import Any, Dict

from app.core.event_bus import event_bus
from app.heartbeat.heartbeat_engine import HeartbeatEngine
from app.heartbeat.cron_tasks import CronTasks
from app.subsystems.autonomy.autonomy_kernel import AutonomyKernel
from app.subsystems.autonomy.loop_controller import LoopController
from app.subsystems.safety import CrisisProtocolEngine, GuardrailEngine, SafetyEngine
from app.subsystems.governance import GovernanceEngine, ProjectPolicy
from app.subsystems.federation import FederatedIntelligenceEngine, NicheClusterer
from app.subsystems.meta import EvolutionRules, MetaLearningEngine
from app.subsystems.orchestrator import HealthChecks, MasterOrchestrator
from app.subsystems.constellation import ConstellationEngine
from app.subsystems.strategy import EmergentStrategyEngine, NoveltyRules
from app.subsystems.selfmodel import IdentityRules, SelfModelEngine
from app.subsystems.soulbind import LoreCatalog, SoulBindEngine
from app.subsystems.archive import ArchiveEngine, EpochDetector
from app.subsystems.observatory import MetricsCalculator, ObservatoryEngine
from app.subsystems.etherlink import EtherlinkEngine, NodeRegistry, SyncProtocol
from app.nexus import Composer, NexusGateway
from app.sanctum import SanctumCommands, SanctumEngine
from app.forge import ForgeEngine, PluginLoader

logger = logging.getLogger("omniva_v2")


class SubsystemRegistry:
    """Simple in-memory registry for subsystem instances."""

    def __init__(self) -> None:
        self._registry: Dict[str, Any] = {}
        logger.info("SubsystemRegistry initialized (placeholder).")
        self.crisis = CrisisProtocolEngine(self)
        self.guardrails = GuardrailEngine(self)
        self.safety = SafetyEngine(self)
        self.policy_model = ProjectPolicy()
        self.governance = GovernanceEngine(self, self.policy_model)
        self.clusterer = NicheClusterer()
        self.federation = FederatedIntelligenceEngine(self, self.clusterer)
        self.meta_rules = EvolutionRules()
        self.meta = MetaLearningEngine(self, self.meta_rules)
        self.health = HealthChecks(self)
        self.orchestrator = MasterOrchestrator(self, self.health)
        self.cron_tasks = CronTasks(self)
        self.heartbeat = HeartbeatEngine(self, self.cron_tasks)
        self.eventbus = event_bus
        self.constellation = ConstellationEngine(self)
        self.autonomy_controller = LoopController()
        self.autonomy = AutonomyKernel(self, self.autonomy_controller)
        self.novelty_rules = NoveltyRules()
        self.strategy = EmergentStrategyEngine(self, self.novelty_rules)
        self.identity_rules = IdentityRules()
        self.selfmodel = SelfModelEngine(self, self.identity_rules)
        self.lore_catalog = LoreCatalog()
        self.soul = SoulBindEngine(self, self.lore_catalog)
        self.epoch_detector = EpochDetector()
        self.archive = ArchiveEngine(self, self.epoch_detector)
        self.metrics = MetricsCalculator()
        self.observatory = ObservatoryEngine(self, self.metrics)
        self.composer = Composer(self)
        self.nexus = NexusGateway(self, self.composer)
        self.sanctum_commands = SanctumCommands(self)
        self.sanctum = SanctumEngine(self, self.sanctum_commands)
        self.forge_loader = PluginLoader()
        self.forge = ForgeEngine(self)
        self.node_registry = NodeRegistry()
        etherlink_token = os.getenv("ETHERLINK_TOKEN", "CHANGE_ME")
        self.sync_protocol = SyncProtocol(self, auth_token=etherlink_token)
        self.etherlink = EtherlinkEngine(self, self.node_registry, self.sync_protocol)
        self.register_subsystem("soul", self.soul)
        self.register_subsystem("archive", self.archive)
        self.register_subsystem("observatory", self.observatory)
        self.register_subsystem("nexus", self.nexus)
        self.register_subsystem("sanctum", self.sanctum)
        self.register_subsystem("forge", self.forge)
        self.register_subsystem("etherlink", self.etherlink)

    def register_subsystem(self, name: str, instance: Any) -> None:
        logger.info("Registering subsystem %s (placeholder)", name)
        self._registry[name] = instance

    def get_subsystem(self, name: str) -> Any:
        return self._registry.get(name)

    def list_subsystems(self) -> Dict[str, str]:
        return {name: instance.__class__.__name__ for name, instance in self._registry.items()}


registry = SubsystemRegistry()


def register_subsystem(name: str, instance: Any) -> None:
    registry.register_subsystem(name, instance)


def get_subsystem(name: str) -> Any:
    return registry.get_subsystem(name)


def list_subsystems() -> Dict[str, str]:
    return registry.list_subsystems()


def initialize_all() -> None:
    """Call initialize on all registered subsystems if available."""
    for subsystem in registry._registry.values():
        initialize = getattr(subsystem, "initialize", None)
        if callable(initialize):
            initialize()
