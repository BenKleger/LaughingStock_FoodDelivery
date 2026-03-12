from typing import List, Dict, Any
from fastapi import HTTPException
from ..schemas.menu import Menu, MenuCreate
from ..repositories.order_repo import load_all, save_all


def list_menus() -> List[Menu]:
    return [Menu(**it) for it in load_all()]

def create_menus(payload: MenuCreate) -> Menu:
    """
    Creates a new menu saves it to database.

    Parameters:
        payload (MenuCreate): Object containing menu data.

    Returns:
        Menu: The created Menu object (already added to the database).

    Description:
        This function loads existing menus from repository,
        creates new menu and appends it to the list,
        and save the updated list back to the repo.
    """

    menus = load_all()
    new_menu = Menu(menu_id=payload.menu_id.strip(), 
                     menus=payload.menus)
    
    menus.append(new_menu.dict())
    save_all(menus)
    return new_menu

def get_menu_by_menu_ID(user_menu_ID: str) -> Menu:
    """
    Gets menu from database using its ID.

    Parameters:
        user_menu_ID (str): menu id provided by user.

    Returns:
        Menu: Matching the provided ID.

    Raises:
        HTTPException: If no menu with the given ID exists in database.

    Description:
        The function searches through all stored menus and returns
        the menu whose menu_id matches the provided value.
    """

    menus = load_all()
    for it in menus:
        if it.get("menu_id") == user_menu_ID:
            return Menu(**it)
    raise HTTPException(status_code=404, detail=f"Menu '{user_menu_ID}' not found")