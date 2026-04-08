from fastapi import APIRouter
from typing import List
from FastAPI_DB.schemas.order import Order, OrderCreate
from FastAPI_DB.services.orders_service import (
    list_orders,
    create_orders,
    get_order_by_order_id,
    change_order_status,
    add_order_item,
    delete_order_item,
    delete_order
)

router = APIRouter(prefix="/orders", tags=["order"])

@router.get("", response_model=List[Order])
def get_orders():
    return list_orders()

@router.post("", response_model=Order, status_code=201)
def post_item(payload: OrderCreate):
    return create_orders(payload)

@router.get("/{order_id}", response_model=Order)
def get_item(order_id: str):
    return get_order_by_order_id(order_id)

@router.put("/{order_id}/status")
def update_order_status(order_id: str, status: str):
    return change_order_status(order_id, status)

@router.post("/{order_id}/items/{item_id}")
def add_item_to_order(order_id: str, item_id: str):
    return add_order_item(order_id, item_id)

@router.delete("/{order_id}/items/{item_id}")
def remove_item_from_order(order_id: str, item_id: str):
    return delete_order_item(order_id, item_id)

@router.delete("/{order_id}")
def delete_order_endpoint(order_id: str):
    return delete_order(order_id)