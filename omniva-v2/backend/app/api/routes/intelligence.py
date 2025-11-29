"""Intelligence engine API routes."""

from fastapi import APIRouter, HTTPException

from app.core.registry import registry

router = APIRouter()


def _engine():
    return registry.get_subsystem("intelligence")


@router.get("/status")
async def get_status() -> dict:
    return _engine().status()


@router.post("/mode/{mode}")
async def set_mode(mode: str) -> dict:
    return _engine().set_mode(mode)


@router.get("/posting-time/{project_id}")
async def get_posting_time(project_id: int) -> dict:
    return _engine().choose_posting_time(project_id)


@router.get("/posting-stats/{project_id}")
async def get_posting_stats(project_id: int) -> dict:
    return _engine().get_posting_stats(project_id)


@router.post("/apply-schedule/{project_id}")
async def apply_schedule(project_id: int) -> dict:
    intel = _engine()
    scheduler = registry.get_subsystem("scheduler")
    recommendation = intel.choose_posting_time(project_id)
    hour = recommendation.get("recommended_hour", 18)
    cron = f"0 {hour} * * *"
    config = scheduler.configure_project(project_id, enabled=True, cron=cron)
    return {
        "project_id": project_id,
        "recommended": recommendation,
        "applied_cron": cron,
        "scheduler_config": config,
    }


@router.get("/trending/{project_id}")
async def get_trending(project_id: int) -> dict:
    intel = _engine()
    return intel.get_trending_keywords(project_id)


@router.post("/semantic-rank/{project_id}")
async def semantic_rank(project_id: int, clips: list) -> list:
    intel = _engine()
    return intel.semantic_rank(project_id, clips)


@router.get("/audio-trends/{project_id}")
async def get_audio_trends(project_id: int) -> dict:
    intel = _engine()
    return intel.get_audio_trends(project_id)


@router.post("/audio-match/{project_id}")
async def audio_match(project_id: int, clip_meta: dict) -> dict:
    intel = _engine()
    return intel.audio_trends.match(project_id, clip_meta)


@router.post("/prioritize/{project_id}")
async def prioritize(project_id: int, payload: dict) -> list:
    intel = _engine()
    return intel.prioritize_clips(
        project_id,
        payload.get("semantic", []),
        payload.get("keyword", []),
        payload.get("audio", []),
    )


@router.get("/prioritizer/weights")
async def get_prioritizer_weights() -> dict:
    intel = _engine()
    return intel.get_prioritizer_weights()


@router.post("/prioritizer/weights")
async def set_prioritizer_weights(new: dict) -> dict:
    intel = _engine()
    return intel.set_prioritizer_weights(new)


@router.post("/ghost-run/{project_id}")
async def ghost_run(project_id: int, payload: dict) -> dict:
    """
    Run offline ghost simulations without touching production resources.

    Expected payload:
    {
        "clips": [{ "id": "c1", "transcript": "...", "meta": {...} }],
        "rounds": 3
    }
    """

    intel = _engine()
    rounds = payload.get("rounds", 1)
    return intel.ghost_run(project_id, payload.get("clips", []), rounds)


@router.post("/self-opt/{project_id}")
async def run_self_opt(project_id: int, payload: dict) -> dict:
    intel = _engine()
    rounds = payload.get("rounds", 5)
    ghost_rounds = payload.get("ghost_rounds", 5)
    clips = payload.get("clips", [])
    return intel.self_optimize(project_id, clips, rounds, ghost_rounds)


@router.get("/self-opt/history/{project_id}")
async def get_self_opt_history(project_id: int) -> dict:
    intel = _engine()
    return intel.get_self_opt_history(project_id)


@router.post("/ltm/snapshot/{project_id}")
async def ltm_snapshot(project_id: int) -> dict:
    intel = _engine()
    return intel.ltm_snapshot(project_id)


