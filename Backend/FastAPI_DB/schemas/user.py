from pydantic import BaseModel


class User(BaseModel):
    id: str
    username: str
    password: str
    type: int #(1)customer, (2)Driver, (3) Manager

class UserCreate(BaseModel):
    username: str
    password: str
    type: int 

class UserUpdate(BaseModel):
    id: str
    username: str
    password: str
    type: int 

"""
Subclasses and their attributes + defualt values:
"""

class Customer(User):
    ordersList: list[str] = [] 

class Driver(User):
    ordersTaken: list[str] = []

class Manager(User):
    restaurantId : int =0 #restaurant ids 1-100