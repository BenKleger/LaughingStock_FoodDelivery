from pydantic import BaseModel
class PaymentProcessor(BaseModel):
    customer_id: str
    order_id: str
    billing_address: str
    payment_number: str
    payment_pin: str
    payment_method: str
    card_holder_name: str
    postal_code: str
    email: str
    email_password: str

class PaymentProcessorCreate(BaseModel):
    customer_id: str
    order_id: str
    billing_address: str = ""
    payment_number: str = ""
    payment_pin: str = ""
    payment_method: str = ""
    card_holder_name: str = ""
    postal_code: str = ""
    email: str = ""
    email_password: str = ""