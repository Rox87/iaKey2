import pytest
from fastapi.testclient import TestClient
from backend.main import app
import backend.db as db
import os

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db(monkeypatch):
    db.DB_PATH = "test_config.db"
    if os.path.exists(db.DB_PATH):
        os.remove(db.DB_PATH)
    db.init_db()

    # Mock keyboard methods so tests don't require root on Linux
    def mock_reload():
        pass

    import backend.hotkeys as hk
    monkeypatch.setattr(hk, "reload_hotkeys", mock_reload)

    yield
    if os.path.exists(db.DB_PATH):
        os.remove(db.DB_PATH)

def test_create_and_get_model():
    response = client.post("/api/models", json={
        "name": "Test Model",
        "base_url": "http://localhost",
        "model_name": "test-gpt",
        "api_key": "test_key"
    })
    assert response.status_code == 200
    model_id = response.json()["id"]

    response2 = client.get("/api/models")
    assert len(response2.json()) == 1
    assert response2.json()[0]["name"] == "Test Model"

def test_create_hotkey():
    client.post("/api/models", json={
        "name": "Test Model",
        "base_url": "http://localhost",
        "model_name": "test-gpt",
        "api_key": "test_key"
    })

    response = client.post("/api/hotkeys", json={
        "keys": "ctrl+a",
        "prefix": "Test Prefix",
        "model_id": 1
    })
    assert response.status_code == 200

    response2 = client.get("/api/hotkeys")
    assert len(response2.json()) == 1
    assert response2.json()[0]["keys"] == "ctrl+a"
