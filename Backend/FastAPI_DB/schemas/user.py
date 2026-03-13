from pydantic import BaseModel


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