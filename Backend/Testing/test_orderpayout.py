from fastapi.testclient import TestClient
from Backend.main import app
from Backend.FastAPI_DB.services.orders_service import calculate_delivery_payout, get_order_by_order_id

"""
tests for proper calulation of delivery payout based on order information."""
def test_calculate_delivery_payout():
    calc = calculate_delivery_payout(get_order_by_order_id("1d8e87M"))#used first order in order database
    expected = 5.0 + (0.59*2.17) #human calculation of payout 
    assert calc == expected

"""
tests for improper calulation of delivery payout based on order information."""
def test_calculate_delivery_payoutFalse():
    calc = calculate_delivery_payout(get_order_by_order_id("1d8e87M"))
    expected = 5.0 + (0.59*0)
    assert calc != expected

"""
tests that payout endpoint works
""""""
def test_payout_endpoint():
    client = TestClient(app)
    response = client.get("/orders/1d8e87M/payout") #used same order as above
    assert response.status_code == 200
"""""
