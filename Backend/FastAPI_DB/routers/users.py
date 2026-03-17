from fastapi import APIRouter, status
from typing import List
from Backend.FastAPI_DB.schemas.user import User, UserCreate, Customer, Driver, Manager
from Backend.FastAPI_DB.services.users_service import list_users, create_users, get_user_by_username

router = APIRouter(prefix="/users", tags=["user"])

@router.get("")
def get_users():
    return list_users()

#simple post the payload (is the body of the request)
@router.post("",response_model= Customer | Driver | Manager,status_code=201)
def post_item(payload: UserCreate):
    return create_users(payload)

@router.get("/{username}")
def get_user(user_username: str):
    return get_user_by_username(user_username)
