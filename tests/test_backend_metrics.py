from backend.app.main import app
from fastapi.testclient import TestClient


def test_healthz_and_metrics_basic_shape():
    client = TestClient(app)

    health = client.get("/healthz")
    assert health.status_code == 200
    body = health.json()
    assert "status" in body
    assert "heartbeat_running" in body
    assert "projects" in body

    metrics = client.get("/metrics")
    assert metrics.status_code == 200
    mbody = metrics.json()
    assert "projects" in mbody
    assert "heartbeat_running" in mbody
    assert "health" in mbody

