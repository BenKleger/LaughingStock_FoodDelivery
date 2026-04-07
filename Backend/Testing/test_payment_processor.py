from FastAPI_DB.services import users_service
from fastapi import HTTPException
import pytest

from FastAPI_DB.schemas.order import OrderCreate
from FastAPI_DB.services.orders_service import create_orders
from FastAPI_DB.services.payment_processor_service import process_payment
from FastAPI_DB.schemas.payment_processor import PaymentProcessorCreate

newUser = users_service.UserCreate(username="testUser", password="testPW", type=1)
newUser = users_service.create_users(newUser)
newOrder = OrderCreate(order_id = "test_order_payment", restaurant_id=16, food_item="Taccos",
                       order_time="",delivery_time="",delivery_distance=1,order_value=1,
                       delivery_method="",traffic_condition="",weather_condition="",
                       item_ids=[],order_status="being_created")

def test_create_paymentProcessor():
    """
    Tests creation of a basic, default payment processor.
    """
    myOrder = create_orders(newOrder)
    myProcessor = PaymentProcessorCreate(customer_id = newUser.id, order_id = myOrder.order_id)
    assert myProcessor.customer_id == newUser.id
# test_create_paymentProcessor()

"""commented until order API is finalized"""
# def test_paymentProcessor_verification():
#     """
#     Tests processor verification. Everything is valid.
#     The credit card number is an actual mastercard test number.
#     """
#     myOrder = create_orders(newOrder)
#     myProcessor = PaymentProcessorCreate(customer_id=newUser.id, order_id=myOrder.order_id, payment_method="CREDIT", 
#                     payment_number="5555500830030331", payment_pin="001",
#                     card_holder_name="John Smith", postal_code="A1A 1A1", billing_address="123 TEST ST")
#     assert process_payment(myProcessor) is True
# test_paymentProcessor_verification()

def test_paymentProcessor_verification_luhn():
    """Tests the luhn algo. Only difference is the 1st digit."""
    myOrder = create_orders(newOrder)
    myProcessor = PaymentProcessorCreate(customer_id=newUser.id, order_id=myOrder.order_id, payment_method="CREDIT", 
                    payment_number="1555500830030331", payment_pin="001",
                    card_holder_name="John Smith", postal_code="A1A 1A1", billing_address="123 TEST ST")
    with pytest.raises(HTTPException) as exception:
        process_payment(myProcessor)
    assert exception.value.status_code == 400
    assert "INVALID CARD NUMBER! DID YOU MAKE A MISTAKE?" in exception.value.detail[0]
    assert len(exception.value.detail) == 1
# test_paymentProcessor_verification_luhn()

def test_paymentProcessor_verification_very_wrong():
    """Tests a very invalid payment method. Paymenr number, pin, postal code, and address 
    are all invalid."""
    myOrder = create_orders(newOrder)
    myProcessor = PaymentProcessorCreate(customer_id=newUser.id, order_id=myOrder.order_id, payment_method="CREDIT", 
                    payment_number="12345", payment_pin="Le0",
                    card_holder_name="John Smith", postal_code="1A1 A1A", billing_address="No Number St")
    with pytest.raises(HTTPException) as exception:
        process_payment(myProcessor)
    assert exception.value.status_code == 400
    assert "CARD NUMBER LENGTH IS INCORRECT!" in exception.value.detail[0]
    assert 'INVALID CARD NUMBER! DID YOU MAKE A MISTAKE?' in exception.value.detail[1]
    assert "INVALID PIN!" in exception.value.detail[2]
    assert "INVALID POSTAL CODE!" in exception.value.detail[3]
    assert "MISSING HOUSE NUMBER!" in exception.value.detail[4]
# test_paymentProcessor_verification_very_wrong()

def test_paymentProcessor_verification_wrong_method():
    """Tests the special case where the payment method is invalid. This skips other checks."""
    myOrder = create_orders(newOrder)
    myProcessor = PaymentProcessorCreate(customer_id=newUser.id, order_id=myOrder.order_id, payment_method="KILL", 
                    payment_number="5555500830030331", payment_pin="001",
                    card_holder_name="John Smith", postal_code="A1A 1A1", billing_address="123 TEST ST")
    with pytest.raises(HTTPException) as exception:
        process_payment(myProcessor)
    assert exception.value.status_code == 400
    assert "INVALID PAYMENT METHOD!" in exception.value.detail[0]
    assert len(exception.value.detail) == 1
# test_paymentProcessor_verification_wrong_method()

"""commented until order API is finalized"""
# def test_paymentProcessor_verification_apple_pay():
#     """
#     Tests processor verification with applepay as the method. Everything is valid.
#     The credit card number is an actual mastercard test number.
#     """
#     myOrder = create_orders(newOrder)
#     myProcessor = PaymentProcessorCreate(customer_id=newUser.id, order_id=myOrder.order_id, payment_method="APPLEPAY",
#                                          email="John@google.com", email_password="emailPW")
#     assert process_payment(myProcessor) is True
# test_paymentProcessor_verification_apple_pay()

def test_paymentProcessor_verification_apple_pay_wrong():
    """Tests the luhn algo. Only difference is the 1st digit."""
    myOrder = create_orders(newOrder)
    myProcessor = PaymentProcessorCreate(customer_id=newUser.id, order_id=myOrder.order_id, payment_method="APPLEPAY",
                                         email="John@.com", email_password="1")
    with pytest.raises(HTTPException) as exception:
        process_payment(myProcessor)
    assert exception.value.status_code == 400
    assert "INVALID EMAIL FORMAT!" in exception.value.detail[0]
    assert "EMAIL PASSWORD TOO SHORT!" in exception.value.detail[1]
    assert len(exception.value.detail) == 2
# test_paymentProcessor_verification_apple_pay_wrong()