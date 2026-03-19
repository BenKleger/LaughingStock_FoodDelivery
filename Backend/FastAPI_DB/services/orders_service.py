from typing import List
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
                        weather_condition=payload.weather_condition.strip(), item_ids=payload.item_ids, order_status=payload.order_status)
   
    orders.append(new_order.model_dump())
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
        HTTPException 404: If no order with the given user_order_id exists in database.

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
                                    item_ids = [str(row[1]) + "-" + row[2]],
                                    order_status="delivered")

            orders.append(new_order.model_dump())
    save_all(orders)

    return True


def add_order_item(user_order_id: str, new_item_id: str):
    """
    Adds an item to an order.

    Parameters:
        user_order_id (str): order id provided by user.
        new_item_id (str): id of the item to add to the order.

    Returns:
        o (Order): The updated order item.

    Raises:
        HTTPException status 404: If no order with user_order_id exists in orders.json,
            or if no item with new_item_id exists in items.json (by items_service).
        HTTPException status 400: If the order is not in "being_created" status.
    
    Description:
        This function adds the given item_id to the given order item_ids. If no item is given it will do nothing.
    """

    orders = load_all()

    order_dict = None
    for order in orders:
        if order.get("order_id") == user_order_id:
            order_dict = order
            break
    
    if order_dict is None:
        raise HTTPException(status_code=404, detail=f"Order '{user_order_id}' not found")
    
    o = Order(**order_dict)
    
    if o.order_status != "being_created":
        raise HTTPException(status_code=400, detail=f"Order '{user_order_id}' cannot be changed because it is not in 'being_created' status")
               
    # May return HTTPException 404 if item is not found in the items.json file.           
    item_to_add = get_item_by_item_ID(new_item_id)
    
    o.item_ids.append(new_item_id)
    o.order_value += item_to_add.price
    
    # Update the dict in the list
    order_dict['item_ids'] = o.item_ids
    order_dict['order_value'] = o.order_value
    
    save_all(orders)

    return o




def delete_order_item(user_order_id: str, item_id_to_remove: str):
    """
    Removes an item from an order.

    Parameters:
        user_order_id (str): order id provided by user.
        item_id_to_remove (str): id of the item to remove.
       
    Returns:
        o (Order): Updated order after item removal.
    
    Raises:
        HTTPException status 404: If no order with user_order_id exists in orders.json, or
            if no item with item_id_to_remove exists in specified orders.json.
        HTTPException status 400: If the order is not in "being_created" status.

    Description:
        This function removes the given item from the given order.
    """
    orders = load_all()
    
    order_dict = None
    for order in orders:
        if order.get("order_id") == user_order_id:
            order_dict = order
            break
    
    if order_dict is None:
        raise HTTPException(status_code=404, detail=f"Order '{user_order_id}' not found")
    
    o = Order(**order_dict)
    
    if o.order_status != "being_created":
        raise HTTPException(status_code=400, detail=f"Item '{item_id_to_remove}' from order '{user_order_id}' cannot be deleted because it is not in 'being_created' status")
    
    if item_id_to_remove not in o.item_ids:
        raise HTTPException(status_code=404, detail=f"Item '{item_id_to_remove}' not found in order '{user_order_id}'")
    
    
    o.item_ids.remove(item_id_to_remove)
    
    # Update the dict in the list
    order_dict['item_ids'] = o.item_ids
    
    save_all(orders)
    
    return o


def delete_order(user_order_id: str):
    """
    Deletes the specified order from the database.

    Parameters:
        user_order_id (str): order id provided by user.
    
    Returns:
        bool: True if successful, False if no order with the given ID exists.

    Raises:
        HTTPException status 404: If no order with user_order_id exists in orders.json.
        HTTPException status 400: If the order is not in "being_created" status.
    
    Description:
        Deletes the specified order from the data/orders.json file
    """

    orders = load_all()
    for order in orders:
        if order.get("order_id") == user_order_id:
            if order.get("order_status") != "being_created":
                raise HTTPException(status_code=400, detail=f"Order '{user_order_id}' cannot be deleted because it is not in 'being_created' status")
            orders.remove(order)
            save_all(orders)
            return True
    
    raise HTTPException(status_code=404, detail=f"Order '{user_order_id}' not found")

def change_order_status(user_order_id: str, new_status: str):
    """
    Changes the status of an order.

    Parameters:
        user_order_id (str): order id provided by user.
        new_status (str): the status the order should be updated to

    Returns:
        o (Order): The updated order item.

    Raises:
        HTTPException status 404: If no order with user_order_id exists in orders.json,
            or if no item with new_item_id exists in items.json (by items_service).
        HTTPException status 400: If the order is not in "being_created", 
        "paid", "sent", or "accepted" status. Basically everything but "delivered".
    
    Description:
        This function modifies the order status of a given order. If no item is given it will do nothing.
    """

    orders = load_all()

    order_dict = None
    for order in orders:
        if order.get("order_id") == user_order_id:
            order_dict = order
            break
    
    if order_dict is None:
        raise HTTPException(status_code=404, detail=f"Order '{user_order_id}' not found")
    
    o = Order(**order_dict)
    
    if o.order_status == "delivered":
        raise HTTPException(status_code=400, detail=f"Order '{user_order_id}' cannot be changed because it was already delivered")
    
    if new_status in ["being_created", "paid", "sent", "accepted"]:
        o.order_status = new_status
    else: 
        raise HTTPException(status_code=400, detail=f"Status '{new_status}' is not a valid status.")
    
    # Update the dict in the list
    order_dict['order_status'] = o.order_status
    
    save_all(orders)

    return o