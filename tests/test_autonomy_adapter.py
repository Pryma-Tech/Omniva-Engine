from app.core.registry import build_registry


def test_autonomy_adapter_start_stop_and_flags():
    registry = build_registry()
    autonomy = registry.autonomy
    project_id = 1

    assert not autonomy.is_running(project_id)

    started = autonomy.start_project(project_id)
    assert started["status"] in {"started", "already_running"}
    assert autonomy.is_running(project_id)

    paused = autonomy.pause_project(project_id)
    assert paused["status"] in {"paused", "not_running"}

    resumed = autonomy.resume_project(project_id)
    assert resumed["status"] in {"resumed", "not_running"}

    stopped = autonomy.stop_project(project_id)
    assert stopped["status"] == "stopped"
    assert not autonomy.is_running(project_id)


def test_autonomy_adapter_micro_macro_iterations():
    registry = build_registry()
    autonomy = registry.autonomy
    project_id = 1

    autonomy.start_project(project_id)

    micro = autonomy.run_micro_iteration(project_id)
    assert micro["status"] == "ok"
    assert micro["loop"] == "micro"

    macro = autonomy.run_macro_iteration(project_id)
    assert macro["status"] in {"ok", "intel_or_projects_unavailable"}
    assert macro["loop"] == "macro"

