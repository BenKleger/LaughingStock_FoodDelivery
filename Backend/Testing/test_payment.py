from Backend.PaymentSystem import paymentProcessor
from Backend.PaymentSystem import paymentService
from Backend.FastAPI_DB.services import users_service
from Backend.Order import order
from Backend.Restaurant import item
from decimal import Decimal

newUser = users_service.UserCreate(username="testUser", password="testPW", type=1) #type 1 is customer
newUser = users_service.create_users(newUser)
item0 = item.item()
item1 = item.item(price=14.99, ID="001", name="Fried watermelon")
item2 = item.item(price=5.99, ID="002", name="Raw watermelon")

def test_create_paymentProcessor():
    """Tests creation of a basic, default payment processor"""
    myProcessor = paymentProcessor.paymentProcessor(newUser)
    assert myProcessor.userID == newUser.id
    # assert myProcessor.userAddress == customer.userAddress
    # rest of the vars are trivial

def test_paymentProcessor_verification():
    """Tests processor verification
    the credit card number is a valid mastercard test number"""
    myProcessor = paymentProcessor.paymentProcessor(newUser, "CREDIT", "5555500830030331",
        "001", "John Smith", "A1A 1A1", "John@google.com", "emailPW")
    assert myProcessor.validatePaymentMethod() is True

def test_paymentProcessor_verification_luhn():
    """Tests the luhn algo. Only difference is the 1st digit."""
    myProcessor = paymentProcessor.paymentProcessor(newUser, "CREDIT", "1555500830030331",
        "001", "John Smith", "A1A 1A1", "John@google.com", "emailPW")
    assert myProcessor.validatePaymentMethod() is False

def test_create_paymentService():
    """Tests creation of a basic, default payment service"""
    newOrder = order.order(item0) #item0 has all default values (0 or empty)
    newService = paymentService.paymentService(newOrder, newUser)
    assert newService.orderID == ""
    assert newService.paymentBase == 0
    assert newService.commission == 0
    assert str(newService.taxRate) == "0.12"

def test_paymentService_total():
    """Tests function of payment service"""
    newOrder = order.order(item1)
    newOrder.add_item(item2)
    newService = paymentService.paymentService(newOrder, newUser)
    subtotal = item1.itemPrice + item2.itemPrice
    assert newService.calcTotal() == Decimal(str(round(subtotal + subtotal*0.05 + subtotal*0.12, 4)))
