from fastapi import APIRouter, HTTPException
from typing import List
from FastAPI_DB.routers import menus
from FastAPI_DB.schemas import menu
from FastAPI_DB.schemas.manager_funcs import restaurantAssign, restaurantCreate, menuItemAdd
from User.manager_branch import get_ownedRestuarants, get_unownedRestuarants, view_menu, add_menu_item
from FastAPI_DB.services.users_service import get_user_by_username
from FastAPI_DB.repositories.user_repo import load_all as load_users, save_all as save_users
from FastAPI_DB.repositories.menu_repo import load_all as load_menu, save_all as save_menus
from FastAPI_DB.repositories.item_repo import load_all as load_items, save_all as save_items
from FastAPI_DB.schemas.item import ItemCreate
from FastAPI_DB.services.items_service import create_items
from FastAPI_DB.services.menus_service import get_menu_by_menu_ID


#TODO: currently a username has to be specified instead of system knowing which manager is logged in
#      depending on how login is implemented this will need to be changed.
#      maybe refactor code if time...

"""
Endpoints for all manager functionalilites including:
- viewing availible restaurant ids
- selecting a restaurant to manage
- creating a new restaurant to manage
- viewing menu for their restaurant
- adding items to their restaurant's menu
- removing items from their restaurant's menu

The logic for each of these endpoints is the same as the functions in manager_branch.py
but re written to work with FastAPI
"""

router = APIRouter(prefix="/managers", tags=["manager"])

@router.get("/restuarants/available")
def get_available_restaurants():
    return get_unownedRestuarants()

@router.post("/{username}/restuarants/assign")
def assign_restaurant(username: str, payload: restaurantAssign):
    manager = manager_check(username)
    if payload.restaurant_id not in get_unownedRestuarants():
        raise HTTPException(status_code=400, detail="restaurant is not available to manage")
    save_restaurant_id(username, payload.restaurant_id)
    return {"message": "restaurant " + str(payload.restaurant_id) + " assigned to manager with username " + username}

@router.post("/restuarants/create")
def create_restaurant(username: str, payload: restaurantAssign):
    manager = manager_check(username)
    taken = get_ownedRestuarants() + get_unownedRestuarants()
    if not(101 <= payload.restaurant_id <= 999) or payload.restaurant_id in taken:
        raise HTTPException(status_code=400, detail="restaurant id " + str(payload.restaurant_id) + " is invalid or already taken")
    save_restaurant_id(username, payload.restaurant_id)
    return {"message": "restuarant "  + str(payload.restaurant_id) + " created and assigned to manager with username " + username}

@router.get("/{username}/menu")
def get_menu(username: str):
    manager = manager_check(username)
    if not(manager.restaurantId):
        raise HTTPException(status_code=400, detail= "manager does not have a restaurant")
    try:
        menu = get_menu_by_menu_ID(str(manager.restaurantId))
    except HTTPException:
        raise HTTPException(status_code=404, detail="menu not found for restaurant " + str(manager.restaurantId))
    return menu.items

@router.post("/{username}/menu/add")
def add_menu_item(username: str, payload: menuItemAdd):
    manager = manager_check(username)
    if not(manager.restaurantId):
        raise HTTPException(status_code=400, detail= "manager does not have a restaurant")
    if not(payload.name.isalpha() or (5 <= len(payload.name) <=20)):
        raise HTTPException(status_code=400, detail="item name must be 5-20 character and only have letters")
    if payload.price <=0:
        raise HTTPException(status_code=400, detail=("price must be valid"))
    
    item_id = str(manager.restaurantId) + "-" + payload.name
    new_item = ItemCreate(item_id=item_id, restaurant_id=manager.restaurantId, name=payload.name, tags=[], price=payload.price)
    create_items(new_item)       
        
    menus = load_menu()

    menu_exists = any(menu["menu_id"] == manager.restaurantId for menu in menus) #checks if a menu for manager alr exists
    if not menu_exists:
        new_menu = {"menu_id": manager.restaurant_Id, "items": [new_item.model_dump()]}
        menus.append(new_menu)
    else:
        for menu in menus:
            if menu["menu_id"] == manager.restaurantId:
                menu["items"].append(new_item.model_dump()) #note to self:model dump converts the model to dict
                break

    save_menus(menus)
    return {"message": "item " + payload.name + " added to menu for restaurant " + str(manager.restaurantId)}


@router.delete("/{username}/menu/remove/{item_id}")
def remove_menu_item(username: str, item_id: str):
    manager = manager_check(username)
    if not(manager.restaurantId):
        raise HTTPException(status_code=400, detail= "manager does not have a restaurant")
    menu = get_menu_by_menu_ID(str(manager.restaurantId))
    if len(menu.items) == 0:
        raise HTTPException(status_code=400, detail="menu is empty")
    match = False
    for item in menu.items:
        if item.item_id == item_id:
            match = True
            break
    if match:
        menus = load_menu()
        for menu in menus:
            if menu["menu_id"] == manager.restaurantId:
                menu["items"] = [item for item in menu["items"] if item["item_id"] != item_id]
                break
        save_menus(menus)
        items = load_items()
        items = [item for item in items if item["item_id"] != item_id] 
        save_items(items)
        return {"message": "item " + item_id + " removed from menu for restaurant " + str(manager.restaurantId)}
    raise HTTPException(status_code=400, detail="item not found in menu")


"""
Helper functions for manager functions

manager_check:
    checks if user is type 3
    returns error if not otherwise returns user obj

save_restaurant_id:
    saves id to a given username in users.json
"""
def manager_check(username: str):
    user = get_user_by_username(username)
    if user.type !=3:
        raise HTTPException(status_code=403, detail="user is not a manager")
    return user

def save_restaurant_id(username: str, restaurant_id: int):
    users = load_users()
    for u in users:
        if u.get("username") == username:
            u["restaurantId"] = restaurant_id
            break
    save_users(users)