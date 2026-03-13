from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    item_id: str
    restaurant_id: int
    name: str
    tags: List[str]
    price: float

class ItemCreate(BaseModel):
    item_id: str
    restaurant_id: int
    name: str
    tags: List[str]
    price: float