from fastapi.testclient import TestClient
from server.src.app.main import app

client = TestClient(app)

def test_register_and_heartbeat():
    reg = client.post("/api/v1/agents/register", json={"hostname": "lab1", "platform": "linux"})
    assert reg.status_code == 200
    agent_id = reg.json()["agent_id"]

    hb = client.post(f"/api/v1/agents/{agent_id}/heartbeat", json={"uptime": 10, "load": 0.1})
    assert hb.status_code == 200

def test_get_tasks_empty_then_create():
    reg = client.post("/api/v1/agents/register", json={"hostname": "lab2", "platform": "linux"})
    agent_id = reg.json()["agent_id"]

    empty = client.get(f"/api/v1/agents/{agent_id}/tasks")
    assert empty.status_code == 200
    assert empty.json() == []

    # create benign task (auth disabled by default)
    create = client.post("/api/v1/tasks", json={"agent_ids": [agent_id], "type": "collect-metrics"})
    assert create.status_code == 201

    tasks = client.get(f"/api/v1/agents/{agent_id}/tasks")
    assert tasks.status_code == 200
    assert len(tasks.json()) == 1
