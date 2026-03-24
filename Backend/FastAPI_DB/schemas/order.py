from pydantic import BaseModel
from typing import List

class Order(BaseModel):
    order_id: str
    restaurant_id: int
    food_item: str
    order_time: str
    delivery_time: str
    delivery_distance: float
    order_value: float
    delivery_method: str
    traffic_condition: str
    weather_condition: str
    item_ids: List[str]
    order_status: str # "being_created", "paid", "sent", "accepted", "delivered"

class OrderCreate(BaseModel):
    restaurant_id: int
    food_item: str
    order_time: str
    delivery_time: str
    delivery_distance: float
    order_value: float
    delivery_method: str
    traffic_condition: str
    weather_condition: str
    item_ids: List[str]
    order_status: str # "being_created", "paid", "sent", "accepted", "delivered"
