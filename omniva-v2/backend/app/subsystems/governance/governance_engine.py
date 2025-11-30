"""Governance enforcement engine."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/governance/governance_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/governance/governance_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/governance/governance_engine with cognitive telemetry.


from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, List, Tuple


class GovernanceEngine:
    """Apply project policies and constraints before executing actions."""

    def __init__(self, registry, policy_model) -> None:
        self.registry = registry
        self.policy_model = policy_model
        self.post_history: Dict[int, List[datetime]] = {}

    def record_post(self, project_id: int) -> None:
        self.post_history.setdefault(project_id, []).append(datetime.utcnow())

    def _policy(self, project_id: int) -> Dict:
        return self.policy_model.get_policy(project_id)

    def check_platform(self, project_id: int, clip: Dict) -> Tuple[bool, str | None]:
        policy = self._policy(project_id)
        platform = clip.get("platform", "")
        if platform in policy["blocked_platforms"]:
            return False, f"Platform '{platform}' blocked by governance policy"
        if policy["allowed_platforms"] and platform not in policy["allowed_platforms"]:
            return False, f"Platform '{platform}' not allowed"
        return True, None

    def check_creator(self, project_id: int, clip: Dict) -> Tuple[bool, str | None]:
        policy = self._policy(project_id)
        creator = clip.get("creator", "")
        if creator in policy["blocked_creators"]:
            return False, f"Creator '{creator}' blocked"
        if policy["allowed_creators"] and creator not in policy["allowed_creators"]:
            return False, f"Creator '{creator}' not allowed"
        return True, None

    def check_post_limits(self, project_id: int) -> Tuple[bool, str | None]:
        policy = self._policy(project_id)
        history = self.post_history.get(project_id, [])
        now = datetime.utcnow()
        today_posts = [stamp for stamp in history if (now - stamp).days == 0]
        if len(today_posts) >= policy["max_daily_posts"]:
            return False, "Daily posting limit reached"
        if history:
            delta = now - history[-1]
            if delta < timedelta(minutes=policy["min_minutes_between_posts"]):
                return False, "Need additional cooldown before next post"
        return True, None

    def check_reuse_limits(self, project_id: int, clip: Dict) -> Tuple[bool, str | None]:
        policy = self._policy(project_id)
        clip_id = clip.get("clip_id")
        if not clip_id or policy["max_clip_reuse_per_week"] <= 0:
            return True, None
        intel = self.registry.get_subsystem("intelligence")
        ltm = intel.ltm.memory_report(project_id) if hasattr(intel, "ltm") else intel.ltm_report(project_id)
        snapshots = ltm.get("snapshots", [])
        reuse_count = 0
        one_week = datetime.utcnow() - timedelta(days=7)
        for snap in snapshots:
            stamp = datetime.fromisoformat(snap.get("time")) if snap.get("time") else None
            if stamp and stamp < one_week:
                continue
            if snap.get("clip_id") == clip_id:
                reuse_count += 1
        if reuse_count >= policy["max_clip_reuse_per_week"]:
            return False, "Clip reuse limit exceeded"
        return True, None

    def enforce(self, project_id: int, decision: Dict) -> Tuple[bool, str | None]:
        clip = decision.get("chosen_clip") or decision.get("final_choice")
        if not clip:
            return False, "No chosen clip to enforce policy with"
        checks = [
            self.check_platform(project_id, clip),
            self.check_creator(project_id, clip),
            self.check_post_limits(project_id),
            self.check_reuse_limits(project_id, clip),
        ]
        for ok, reason in checks:
            if not ok:
                return False, reason
        policy = self._policy(project_id)
        if policy["require_manual_review"]:
            return False, "Manual review required before execution"
        return True, None

    def snapshot(self) -> Dict[str, Dict]:
        """
        Provide a lightweight governance overview for the Nexus composer.
        """
        policies = {pid: policy for pid, policy in self.policy_model.policies.items()}
        history = {
            pid: [stamp.isoformat() for stamp in stamps[-5:]]
            for pid, stamps in self.post_history.items()
        }
        return {
            "policies": policies,
            "recent_posts": history,
        }
