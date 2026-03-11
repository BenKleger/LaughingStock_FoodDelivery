from fastapi.testclient import TestClient
from Backend.main import app 

client = TestClient(app)
def test_create_user():
    response = client.post("/users", json={"id" : "12345", "username": "testuser", "password": "testpass", "type": 1})
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["type"] == 1
    assert "id" in data #ensures id exists for user
