import uuid
from typing import List
from fastapi import HTTPException
from FastAPI_DB.schemas.user import Customer, Driver, User, UserCreate, Manager
from FastAPI_DB.repositories.user_repo import load_all, save_all


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