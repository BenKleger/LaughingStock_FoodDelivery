from fastapi import APIRouter, status
from typing import List
from FastAPI_DB.schemas.user import User, UserCreate
from FastAPI_DB.services.users_service import list_users, create_user, get_user_by_username

router = APIRouter(prefix="/users", tags=["user"])

@router.get("", response_model=List[User])
def get_users():
    return list_users()

#simple post the payload (is the body of the request)
@router.post("", response_model=User, status_code=201)
def post_item(payload: UserCreate):
    return create_user(payload)


from FastAPI_DB.services.users_service import list_items, create_user

@router.get("/{username}", response_model=User)
def get_user(user_username: str):
    return get_user_by_username(user_username)
