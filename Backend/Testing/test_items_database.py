from Backend.FastAPI_DB.services.items_service import list_items, reset_items_DB
from Backend.FastAPI_DB.schemas.item import Item


def test_item_database_creation():
    """
    Tests item database creation and population with initial data.
    
    Will alter items.json
    """
    reset_items_DB()

    order_database = list_items()

    assert len(order_database) == 2083
    assert isinstance(order_database[0], Item)

def test_item_database_content():
    """
    Tests item database content retrieval.
    """
    order_database = list_items()

    assert len(order_database) > 0
    assert isinstance(order_database[0], Item)
