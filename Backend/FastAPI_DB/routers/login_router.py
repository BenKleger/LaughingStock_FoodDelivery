from fastapi import APIRouter, HTTPException
from FastAPI_DB.schemas.user import UserLogin
from FastAPI_DB.repositories.user_repo import load_all, save_all

router = APIRouter(prefix="/login", tags=["login"])

@router.post("/")
def login(user_login: UserLogin):
    users = load_all()
    for user in users:
        if user.get("username") == user_login.username and user.get("password") == user_login.password:
            return user
    raise HTTPException(status_code=401, detail="Invalid username or password")
