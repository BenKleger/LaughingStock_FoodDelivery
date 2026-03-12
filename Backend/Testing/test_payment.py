from Backend.PaymentSystem import paymentProcessor
from Backend.PaymentSystem import paymentService
from Backend.FastAPI_DB.services import users_service
from Backend.Order import order
from Backend.Restaurant import item
from decimal import Decimal

newUser = users_service.UserCreate(username="testUser", password="testPW")
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

def test_create_paymentService():
    """Tests creation of a basic, default payment service"""
    newOrder = order.order(item0) #item0 has all default values (0 or empty)
    newService = paymentService.paymentService(newOrder, newUser)
    assert newService.orderID == ""
    assert newService.paymentBase == 0
    assert newService.commission == 0
    assert str(newService.taxRate) == "0.12"

def test_paymentService_total():
    """tests function of payment service"""
    newOrder = order.order(item1)
    newService = paymentService.paymentService(newOrder, newUser)
    # print(newService.calcTotal())
    assert newService.calcTotal() == Decimal(str(round(14.99 + 14.99*0.05 + 14.99*0.12, 4)))
