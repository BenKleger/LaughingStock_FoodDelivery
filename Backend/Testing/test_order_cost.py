from ..FastAPI_DB.services.orders_service import get_order_by_order_id
from ..FastAPI_DB.services.items_service import get_item_by_item_ID

from ..User.user_utils import get_order_cost

def test_order_cost():
    """Tests order cost calculations"""
    user_order = "fac5b0A"

    user_tip = 2.0
    
    item_price = get_item_by_item_ID(get_order_by_order_id(user_order).item_ids[0]).price

    func_cost, distance = get_order_cost(user_order, user_tip)
    real_cost = item_price + item_price*0.13 + user_tip + (7 if distance*0.7 < 7 else 2 + distance*0.7)

    assert func_cost == round(real_cost, 2)