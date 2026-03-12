import uuid, time
from typing import List, Dict, Any
from fastapi import HTTPException

from ..schemas.item import Item, ItemCreate
from ..repositories.item_repo import load_all as items_load, save_all as items_save

from ..schemas.order import Order
from ..repositories.order_repo import load_all as orders_load


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
    items_save([])

    new_id = str(uuid.uuid4())

    if any(it.get("item_id") == new_id for it in items):  # extremely unlikely, but consistent check
        raise HTTPException(status_code=409, detail="ID collision; retry.")
    
    new_item = Item(item_id=new_id.strip(), 
                    restaurant_id=payload.restaurant_id,
                    name=payload.name.strip(), 
                    tags=payload.tags, 
                    price=payload.price)
    
    items.append(new_item.dict())
    items_save(items)
    return new_item

    # users = load_all()
    # new_id = str(uuid.uuid4())
    # if any(it.get("id") == new_id for it in users):  # extremely unlikely, but consistent check
    #     raise HTTPException(status_code=409, detail="ID collision; retry.")
    # new_user = User(id=new_id, username=payload.username.strip(), password=payload.password.strip())
    # users.append(new_user.dict())
    # save_all(users)
    # return new_user

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
        items_save([])

        unique_items = []
        orders_from_db = orders_load()

        for order in orders_from_db:
            restaurant_id = order["restaurant_id"]
            item_name = order["food_item"]
            item_price = order["order_value"]

            key = (restaurant_id, item_name)

            if key not in unique_items:
                unique_items.append(key)

                create_items(ItemCreate(item_id="-1",
                                restaurant_id=restaurant_id,
                                name=item_name,
                                tags=[],
                                price=item_price))
                
        return True
    except:
        return False

    # with open("FastAPI_DB/data/food_delivery.csv", newline="") as f:
    #     reader = csv.reader(f)

    #     next(reader)

    #     for row in reader:
    #         new_order = ItemCreate(order_id=row[0], 
    #                                 restaurant_id=int(row[1]), 
    #                                 food_item=row[2], 
    #                                 order_time=row[3], 
    #                                 delivery_time=row[4], 
    #                                 delivery_distance=float(row[5]), 
    #                                 order_value=float(row[6]), 
    #                                 delivery_method=row[7], 
    #                                 traffic_condition=row[8], 
    #                                 weather_condition=row[9])
    #         orders.append(new_order.dict())
    # save_all(orders)

    # return True