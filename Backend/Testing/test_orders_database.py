from Backend.FastAPI_DB.services.orders_service import list_orders, reset_order_DB
from Backend.FastAPI_DB.schemas.order import Order


def test_order_database_content():
    """
    Tests orders database content retrieval.
    """
    orders_database = list_orders()

    assert len(orders_database) > 0
    assert isinstance(orders_database[0], Order)
