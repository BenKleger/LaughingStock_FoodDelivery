from Backend.Restaurant.item import item
from Backend.Order.order import order
    
myOrder: order
item1: item = item(10)

def test_create_order():
    """Tests creation of an order"""
    myOrder = order(item1)
    assert myOrder.order_size == 1
    assert len(myOrder.order_list) == 1
    assert isinstance(myOrder, order)

def test_payment_total():
    """Tests payment total of an order with one item"""
    myOrder = order(item1)
    total = myOrder.get_total()
    assert item1.itemPrice == 10
    assert myOrder.order_size == 1
    assert total == 10

def test_add_item():
    """Tests adding an item to the list"""
    item2 = item(20)
    myOrder = order(item1)
    myOrder.add_item(item2)
    assert len(myOrder.order_list) == 2
    assert myOrder.order_size == 2

def test_payment_total2():
    item2 = item(20)
    myOrder = order(item1)
    myOrder.add_item(item2)
    total = myOrder.get_total()
    assert total == 30

def test_remove_item_with_index():
    item2 = item(20)
    myOrder = order(item1)
    myOrder.remove_item(0)    
    assert myOrder.order_size == 0


def test_remove_item_with_item():
    item2 = item(20)
    myOrder = order(item1)
    myOrder.add_item(item2)
    myOrder.remove_item(1)
    myOrder.remove_item(item1)
    assert myOrder.order_size == 0

def test_directory():
    print(test_directory)
    assert True