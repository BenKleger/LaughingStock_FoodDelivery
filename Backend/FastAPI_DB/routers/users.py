from typing import List

from fastapi import APIRouter
from FastAPI_DB.schemas.order import Order, OrderCreate
from FastAPI_DB.schemas.user import UserCreate, Customer, Driver, Manager
from FastAPI_DB.services.users_service import (
    list_users,
    create_users,
    get_user_by_username,
    get_driver_available_orders,
    get_driver_accepted_orders,
    accept_order_for_driver,
    get_customer_orders,
    create_order_for_customer,
)

router = APIRouter(prefix="/users", tags=["user"])

@router.get("")
def get_users():
    return list_users()

#simple post the payload (is the body of the request)
@router.post("",response_model= Customer | Driver | Manager,status_code=201)
def post_item(payload: UserCreate):
    return create_users(payload)

@router.get("/{username}/available_orders", response_model=List[Order])
def get_driver_available_orders_endpoint(username: str):
    return get_driver_available_orders(username)


@router.get("/{username}/accepted_orders", response_model=List[Order])
def get_driver_accepted_orders_endpoint(username: str):
    return get_driver_accepted_orders(username)


@router.post("/{username}/accept/{order_id}", response_model=Order)
def accept_order_for_driver_endpoint(username: str, order_id: str):
    return accept_order_for_driver(username, order_id)


@router.get("/{username}")
def get_user(username: str):
    return get_user_by_username(username)


@router.get("/{username}/orders", response_model=List[Order])
def get_customer_orders_endpoint(username: str):
    return get_customer_orders(username)

@router.post("/{username}/orders", response_model=Order, status_code=201)
def create_order_for_customer_endpoint(username: str, payload: OrderCreate):
    return create_order_for_customer(username, payload.model_dump())
