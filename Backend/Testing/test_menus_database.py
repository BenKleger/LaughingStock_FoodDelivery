from ..FastAPI_DB.services.menus_service import list_menus, reset_menus_DB
from ..FastAPI_DB.schemas.menu import Menu

def test_database_content():
    """Tests database fetch"""
    menus_database = list_menus()

    assert len(menus_database) > 0
    assert isinstance(menus_database[0], Menu)

def test_database_creation():
    reset_menus_DB()

    menus_database = list_menus()

    assert len(menus_database) == 100