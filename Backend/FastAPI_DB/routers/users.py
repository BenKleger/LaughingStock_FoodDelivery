from typing import List

from fastapi import APIRouter, HTTPException
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
    get_total_driver_tips,
    get_total_customer_tips
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

@router.get("/{username}/total_tips")
def get_total_tips(username: str):
    user = get_user_by_username(username)
    if user.type == 1:  # Customer
        return {"total_tips_given": get_total_customer_tips(username)}
    elif user.type == 2:  # Driver
        return {"total_tips_received": get_total_driver_tips(username)}
    else:
        raise HTTPException(status_code=400, detail="Invalid user type")
