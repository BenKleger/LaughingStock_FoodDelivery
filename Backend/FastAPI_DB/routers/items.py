from fastapi import APIRouter, status
from typing import List
from FastAPI_DB.schemas.order import Item, ItemCreate
from FastAPI_DB.services.items_service import list_items, create_items, get_item_by_item_id

router = APIRouter(prefix="/items", tags=["item"])

@router.get("", response_model=List[Item])
def get_items():
    return list_items()

@router.post("", response_model=Item, status_code=201)
def post_item(payload: ItemCreate):
    return create_items(payload)

@router.get("/{item}", response_model=Item)
def get_item(item_id: str):
    return get_item_by_item_id(item_id)