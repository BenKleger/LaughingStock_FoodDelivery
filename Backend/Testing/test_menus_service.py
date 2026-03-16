from ..FastAPI_DB.services.menus_service import get_menu_by_menu_ID

def test_menu_by_menu_ID():
    menu = get_menu_by_menu_ID("100")
    assert menu is not None