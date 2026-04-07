from pydantic import BaseModel
from typing import List

class restaurantAssign(BaseModel):
    restaurant_id: int

class restaurantCreate(BaseModel):
    restaurant_id: int

class menuItemAdd(BaseModel):
    name: str
    price: float