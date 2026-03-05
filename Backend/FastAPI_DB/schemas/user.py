from pydantic import BaseModel
from typing import List

class User(BaseModel):
    id: str
    username: str
    password: str
    # type:

class UserCreate(BaseModel):
    username: str
    password: str
    # type:

class UserUpdate(BaseModel):
    id: str
    username: str
    password: str
    # type: