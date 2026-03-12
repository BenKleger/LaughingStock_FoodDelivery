from typing import List, Dict, Any
from fastapi import HTTPException
from ..schemas.item import Item, ItemCreate
from ..repositories.order_repo import load_all, save_all


def list_items() -> List[Item]:
    return [Item(**it) for it in load_all()]

def create_items(payload: ItemCreate) -> Item:
    """
    Creates a new item saves it to database.

    Parameters:
        payload (ItemCreate): Object containing order data.

    Returns:
        Item: The created Item object (already added to the database).

    Description:
        This function loads existing items from repository,
        creates new item and appends it to the list,
        and save the updated list back to the repo.
    """

    items = load_all()
    new_item = Item(item_id=payload.itemID.strip(), 
                     name=payload.name, 
                     tags=payload.tags, 
                     price=payload.price)
    
    items.append(new_item.dict())
    save_all(items)
    return new_item

def get_item_by_item_ID(user_item_ID: str) -> Item:
    """
    Gets item from database using its ID.

    Parameters:
        user_item_ID (str): item id provided by user.

    Returns:
        Item: Matching the provided ID.

    Raises:
        HTTPException: If no order with the given ID exists in database.

    Description:
        The function searches through all stored items and returns
        the item whose item_id matches the provided value.
    """

    items = load_all()
    for it in items:
        if it.get("item_id") == user_item_ID:
            return Item(**it)
    raise HTTPException(status_code=404, detail=f"Item '{user_item_ID}' not found")