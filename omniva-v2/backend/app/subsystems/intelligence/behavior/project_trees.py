"""Project-specific behavior trees for the intelligence subsystem."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/intelligence/behavior/project_trees.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/intelligence/behavior/project_trees with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/intelligence/behavior/project_trees with cognitive telemetry.


from __future__ import annotations

from typing import Any, Dict, List

from app.core.registry import registry

from .nodes import ActionNode, ConditionNode, SelectorNode, SequenceNode


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _project(ctx: Dict[str, Any]) -> Dict[str, Any]:
    project = ctx.get("project") or {}
    project.setdefault("id", 0)
    return project


def _append(ctx: Dict[str, Any], key: str, value: Any) -> None:
    ctx.setdefault("logs", []).append({"step": key, "value": value})


def check_autonomous(ctx: Dict[str, Any]) -> bool:
    project = _project(ctx)
    result = bool(project.get("autonomous", False))
    _append(ctx, "check_autonomous", result)
    return result


def discover_clips(ctx: Dict[str, Any]) -> bool:
    project = _project(ctx)
    discover = registry.get_subsystem("discovery")
    links: List[str] = []
    if discover:
        try:
            links = discover.discover_new_posts(project["id"])
        except Exception as exc:  # pragma: no cover - defensive
            _append(ctx, "discover_error", str(exc))
    if not links:
        links = ctx.get("links") or project.get("seed_links", [])
    ctx["links"] = links
    _append(ctx, "discover_links", links)
    return len(links) > 0


def download_clips(ctx: Dict[str, Any]) -> bool:
    project = _project(ctx)
    candidates: List[Dict[str, Any]] = []
    for link in ctx.get("links", []):
        local_path = f"/tmp/ghost_clip_{abs(hash((project['id'], link)))}.mp4"
        candidates.append({"id": link, "local": local_path, "meta": {"link": link}})
    ctx["candidates"] = candidates
    _append(ctx, "download_candidates", candidates)
    return len(candidates) > 0


def analyze_clips(ctx: Dict[str, Any]) -> bool:
    transcriber = registry.get_subsystem("transcription")
    analysis = registry.get_subsystem("analysis")
    clips: List[Dict[str, Any]] = []
    for candidate in ctx.get("candidates", []):
        transcript = candidate.get("transcript")
        if not transcript and transcriber and hasattr(transcriber, "transcribe"):
            try:
                transcript = "synthetic transcript"
            except Exception:  # pragma: no cover
                transcript = "synthetic transcript"
        transcript = transcript or candidate.get("id", "")
        summary = {"keywords": [], "score": 0.0}
        if analysis and hasattr(analysis, "analyze"):
            try:
                summary = analysis.analyze(transcript)
            except Exception as exc:  # pragma: no cover
                _append(ctx, "analysis_error", str(exc))
        clips.append(
            {
                "id": candidate["id"],
                "transcript": transcript,
                "analysis": summary,
                "meta": candidate.get("meta", {}),
            }
        )
    ctx["clips"] = clips
    _append(ctx, "analyzed_clips", clips)
    return len(clips) > 0


def score_clips(ctx: Dict[str, Any]) -> bool:
    intel = registry.get_subsystem("intelligence")
    project = _project(ctx)
    if intel is None:
        return False
    sem = intel.semantic_rank(project["id"], ctx.get("clips", []))
    kw = intel.keyword_ranker.rank(project["id"], ctx.get("clips", []))
    audio = [{"clip_id": clip.get("id"), "audio_score": 0} for clip in ctx.get("clips", [])]
    scored = intel.prioritize_with_personality(project["id"], sem, kw, audio)
    ctx["scored"] = scored
    _append(ctx, "scored", scored)
    return len(scored) > 0


def recommend_clips(ctx: Dict[str, Any]) -> bool:
    intel = registry.get_subsystem("intelligence")
    project = _project(ctx)
    if intel is None:
        return False
    recommendations = intel.recommend_clips(project["id"], ctx.get("scored", []), limit=3)
    ctx["recommendations"] = recommendations
    _append(ctx, "recommendations", recommendations)
    return len(recommendations) > 0


def apply_adaptive_rules(ctx: Dict[str, Any]) -> bool:
    intel = registry.get_subsystem("intelligence")
    project = _project(ctx)
    if not intel:
        return True
    personality = intel.personality.get_personality(project["id"])
    ctx.setdefault("adaptive", {})["profile"] = personality.get("key")
    ctx["adaptive"]["post_aggression"] = personality.get("post_aggression")
    _append(ctx, "adaptive_rules", ctx["adaptive"])
    return True


def decide_action(ctx: Dict[str, Any]) -> bool:
    intel = registry.get_subsystem("intelligence")
    project = _project(ctx)
    aggression = 1.0
    if intel:
        aggression = intel.personality.post_aggression(project["id"])
    decision = "publish" if aggression > 1.2 else "schedule"
    ctx["decision"] = decision
    ctx.setdefault("notes", {})["aggression"] = aggression
    _append(ctx, "decision", decision)
    return True


# ---------------------------------------------------------------------------
# Tree builder
# ---------------------------------------------------------------------------

def get_project_tree(project_id: int):
    """Return a behavior tree tailored to the project's personality."""

    intel = registry.get_subsystem("intelligence")
    personality_key = "balanced"
    if intel:
        personality_key = intel.personality.get_personality(project_id).get("key", "balanced")

    base_pipeline = SequenceNode(
        ConditionNode(check_autonomous, name="CheckAutonomous"),
        ActionNode(discover_clips, name="Discover"),
        ActionNode(download_clips, name="Download"),
        ActionNode(analyze_clips, name="Analyze"),
        ActionNode(score_clips, name="Score"),
        ActionNode(recommend_clips, name="Recommend"),
        ActionNode(decide_action, name="Decide"),
        name="BaseSequence",
    )

    if personality_key == "growth_spiral":
        return SequenceNode(ActionNode(apply_adaptive_rules, name="Adaptive"), base_pipeline, name="GrowthTree")
    if personality_key == "viral_hunter":
        # Viral hunters attempt to skip download step if cached clips exist.
        cached_path = SelectorNode(
            ActionNode(download_clips, name="DownloadFresh"),
            ActionNode(analyze_clips, name="AnalyzeCached"),
            name="AcquisitionSelector",
        )
        return SequenceNode(
            ConditionNode(check_autonomous, name="CheckAutonomous"),
            ActionNode(discover_clips, name="Discover"),
            cached_path,
            ActionNode(score_clips, name="Score"),
            ActionNode(recommend_clips, name="Recommend"),
            ActionNode(decide_action, name="Decide"),
            name="ViralTree",
        )

    return base_pipeline
