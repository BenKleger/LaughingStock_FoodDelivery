from ..FastAPI_DB.services.orders_service import get_order_by_order_id
from ..User.user_utils import get_order_cost

def test_order_cost():
    """Tests order cost calculations"""
    user_order = "1d8e87M"

    user_discount = 0.2
    user_tip = 2.0

    assert get_order_cost(user_order, user_tip, user_discount) == 40.59