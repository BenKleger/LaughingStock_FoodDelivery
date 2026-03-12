from fastapi import APIRouter, status
from typing import List
from FastAPI_DB.schemas.order import Order, OrderCreate
from FastAPI_DB.services.orders_service import list_orders, create_orders, get_order_by_order_id

router = APIRouter(prefix="/orders", tags=["order"])

@router.get("", response_model=List[Order])
def get_orders():
    return list_orders()

@router.post("", response_model=Order, status_code=201)
def post_item(payload: OrderCreate):
    return create_orders(payload)

@router.get("/{order}", response_model=Order)
def get_user(order_id: str):
    return get_order_by_order_id(order_id)