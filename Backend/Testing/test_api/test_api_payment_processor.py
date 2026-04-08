from fastapi.testclient import TestClient
from Backend.main import app
from FastAPI_DB.services.users_service import get_user_by_id
from FastAPI_DB.services.orders_service import change_order_status

test_client = TestClient(app)

def test_api_paymentProcessor_payment_method_valid():
    """
    Tests the verification of a valid payment method.
    """    
    response = test_client.post("/payment/validate", json={
        "customer_id": "",
        "order_id": "",
        "billing_address": "123 test st",
        "payment_number": "4111111111111111",
        "payment_pin": "888",
        "payment_method": "CREDIT",
        "card_holder_name": "Daniel",
        "postal_code": "A1A 1A1",
        "email": "daniel@test.com",
        "email_password": "123456789"
    })
    assert response.status_code == 200
    
def test_api_paymentProcessor_payment_method_invalid_credit():
    """
    Tests the verification of an invalid payment method. Everything except the payment method is blank.
    """    
    response = test_client.post("/payment/validate", json={
        "customer_id": "",
        "order_id": "",
        "billing_address": "",
        "payment_number": "",
        "payment_pin": "",
        "payment_method": "CREDIT",
        "card_holder_name": "",
        "postal_code": "",
        "email": "",
        "email_password": ""
    })
    assert response.status_code == 400
    assert response.json()["detail"] == ["CARD NUMBER LENGTH IS INCORRECT!","INVALID PIN!",
        "INVALID CARDHOLDER NAME!","INVALID POSTAL CODE!","ADDRESS TOO SHORT!"]
    
def test_api_paymentProcessor_payment_method_invalid_applepay():
    """
    Tests the verification of an invalid payment method. Everything except the payment method is blank.
    """    
    response = test_client.post("/payment/validate", json={
        "customer_id": "",
        "order_id": "",
        "billing_address": "",
        "payment_number": "",
        "payment_pin": "",
        "payment_method": "APPLEPAY",
        "card_holder_name": "",
        "postal_code": "",
        "email": "",
        "email_password": ""
    })
    assert response.status_code == 400
    assert response.json()["detail"] == ["INVALID EMAIL DOMAIN!","EMAIL PASSWORD TOO SHORT!"]

def test_api_paymentProcessor_process_order_valid():
    """
    Tries to process a valid order.
    """    
    change_order_status("f4d84dC", "being_created") #reset status
    response = test_client.post("/payment/process", json={
        "customer_id": "1fb6ba46-4857-46d4-9ea9-45f12c21623a",
        "order_id": "f4d84dC",
        "billing_address": "123 test st",
        "payment_number": "4111111111111111",
        "payment_pin": "888",
        "payment_method": "CREDIT",
        "card_holder_name": "Daniel",
        "postal_code": "A1A 1A1",
        "email": "daniel@test.com",
        "email_password": "123456789"
    })
    assert response.status_code == 200
    
def test_api_paymentProcessor_process_order_invalid_customer():
    """
    Tries to process an invalid order. The customer ID is wrong.
    """    
    response = test_client.post("/payment/process", json={
        "customer_id": "bad-id",
        "order_id": "f4d84dC",
        "billing_address": "123 test st",
        "payment_number": "4111111111111111",
        "payment_pin": "888",
        "payment_method": "CREDIT",
        "card_holder_name": "Daniel",
        "postal_code": "A1A 1A1",
        "email": "daniel@test.com",
        "email_password": "123456789"
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "User 'bad-id' not found"

def test_api_paymentProcessor_process_order_invalid_order1():
    """
    Tries to process an invalid order. The order ID does not exist.
    """    
    response = test_client.post("/payment/process", json={
        "customer_id": "1fb6ba46-4857-46d4-9ea9-45f12c21623a",
        "order_id": "bad-id",
        "billing_address": "123 test st",
        "payment_number": "4111111111111111",
        "payment_pin": "888",
        "payment_method": "CREDIT",
        "card_holder_name": "Daniel",
        "postal_code": "A1A 1A1",
        "email": "daniel@test.com",
        "email_password": "123456789"
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Order 'bad-id' not found"
    
def test_api_paymentProcessor_process_order_invalid_order2():
    """
    Tries to process an invalid order. The order ID exists but does not belong to the user.
    """    
    response = test_client.post("/payment/process", json={
        "customer_id": "1fb6ba46-4857-46d4-9ea9-45f12c21623a",
        "order_id": "5a6006W",
        "billing_address": "123 test st",
        "payment_number": "4111111111111111",
        "payment_pin": "888",
        "payment_method": "CREDIT",
        "card_holder_name": "Daniel",
        "postal_code": "A1A 1A1",
        "email": "daniel@test.com",
        "email_password": "123456789"
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "USER DOES NOT HAVE THIS ORDER!"