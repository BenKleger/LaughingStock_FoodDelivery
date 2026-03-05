from Backend.Restaurant.item import itemClass
from Backend.Order.order import orderClass

def test_payment_total():
    item1 = itemClass(10)
    item2 = itemClass(20)
    order = orderClass([item1, item2])
    total = order.get_total
    assert total == 30