from ..FastAPI_DB.services.menus_service import list_menus, reset_menus_DB
from ..FastAPI_DB.schemas.menu import Menu


def test_menu_database_creation():
    """
    Tests menu database creation and population with initial data.
    
    Will alter menus.json
    """
    reset_menus_DB()

    menus_database = list_menus()

    assert isinstance(menus_database[0], Menu)
    assert len(menus_database) == 100
    
def test_menu_database_content():
    """
    Tests menu database content retrieval.
    """
    menus_database = list_menus()

    assert len(menus_database) > 0