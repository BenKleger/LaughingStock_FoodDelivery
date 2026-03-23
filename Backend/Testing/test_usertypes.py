from fastapi.testclient import TestClient
from Backend.main import app


testClient = TestClient(app)

"""Tests user creation of each type by posting a User class object to the /users endpoint.
checks username, type, and unique attributes of each class
HTTP 201 means that the new User was created properly"""

def test_customer_creation():
    response = testClient.post(
        "/users", json={"username": "test_customer", "password": "test_password", "type" : 1}
    )
    assert response.status_code == 201
    data = response.json()
    assert data ["username"] == "test_customer"
    assert data ["type"] == 1
    assert "ordersList" in data

def test_Driver_creation():
    response = testClient.post(
        "/users", json={"username": "test_driver", "password": "test_password", "type" : 2}
    )
    assert response.status_code == 201
    data = response.json()
    assert data ["username"] == "test_driver"
    assert data ["type"] == 2
    assert "ordersTaken" in data

def test_Manager_creation():
    response = testClient.post(
        "/users", json={"username": "test_manager", "password": "test_password", "type" : 3}
    )
    assert response.status_code == 201
    data = response.json()
    assert data ["username"] == "test_manager"
    assert data ["type"] == 3
    assert "restaurantId" in data