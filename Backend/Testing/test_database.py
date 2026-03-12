from ..FastAPI_DB.services.orders_service import list_orders
from ..FastAPI_DB.schemas.order import Order

def test_database_content():
    """Tests database fetch"""
    order_database = list_orders()

    assert len(order_database) > 0
    assert isinstance(order_database[0], Order)