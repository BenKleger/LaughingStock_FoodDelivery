import uuid
from typing import List, Dict, Any
from fastapi import HTTPException
from FastAPI_DB.schemas.user import User, UserCreate
from FastAPI_DB.repositories.user_repo import load_all, save_all


def list_users() -> List[User]:
    return [User(**it) for it in load_all()]

def create_users(payload: UserCreate) -> User:
    users = load_all()
    new_id = str(uuid.uuid4())
    if any(it.get("id") == new_id for it in users):  # extremely unlikely, but consistent check
        raise HTTPException(status_code=409, detail="ID collision; retry.")
    new_user = User(id=new_id, username=payload.username.strip(), password=payload.password.strip())
    users.append(new_user.dict())
    save_all(users)
    return new_user

def get_user_by_username(user_username: str) -> User:
    items = load_all()
    for it in items:
        if it.get("username") == user_username:
            return User(**it)
    raise HTTPException(status_code=404, detail=f"User '{user_username}' not found")

def get_user_by_id(user_id: str) -> User:
    items = load_all()
    for it in items:
        if it.get("id") == user_id:
            return User(**it)
    raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")