from pydantic import BaseModel

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

class OrderCreate(BaseModel):
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