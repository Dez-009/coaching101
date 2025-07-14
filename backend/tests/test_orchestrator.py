# Tests for orchestrator service
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Admin Orchestrator running"

def test_execute_query():
    payload = {"user_id": "1", "query": "show data"}
    resp = client.post("/orchestrator/query", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert len(data["results"]) == 1
