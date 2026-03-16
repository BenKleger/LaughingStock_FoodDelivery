from operator import attrgetter
from typing import List
from fastapi import HTTPException

from ..schemas.search import Search, SearchCreate
from .menus_service import get_menu_by_menu_ID
from .items_service import get_item_by_item_ID
from .orders_service import list_orders

ITEMS_PER_PAGE = 10

def create_search(payload: SearchCreate) -> Search:
    """
    Creates a new search result.

    Parameters:
        payload (SearchCreate): Object containing search data.
    
    Returns:
        Search: The created Search object.

    Description:
        This function performs a search for the given query and filter.
        
        It first checks if the user is searching for a restaurant's id,
        and will return the entire menu for that restaurant if so.

        Next it checks if the user is searching for an item id, returning that
        one item if so.

        Finally it will check through the item database for any possible matches
        to the search query, and return those. If no matches are found, it will return an empty list.
    """
    try:
        return create_search_by_restaurant_ID(payload,get_menu_by_menu_ID(payload.query))
        # Will generate HTTPException when no menu with given ID is found.
    except HTTPException:
        try:
            item = get_item_by_item_ID(payload.query)
            return Search(search_results = [0][item.item_id])
            # Will generate HTTPException when no item with given ID is found.
        except HTTPException:
            try:
                return create_search_by_item_name(payload)
            except:
                return Search(search_results=[])

def create_search_by_restaurant_ID(payload: SearchCreate) -> Search:
    """
    Helper function to create_search, searches by restaurant ID.

    Parameters:
        payload (SearchCreate): Object containing search data.
    
    Returns:
        Search: The created Search object.

    Description:
        This function returns all items from the menu of a given restaurant.
        TODO
    """
    return []
    
def create_search_by_item_name(payload: SearchCreate) -> Search:
    """
    Creates a new search result.

    Parameters:
        payload (SearchCreate): Object containing search data.
    
    Returns:
        Search: The created Search object.

    Description:
        This function performs a search for by item name through the item database.
        TODO
    """

    return []

def paginate_list(payload: SearchCreate, items_ids: List[str]) -> List[List[str]]:
    """
    Helper function to sort and paginate search results.
    
    Paramters:
        payload (SearchCreate): used to obtain method of sorting items. 
        items (List[str]): List of items to be sorted into pages.
        
    Returns: 
        List[List[str]]: Paginated result sorted by filtering method,
        uses ITEMS_PER_PAGE to determine at most how many items to
        include on each page.
    """
    items = [get_item_by_item_ID(item_id) for item_id in items_ids]
    if payload.filter == "price_high_to_low":
        sorted_items = sorted(items, key=attrgetter("price"), reverse=True)
    elif payload.filter == "price_low_to_high":
        sorted_items = sorted(items, key=attrgetter("price"), reverse=False)
    else:
        sorted_items = items

    paginated_results: List[List[str]] = []
    for i in range(0, len(sorted_items), ITEMS_PER_PAGE):
        paginated_results.append([item.item_id for item in sorted_items[i:i+ITEMS_PER_PAGE]])
    
    return paginated_results

