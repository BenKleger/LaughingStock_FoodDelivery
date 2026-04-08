from pydantic import BaseModel

class OrderInstructions(BaseModel):
    order_id: str
    instructions: str