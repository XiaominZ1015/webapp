from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/v1/account", json={
      "first_name": "Tony",
      "last_name": "lu",
      "email": "tony@111.com",
      "password": "123"
    })
    assert response.status_code == 200


