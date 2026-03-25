from pydantic import BaseModel
from typing import List
from FastAPI_DB.schemas import user as userClass
from FastAPI_DB.schemas import order as orderClass

class PaymentProcessor(BaseModel):
    customer: userClass.User
    order: orderClass.Order
    billing_address: str
    payment_number: str
    payment_pin: str
    payment_method: str
    card_holder_name: str
    postal_code: str
    email: str
    email_password: str

class PaymentProcessorCreate(BaseModel):
    customer: userClass.User
    order: orderClass.Order
    billing_address: str = ""
    payment_number: str = ""
    payment_pin: str = ""
    payment_method: str = ""
    card_holder_name: str = ""
    postal_code: str = ""
    email: str = ""
    email_password: str = ""