"""Smoke tests for heartbeat + orchestrator routes."""

from fastapi.testclient import TestClient

from backend.app.main import app
from app.core.registry import registry

client = TestClient(app)
CONTROL_HEADERS = {"X-Omniva-Control-Token": "test-control"}


def test_heartbeat_start_stop_cycle():
    start_resp = client.post("/heartbeat/start", headers=CONTROL_HEADERS)
    assert start_resp.status_code == 200
    assert start_resp.json()["status"] in {"heartbeat_started", "already_running"}

    status_resp = client.get("/heartbeat/status")
    assert status_resp.status_code == 200
    assert "running" in status_resp.json()

    stop_resp = client.post("/heartbeat/stop", headers=CONTROL_HEADERS)
    assert stop_resp.status_code == 200
    assert stop_resp.json()["status"] == "heartbeat_stopped"


def test_orchestrator_lifecycle_and_health():
    start_resp = client.post("/orchestrator/start_all", headers=CONTROL_HEADERS)
    assert start_resp.status_code == 200
    assert start_resp.json()["status"] == "all_projects_started"

    cycle_resp = client.get("/orchestrator/cycle")
    assert cycle_resp.status_code == 200
    cycle_body = cycle_resp.json()
    assert "health" in cycle_body
    assert isinstance(cycle_body.get("federation"), dict)

    health_resp = client.get("/orchestrator/health")
    assert health_resp.status_code == 200
    assert "projects" in health_resp.json()

    stop_resp = client.post("/orchestrator/stop_all", headers=CONTROL_HEADERS, json={})
    assert stop_resp.status_code == 200
    assert stop_resp.json()["status"] == "all_projects_stopped"


def test_system_health_probe():
    resp = client.get("/healthz")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert isinstance(body["projects"], list)
