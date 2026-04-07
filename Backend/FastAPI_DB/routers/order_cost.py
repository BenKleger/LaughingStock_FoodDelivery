from fastapi import APIRouter
from FastAPI_DB.schemas.order_cost import OrderCost
from FastAPI_DB.services.order_cost_service import get_order_cost

router = APIRouter(prefix="/order_cost", tags=["order_cost"])

@router.get("/{user_order_id}/{tip}", response_model=OrderCost)
def get_cost(user_order_id: str, tip: float):
    cost, distance = get_order_cost(user_order_id, tip)
    return OrderCost(order_cost=[cost, distance])