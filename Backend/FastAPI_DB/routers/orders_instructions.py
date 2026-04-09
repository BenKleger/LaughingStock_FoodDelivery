from fastapi import APIRouter
from FastAPI_DB.schemas.order_instructions import OrderInstructions
from FastAPI_DB.services.orders_service_instructions import get_order_delivery_instructions,get_order_cooking_instructions
from FastAPI_DB.services.orders_service_instructions import set_order_delivery_instructions,set_order_cooking_instructions

router = APIRouter(prefix="/instructions", tags=["instructions"])

@router.get("/delivery/{order_id}", response_model=OrderInstructions)
def get_delivery_instructions(order_id: str):
    id, inst = get_order_delivery_instructions(order_id)
    return OrderInstructions(order_id=id, instructions=inst)

@router.get("/cooking/{order_id}", response_model=OrderInstructions)
def get_cooking_instructions(order_id: str):
    id, inst = get_order_cooking_instructions(order_id)
    return OrderInstructions(order_id=id, instructions=inst)

@router.post("/delivery", response_model=OrderInstructions)
def post_delivery_instructions(payload: OrderInstructions):
    id, inst = set_order_delivery_instructions(payload.order_id, payload.instructions)
    return OrderInstructions(order_id=id, instructions=inst)

@router.post("/cooking", response_model=OrderInstructions)
def post_cooking_instructions(payload: OrderInstructions):
    id, inst = set_order_cooking_instructions(payload.order_id, payload.instructions)
    return OrderInstructions(order_id=id, instructions=inst)
