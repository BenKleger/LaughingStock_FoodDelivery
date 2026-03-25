from Backend.FastAPI_DB.services.menus_service import get_menu_by_menu_ID

def test_menu_by_menu_ID():
    """
    Tests if getting menu by menu ID works
    """
    menu = get_menu_by_menu_ID(100)
    assert menu is not None
    assert menu.menu_id == 100
    assert len(menu.items) == 21