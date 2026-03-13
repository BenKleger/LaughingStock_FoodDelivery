from Backend.FastAPI_DB.services.orders_service import list_orders, reset_order_DB
from Backend.FastAPI_DB.schemas.order import Order


def test_database_creation():
    reset_order_DB()

    orders_database = list_orders()

    assert len(orders_database) == 10000
    assert isinstance(orders_database[0], Order)

def test_database_content():
    """Tests database fetch"""
    menus_database = list_orders()

    assert len(menus_database) > 0
    assert isinstance(menus_database[0], Order)

#def test_database_content():
#    """Tests database fetch"""
#    order_database = list_orders()
#
 #   assert len(order_database) > 0
#    assert isinstance(order_database[0], Order)