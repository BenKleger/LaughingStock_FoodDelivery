from pydantic import BaseModel
from typing import List

class OrderCost(BaseModel):
    order_cost: List[float]

class OrderCostCreate(BaseModel):
    user_order_id: str
    tip: float