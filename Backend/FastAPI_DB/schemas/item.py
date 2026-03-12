from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    item_id: str
    name: str
    tags: List[str]
    price: float

class ItemCreate(BaseModel):
    item_id: str
    name: str
    tags: List[str]
    price: float