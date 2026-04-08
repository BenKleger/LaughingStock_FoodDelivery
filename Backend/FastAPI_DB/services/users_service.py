import uuid
from typing import List
from fastapi import HTTPException
from ..schemas.order import Order, OrderCreate
from ..schemas.user import Customer, Driver, User, UserCreate, Manager
from ..repositories.user_repo import load_all, save_all
from ..services.orders_service import list_orders, change_order_status, get_order_by_order_id, create_orders


def list_users() -> List[User]:
    users =[]
    for it in load_all():
        if it.get("type") == 1: #checks the type field for each user and returns proper class
            users.append(Customer(**it))
        elif it.get("type") == 2:
            users.append(Driver(**it))
        elif it.get("type") == 3:
            users.append(Manager(**it))
    return users

"""Returns created user with a unique id, its type determines which subclass it is + its attributes. The user is then added to the database."""
def create_users(payload: UserCreate) -> User:
    users = load_all()
    new_id = str(uuid.uuid4())
    if any(it.get("id") == new_id for it in users):  # extremely unlikely, but consistent check
        raise HTTPException(status_code=409, detail="ID collision; retry.")
    
    if payload.type ==1:
        new_user = Customer(id=new_id, username=payload.username.strip(), password=payload.password.strip(), type=payload.type, ordersList=[])
    elif payload.type == 2:
        new_user = Driver(id=new_id, username=payload.username.strip(), password=payload.password.strip(), type=payload.type, ordersTaken=[])
    elif payload.type == 3:
        new_user = Manager(id=new_id, username=payload.username.strip(), password=payload.password.strip(), type=payload.type, restaurantId=0)
    else:
        raise HTTPException(status_code=400, detail="Invalid user type, must be 1, 2, or 3.")

    users.append(new_user.model_dump())
    save_all(users)
    return new_user

"""Searches through database for user with matching username and returns it. Exception if none found"""
def get_user_by_username(user_username: str) -> User:
    items = load_all()
    for it in items:
        if it.get("username") == user_username:
            if it.get("type") == 1: #this logic just returns the correct subclass based on type
                return Customer(**it)
            elif it.get("type") == 2:
                return Driver(**it)
            elif it.get("type") == 3:
                return Manager(**it)
          #  return User(**it)
    raise HTTPException(status_code=404, detail=f"User '{user_username}' not found")

def get_user_by_id(user_id: str) -> User:
    items = load_all()
    for it in items:
        if it.get("id") == user_id:
            if it.get("type") == 1:
                return Customer(**it)
            elif it.get("type") == 2:
                return Driver(**it)
            elif it.get("type") == 3:
                return Manager(**it)
    raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")


def save_user(user: User) -> User:
    users = load_all()
    for idx, it in enumerate(users):
        if it.get("id") == user.id:
            users[idx] = user.model_dump()
            save_all(users)
            return user
    raise HTTPException(status_code=404, detail=f"User '{user.id}' not found")


def get_driver_available_orders(user_username: str) -> List[Order]:
    driver = get_user_by_username(user_username)
    if not isinstance(driver, Driver):
        raise HTTPException(status_code=400, detail=f"User '{user_username}' is not a driver")

    return [order for order in list_orders() if order.order_status == "paid"]


def get_driver_accepted_orders(user_username: str) -> List[Order]:
    driver = get_user_by_username(user_username)
    if not isinstance(driver, Driver):
        raise HTTPException(status_code=400, detail=f"User '{user_username}' is not a driver")

    accepted_orders: List[Order] = []
    for order_id in driver.ordersTaken:
        accepted_orders.append(get_order_by_order_id(order_id))
    return accepted_orders


def accept_order_for_driver(user_username: str, order_id: str) -> Order:
    driver = get_user_by_username(user_username)
    if not isinstance(driver, Driver):
        raise HTTPException(status_code=400, detail=f"User '{user_username}' is not a driver")

    order = get_order_by_order_id(order_id)
    if order.order_status != "paid":
        raise HTTPException(status_code=400, detail="Only orders in paid status can be accepted.")

    order = change_order_status(order_id, "accepted")
    if order_id not in driver.ordersTaken:
        driver.ordersTaken.append(order_id)
        save_user(driver)

    return order


def get_customer_orders(username: str) -> List[Order]:
    """Get all orders for a customer"""
    user = get_user_by_username(username)
    if user.type != 1:
        raise HTTPException(status_code=400, detail=f"User '{username}' is not a customer")

    customer = Customer(**user.model_dump())
    orders = []
    for order_id in customer.ordersList:
        try:
            order = get_order_by_order_id(order_id)
            orders.append(order)
        except:
            pass  # Skip orders that don't exist
    return orders


def create_order_for_customer(username: str, order_data: dict) -> Order:
    """Create a new order for a customer"""
    user = get_user_by_username(username)
    if user.type != 1:
        raise HTTPException(status_code=400, detail=f"User '{username}' is not a customer")

    # Create the order
    order_create = OrderCreate(**order_data)
    order = create_orders(order_create)

    # Add order to customer's order list
    customer = Customer(**user.model_dump())
    if order.order_id not in customer.ordersList:
        customer.ordersList.append(order.order_id)
        save_user(customer)

    return order