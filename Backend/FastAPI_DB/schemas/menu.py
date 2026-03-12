from pydantic import BaseModel
from typing import List
from .item import Item

class Menu(BaseModel):
    menu_id: int
    items: List[Item]

class MenuCreate(BaseModel):
    menu_id: int
    items: List[Item]