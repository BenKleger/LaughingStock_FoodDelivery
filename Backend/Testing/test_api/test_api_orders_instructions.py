from fastapi.testclient import TestClient
from Backend.main import app
from FastAPI_DB.services.users_service import get_user_by_id
from FastAPI_DB.services.orders_service import change_order_status

test_client = TestClient(app)

def test_api_delivery_instructions_post_valid():
    """
    Tries to post a valid request
    """
    response = test_client.post("/instructions/delivery", json={
        "order_id": "135630M",
        "instructions": "Leave in mailbox" 
    })
    assert response.status_code == 200
    assert response.json()["order_id"] == "135630M"
    assert response.json()["instructions"] == "Leave in mailbox"
    
def test_api_delivery_instructions_post_invalid():
    """
    Tries to post an invalid request
    """
    response = test_client.post("/instructions/delivery", json={
        "order_id": "bad-id",
        "instructions": "Leave in mailbox" 
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Order 'bad-id' not found"

def test_api_delivery_instructions_get_invalid():
    """
    Tries to post an invalid request
    """
    response = test_client.get("/instructions/delivery/bad-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Order 'bad-id' not found"

def test_api_delivery_instructions_get_valid():
    """
    Tries to post a valid request
    """    
    response = test_client.get("/instructions/delivery/135630M")
    assert response.status_code == 200
    assert response.json()["order_id"] == "135630M"
    assert response.json()["instructions"] == "Leave in mailbox"