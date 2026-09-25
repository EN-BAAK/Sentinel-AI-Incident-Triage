from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_create_incident() -> None:
    response = client.post(
        "/incidents",
        json={
            "title": "Orders API latency",
            "description": "API latency has been increasing for several hours.",
            "service": "orders-api",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["summary"] == (
        "API latency has been increasing for several hours."
    )
    assert body["evidence"] == []
    assert body["hypotheses"] == []
    assert body["recommended_steps"] == []
    assert body["confidence"] == 0.0

def test_create_incident_rejects_invalid_input() -> None:
    response = client.post(
        "/incidents",
        json={
            "title": "x",
            "description": "short",
            "service": "",
        },
    )

    assert response.status_code == 422