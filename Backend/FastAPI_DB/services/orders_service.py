from typing import List, Dict, Any
from fastapi import HTTPException
from ..schemas.order import Order, OrderCreate
from ..repositories.order_repo import load_all, save_all
import csv


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
    new_order = Order(order_id=payload.order_id.strip(), restaurant_id=payload.restaurant_id, food_item=payload.food_item.strip(),
                        order_time=payload.order_time.strip(), delivery_time=payload.delivery_time.strip(), delivery_distance=payload.delivery_distance,
                        order_value=payload.order_value, delivery_method=payload.delivery_method.strip(), traffic_condition=payload.traffic_condition.strip(),
                        weather_condition=payload.weather_condition.strip())
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

    items = load_all()
    for it in items:
        if it.get("order_id") == user_order_id:
            return Order(**it)
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

    with open("FastAPI_DB/data/food_delivery.csv", newline="") as f:
        reader = csv.reader(f)

        next(reader)

        for row in reader:
            new_order = OrderCreate(order_id=row[0], 
                                    restaurant_id=int(row[1]), 
                                    food_item=row[2], 
                                    order_time=row[3], 
                                    delivery_time=row[4], 
                                    delivery_distance=float(row[5]), 
                                    order_value=float(row[6]), 
                                    delivery_method=row[7], 
                                    traffic_condition=row[8], 
                                    weather_condition=row[9])
            orders.append(new_order.dict())
    save_all(orders)

    return True

def calculate_delivery_payout(order: Order) -> float:
    """
    Calulates the payout for an order based on a flat rate and delivery distance. 
    Delivery distance is based off of Doordash Average PricePerKm of $0.59/Km"""

   # order = get_order_by_order_id(order.order_id)
    flate_rate = 5.0
    distance_rate = 0.59
    payout = flate_rate + (distance_rate * order.delivery_distance)
    return payout


