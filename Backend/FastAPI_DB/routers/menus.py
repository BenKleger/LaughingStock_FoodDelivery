from fastapi import APIRouter, status
from typing import List
from FastAPI_DB.schemas.menu import Menu, MenuCreate
from FastAPI_DB.services.items_service import list_menus, create_menus, get_menu_by_menu_id

router = APIRouter(prefix="/menus", tags=["menu"])

@router.get("", response_model=List[Menu])
def get_items():
    return list_menus()

@router.post("", response_model=Menu, status_code=201)
def post_item(payload: MenuCreate):
    return create_menus(payload)

@router.get("/{menu}", response_model=Menu)
def get_item(menu_id: str):
    return get_menu_by_menu_id(menu_id)