@router.post("/ltm/drift/{project_id}")
async def ltm_drift(project_id: int) -> dict:
    intel = _engine()
    return intel.ltm_detect_drift(project_id)


@router.post("/ltm/consolidate/{project_id}")
async def ltm_consolidate(project_id: int) -> dict:
    intel = _engine()
    return intel.ltm_consolidate(project_id)


@router.get("/ltm/report/{project_id}")
async def ltm_report(project_id: int) -> dict:
    intel = _engine()
    return intel.ltm_report(project_id)


@router.get("/personality/profiles")
async def list_personality_profiles() -> dict:
    intel = _engine()
    return intel.personality.available_profiles()


@router.get("/personality/{project_id}")
async def get_personality(project_id: int) -> dict:
    intel = _engine()
    return intel.personality.get_personality(project_id)


@router.post("/personality/{project_id}/{key}")
async def set_personality(project_id: int, key: str) -> dict:
    intel = _engine()
    try:
        return intel.personality.set_personality(project_id, key)
    except ValueError as exc:  # pragma: no cover - user error feedback
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/persona/{project_id}")
async def get_persona(project_id: int) -> dict:
    intel = _engine()
    return intel.persona.get_persona(project_id)


@router.post("/persona/{project_id}")
async def set_persona(project_id: int, payload: dict) -> dict:
    intel = _engine()
    payload = payload or {}
    try:
        return intel.persona.set_persona(
            project_id,
            payload.get("temperament", "calm"),
            payload.get("voice", "minimal"),
            payload.get("committee", []),
        )
    except ValueError as exc:  # pragma: no cover - validation feedback
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/behavior/run/{project_id}")
async def run_behavior_tree(project_id: int, payload: dict) -> dict:
    intel = _engine()
    payload = payload or {}
    ctx = payload.get("context", {}) or {}
    project = payload.get("project") or {}
    project.setdefault("id", project_id)
    if "autonomous" not in project:
        project["autonomous"] = payload.get("autonomous", True)
    ctx["project"] = project
    if "links" in payload:
        ctx["links"] = payload["links"]
    if "seed_links" in payload:
        ctx["project"]["seed_links"] = payload["seed_links"]
    return intel.run_behavior_tree(project_id, ctx)


@router.get("/planner/{project_id}/{goal}")
async def run_planner(project_id: int, goal: str) -> dict:
    intel = _engine()
    return intel.plan(project_id, goal)


@router.post("/cognition/attention/{project_id}/{value}")
async def set_attention(project_id: int, value: float) -> dict:
    intel = _engine()
    updated = intel.cognition.set_attention(project_id, float(value))
    return {"project_id": project_id, "attention": updated}


@router.get("/cognition/memory/{project_id}")
async def get_memory(project_id: int, recent: int = 5):
    intel = _engine()
    return intel.cognition.recent_memory(project_id, recent)


@router.post("/cognition/update_focus/{project_id}")
async def update_focus(project_id: int, payload: dict) -> dict:
    intel = _engine()
    payload = payload or {}
    temperament = payload.get("temperament", "calm")
    trend_score = float(payload.get("trend_score", 0.5))
    drift_detected = bool(payload.get("drift_detected", False))
    return intel.cognition.update_focus(project_id, temperament, trend_score, drift_detected)


@router.post("/deliberate/{project_id}")
async def run_deliberation(project_id: int, payload: dict) -> dict:
    intel = _engine()
    scored = payload.get("scored", []) if payload else []
    return intel.deliberate(project_id, scored)


@router.get("/emotion/{project_id}")
async def get_emotion(project_id: int) -> dict:
    intel = _engine()
    return intel.emotion_model.get(project_id)


@router.post("/brain/{project_id}")
async def brain_decision(project_id: int, payload: dict) -> dict:
    """
    payload = { "clips": [...] }
    """
    intel = _engine()
    clips = payload.get("clips", []) if payload else []
    return intel.brain_decide(project_id, clips)
