from app.subsystems.scheduler import ScheduleStore, SchedulerSubsystem


def test_schedule_store_roundtrip(tmp_path):
    store = ScheduleStore(base_dir=str(tmp_path))
    proj_id = 42

    default_cfg = store.load(proj_id)
    assert default_cfg["project_id"] == proj_id
    assert "cron" in default_cfg

    saved = store.save(proj_id, {"enabled": True, "cron": "0 12 * * *"})
    assert saved["enabled"] is True
    assert saved["cron"] == "0 12 * * *"

    loaded = store.load(proj_id)
    assert loaded == saved


def test_scheduler_subsystem_configure_and_get(tmp_path):
    store = ScheduleStore(base_dir=str(tmp_path))
    scheduler = SchedulerSubsystem(store=store)
    proj_id = 7

    cfg = scheduler.configure_project(proj_id, enabled=True, cron="5 4 * * *")
    assert cfg["enabled"] is True
    assert cfg["cron"] == "5 4 * * *"

    got = scheduler.get_project_schedule(proj_id)
    assert got == cfg
