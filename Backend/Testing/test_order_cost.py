from ..FastAPI_DB.services.orders_service import get_order_by_order_id
from ..FastAPI_DB.schemas.order import Order

from ..User.user_utils import get_order_cost

def test_database_content():
    """Tests order cost calculations"""
    user_discount = 0.2
    user_tip = 2
    user_order = get_order_by_order_id("1d8e87M")
    
    assert get_order_cost(user_order, user_tip, user_discount) == 40.59