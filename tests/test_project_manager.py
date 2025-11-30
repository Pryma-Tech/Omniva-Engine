from app.subsystems.projects import ProjectManager, ProjectStore


def test_project_store_defaults_and_roundtrip(tmp_path):
    store = ProjectStore(base_path=str(tmp_path))

    # Defaults when no file exists
    project = store.get(1)
    assert project["project_id"] == 1
    assert project["id"] == 1
    assert "creators" in project
    assert "clips" in project

    # Save and read back
    saved = store.save(2, {"creators": ["alice"], "keywords": ["omniva"]})
    loaded = store.get(2)
    assert loaded["creators"] == ["alice"]
    assert loaded["keywords"] == ["omniva"]
    assert saved == loaded


def test_project_store_list_ids_and_all(tmp_path):
    store = ProjectStore(base_path=str(tmp_path))
    store.save(3, {})
    store.save(1, {})

    ids = store.list_ids()
    assert ids == [1, 3]

    projects = store.list_all()
    returned_ids = sorted(p["project_id"] for p in projects)
    assert returned_ids == [1, 3]


def test_project_manager_seeds_default_project(tmp_path):
    store = ProjectStore(base_path=str(tmp_path))
    manager = ProjectManager(store=store)

    ids = store.list_ids()
    assert ids == [1]

    project = manager.get(1)
    assert project["project_id"] == 1
    assert "schedule" in project

