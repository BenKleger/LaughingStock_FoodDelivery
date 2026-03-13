from typing import List, Dict, Any
from fastapi import HTTPException
from ..schemas.order import Order, OrderCreate
from ..repositories.order_repo import load_all, save_all
import csv
import uuid
from .items_service import get_item_by_item_ID
from ..schemas.item import Item as item 

def list_orders() -> List[Order]:
    return [Order(**it) for it in load_all()]

def create_orders(payload: OrderCreate) -> Order:
    """
    Creates a new order saves it to database.

    Parameters:
        payload (OrderCreate): Object containing order data.

    Returns:
        Order: The created Order object (already added to the database).

    Description:
        This function loads existing orders from repository,
        creates new order and appends it to the list,
        and save the updated list back to the repo.
    """
    orders = load_all()

    new_id = str(uuid.uuid4())
    if any(order.get("order_id") == new_id for order in orders):  # extremely unlikely, but consistent check
        raise HTTPException(status_code=409, detail="ID collision; retry.")
    
    new_order = Order(order_id=new_id, restaurant_id=payload.restaurant_id, food_item=payload.food_item.strip(),
                        order_time=payload.order_time.strip(), delivery_time=payload.delivery_time.strip(), delivery_distance=payload.delivery_distance,
                        order_value=payload.order_value, delivery_method=payload.delivery_method.strip(), traffic_condition=payload.traffic_condition.strip(),
                        weather_condition=payload.weather_condition.strip(), item_ids=payload.item_ids)
    for item in payload.items:
        add_order_item(new_order.order_id, item)

    orders.append(new_order.dict())
    save_all(orders)
    return new_order

def get_order_by_order_id(user_order_id: str) -> Order:
    """
    Gets order from database using its ID.

    Parameters:
        user_order_id (str): order id provided by user.

    Returns:
        Order: Matching the provided ID.

    Raises:
        HTTPException: If no order with the given ID exists in database.

    Description:
        The function searches through all stored orders and returns
        the order whose order_id matches the provided value.
    """

    orders = load_all()
    for order in orders:
        if order.get("order_id") == user_order_id:
            return Order(**order)
    raise HTTPException(status_code=404, detail=f"Order '{user_order_id}' not found")

def reset_order_DB():
    """
    Resets the order database using data from the CSV file.

    Returns:
        bool: True if successful.

    Description:
        This function clears the current order database and repopulates it
        using the records from the food_delivery.csv dataset.
    """

    orders = []

    with open("Backend/FastAPI_DB/data/food_delivery.csv", newline="") as f:
        reader = csv.reader(f)

        next(reader)
    
        for row in reader:
            new_order = Order(order_id=row[0], 
                                    restaurant_id=int(row[1]), 
                                    food_item = row[2],
                                    order_time=row[3], 
                                    delivery_time=row[4], 
                                    delivery_distance=float(row[5]), 
                                    order_value=float(row[6]), 
                                    delivery_method=row[7], 
                                    traffic_condition=row[8], 
                                    weather_condition=row[9],
                                    item_ids = [str(row[1]) + "-" + row[2]]) 
            orders.append(new_order.dict())
    save_all(orders)

    return True


def add_order_item(user_order_id: str, new_item: item = None):
    """
    Adds an item to an order.

    Parameters:
        user_order_id (str): order id provided by user.
        new_item (item): item provided by user to replace current item in order.

    Returns:
        bool: True if successful.

    Description:
        This function overwrites the item in a given order, if no item is specified it will empty the order.
    """
    if new_item == None:
        # new_item not specified, clear the item from the order.
        return _clear_order_item(user_order_id)
    
    # new_item specified
    orders = load_all()
    for order in orders:
        if order.get("order_id") == user_order_id:
            o = Order(**order)
            break
        o.food_item = new_item
    raise HTTPException(status_code=404, detail=f"Order '{user_order_id}' not found")
    

    return True




def delete_order_item(user_order_id: str, item_id_to_remove: str):
    """
    Removes an item from an order.

    Parameters:
        user_order_id (str): order id provided by user.
        item_id_to_remove (str): id of the item to remove.
       
    Returns:
        bool: True if successful.

    Description:
        This function clears the item in a given order.
    """
    orders = load_all()
    for order in orders:
        if order.get("order_id") == user_order_id:
            return Order(**order)
    raise HTTPException(status_code=404, detail=f"Order '{user_order_id}' not found")

def delete_order(user_order_id: str):
    """
    Deletes the specified order from the database.

    Parameters:
        user_order_id (str): order id provided by user.
    
    Returns:
        bool: True if successful

    Description:
        Deletes the specified order from the data/orders.json file
    """

    pass
    return True