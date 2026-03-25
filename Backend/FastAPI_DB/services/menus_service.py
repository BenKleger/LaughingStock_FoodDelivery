from typing import List
from fastapi import HTTPException

from FastAPI_DB.schemas.menu import Menu, MenuCreate
from FastAPI_DB.repositories.menu_repo import load_all as menus_load, save_all as menus_save

from FastAPI_DB.repositories.item_repo import load_all as items_load


def list_menus() -> List[Menu]:
    return [Menu(**it) for it in menus_load()]

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

    menus = menus_load()
    new_menu = Menu(menu_id=payload.menu_id, 
                     items=payload.items)
    
    menus.append(new_menu.model_dump())
    menus_save(menus)
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

    menus = menus_load()
    for it in menus:
        if it.get("menu_id") == int(user_menu_ID):
            return Menu(**it)
    raise HTTPException(status_code=404, detail=f"Menu '{user_menu_ID}' not found")

def reset_menus_DB():
    """
    Resets the item database using data from the orders.json file.

    Returns:
        bool: True if successful.

    Description:
        This function clears the current item database and repopulates it
        using the records from the orders.json dataset.
    """
    try:
        menus_save([])

        items_from_db = items_load()
        items_by_restaurant = {}

        for item in items_from_db:
            restaurant_id = item["restaurant_id"]

            if restaurant_id not in items_by_restaurant:
                items_by_restaurant[restaurant_id] = []

            items_by_restaurant[restaurant_id].append(item)

        for restaurant_id in items_by_restaurant:
            create_menus(MenuCreate(menu_id=restaurant_id, 
                                    items=items_by_restaurant[restaurant_id]))

        return True
    except:
        print("Menus reset failed...")
        return False