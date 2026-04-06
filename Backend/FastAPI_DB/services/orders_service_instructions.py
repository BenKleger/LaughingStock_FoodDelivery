from FastAPI_DB.services.orders_service import get_order_by_order_id
from User.user_utils import alter_order_json
from fastapi import HTTPException

def set_order_delivery_instructions(order_id: str, instructions: str):
    order = get_order_by_order_id(order_id)
    order.delivery_instructions = instructions
    alter_order_json(order)
    return order.order_id, order.delivery_instructions

def set_order_cooking_instructions(order_id: str, instructions: str):
    order = get_order_by_order_id(order_id)
    order.cooking_instructions = instructions
    alter_order_json(order)
    return order.order_id, order.cooking_instructions
    
def get_order_delivery_instructions(order_id: str):
    order = get_order_by_order_id(order_id)
    if(order.delivery_instructions.strip()):
        return order.order_id, order.delivery_instructions
    else:
        raise HTTPException(status_code=404, detail="This order has no delivery instructions.")

def get_order_cooking_instructions(order_id: str):
    order = get_order_by_order_id(order_id)
    if(order.cooking_instructions.strip()):
        return order.order_id, order.cooking_instructions
    else:
        raise HTTPException(status_code=404, detail="This order has no cooking instructions.")
 

    