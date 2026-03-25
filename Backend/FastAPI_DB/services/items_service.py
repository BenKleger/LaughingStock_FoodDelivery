from typing import List
from fastapi import HTTPException

from FastAPI_DB.schemas.item import Item, ItemCreate
from FastAPI_DB.repositories.item_repo import load_all as items_load, save_all as items_save

from FastAPI_DB.repositories.order_repo import load_all as orders_load


def list_items() -> List[Item]:
    return [Item(**it) for it in items_load()]

def create_items(payload: ItemCreate) -> Item:
    """
    Creates a new item and saves it to database.

    Parameters:
        payload (ItemCreate): Object containing order data.

    Returns:
        Item: The created Item object (already added to the database).

    Description:
        This function loads existing items from repository,
        creates new item and appends it to the list,
        and save the updated list back to the repo.
    """

    items = items_load()

    new_item = Item(item_id=payload.item_id.strip(), 
                    restaurant_id=payload.restaurant_id,
                    name=payload.name.strip(), 
                    tags=payload.tags, 
                    price=payload.price)
    
    items.append(new_item.model_dump())
    items_save(items)
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

    items = items_load()
    for it in items:
        if it.get("item_id") == user_item_ID:
            return Item(**it)
    raise HTTPException(status_code=404, detail=f"Item '{user_item_ID}' not found")

def reset_items_DB():
    """
    Resets the item database using data from the orders.json file.

    Returns:
        bool: True if successful.

    Description:
        This function clears the current item database and repopulates it
        using the records from the orders.json dataset.
    """
    try:
        orders_from_db = orders_load()

        unique_items = {}
        for order in orders_from_db:
            restaurant_id = order.get("restaurant_id")
            item_name = order.get("food_item")
            item_price = order.get("order_value")

            if restaurant_id is None or item_name is None or item_price is None:
                continue

            key = (restaurant_id, item_name)
            if key in unique_items:
                continue

            unique_items[key] = item_price

        items = []
        for (restaurant_id, item_name), item_price in unique_items.items():
            items.append({
                "item_id": f"{restaurant_id}-{item_name}",
                "restaurant_id": restaurant_id,
                "name": item_name,
                "tags": [],
                "price": item_price,
            })

        items_save(items)
        return True
    except:
        print("Items reset failed...")
        return False