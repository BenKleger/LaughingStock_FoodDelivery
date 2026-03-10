from typing import List, Dict, Any
from fastapi import HTTPException
from FastAPI_DB.schemas.order import Order, OrderCreate
from FastAPI_DB.repositories.order_repo import load_all, save_all
import csv


def list_orders() -> List[Order]:
    return [Order(**it) for it in load_all()]

def create_orders(payload: OrderCreate) -> Order:
    orders = load_all()
    new_order = Order(order_id=payload.order_id.strip(), restaurant_id=payload.restaurant_id, food_item=payload.food_item.strip(),
                        order_time=payload.order_time.strip(), delivery_time=payload.delivery_time.strip(), delivery_distance=payload.delivery_distance,
                        order_value=payload.order_value, delivery_method=payload.delivery_method.strip(), traffic_condition=payload.traffic_condition.strip(),
                        weather_condition=payload.weather_condition.strip())
    orders.append(new_order.dict())
    save_all(orders)
    return new_order

def get_order_by_order_id(user_order_id: str) -> Order:
    items = load_all()
    for it in items:
        if it.get("order_id") == user_order_id:
            return Order(**it)
    raise HTTPException(status_code=404, detail=f"Order '{user_order_id}' not found")

def reset_order_DB():
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