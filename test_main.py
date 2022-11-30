from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_create_user():
    response = client.get("/healthz")
    assert response.status_code == 200


