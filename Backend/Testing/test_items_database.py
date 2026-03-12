from ..FastAPI_DB.services.items_service import list_items, reset_items_DB
from ..FastAPI_DB.schemas.item import Item

def test_database_content():
    """Tests database fetch"""
    order_database = list_items()

    assert len(order_database) > 0
    assert isinstance(order_database[0], Item)

def test_database_creation():
    reset_items_DB()

    order_database = list_items()

    assert len(order_database) == 2083
    assert isinstance(order_database[0], Item)

# python3 -m Backend.Testing.test_items_database