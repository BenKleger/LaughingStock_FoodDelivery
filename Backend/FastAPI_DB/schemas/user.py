from pydantic import BaseModel
from typing import List

class User(BaseModel):
    id: str
    username: str
    password: str
    type: int # 0 for customer, 1 for restaurant, 2 for delivery

class UserCreate(BaseModel):
    username: str
    password: str
    type: int 

class UserUpdate(BaseModel):
    id: str
    username: str
    password: str
    type: int 