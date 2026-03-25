from fastapi import HTTPException
import pytest

from Backend.FastAPI_DB.schemas.item import Item, ItemCreate
from Backend.FastAPI_DB.services.items_service import create_items
from Backend.FastAPI_DB.schemas.order import Order, OrderCreate
from Backend.FastAPI_DB.services.orders_service import create_orders, add_order_item, delete_order_item, delete_order, get_order_by_order_id, change_order_status
    
order: Order = None

def test_create_order_and_add_and_delete_order_item():
    """
    Tests create_orders function, adding multiple items with the add_order_item function,
    deleting an item with the delete_order_item function and finally deleting the order.

    All are in same function as it is easiest to test on a single order, not requring multiple
    order creations.
    """
    
    orderCreate = OrderCreate(order_id = "test_order",
                          restaurant_id = 101,
                          food_item = "Test Food",
                          order_time = "now",
                          delivery_time = "later",
                          delivery_distance = 5.5,
                          order_value = 10.12,
                          delivery_method = "bike",
                          traffic_condition = "light",
                          weather_condition = "sunny",
                          item_ids = [],
                          order_status = "being_created")
    
    order = create_orders(orderCreate)


    itemCreate = ItemCreate(item_id="101-Test Item", restaurant_id = 101, name="Test Item", price=9.99, tags=["tasty","yummy"])
    
    item = create_items(itemCreate)

    order = add_order_item(order.order_id, item.item_id)
    order = add_order_item(order.order_id, "21-Pasta")

    print(order.item_ids)
    o = get_order_by_order_id(order.order_id)
    print(o.item_ids)
    assert len(order.item_ids) == 2
    assert order.item_ids[0] == item.item_id

    order = delete_order_item(order.order_id, "101-Test Item")
    
    assert len(order.item_ids) == 1

    #testing order status change
    order = change_order_status(order.order_id, "paid")
    o = get_order_by_order_id(order.order_id)
    print("change 1:" + o.order_status)
    assert o.order_status == "paid"
    #test invalid status change
    with pytest.raises(HTTPException) as exception:
        order = change_order_status(order.order_id, "KILL")
        assert exception.value.detail == "Status KILL is not a valid status." 
    #change status back to being_created so it can be deleted
    order = change_order_status(order.order_id, "being_created")
    o = get_order_by_order_id(order.order_id)
    print("change 2:" + o.order_status)
    assert o.order_status == "being_created"
    
    deleted = delete_order(order.order_id)
    
    assert deleted == True

def test_delete_order_item_completed_order():
    """
    Tests delete_order_item function, to ensure that an item cannot 
    be deleted from an order that is not in "being_created" status.
    """
    with pytest.raises(HTTPException):    
        assert delete_order_item("1d8e87M", "16-Taccos")

