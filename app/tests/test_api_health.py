from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_api_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.text == "F5-UP"
