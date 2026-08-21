from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import app

client = TestClient(app)
settings = get_settings()

def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["app_name"] == settings.app_name
    assert data["environment"] == settings.environment

def test_root() -> None:
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["message"] == "RAG API is running"

def test_blank_question_returns_422() -> None:
    response = client.post(
        "/ask",
        json={
            "question": "       ",
        },
    )

    assert response.status_code == 422
