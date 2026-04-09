from operator import attrgetter
from typing import List
from fastapi import HTTPException

from FastAPI_DB.schemas.item import Item

from ..schemas.search import Search, SearchCreate
from .menus_service import get_menu_by_menu_ID
from .items_service import get_item_by_item_ID
from ..repositories.item_repo import load_all as items_load

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
        return create_search_by_restaurant_ID(payload)
        # Will generate HTTPException when no menu with given ID is found.
    except:
        try:
            item = get_item_by_item_ID(payload.query)
            return Search(search_results=paginate_list(payload, [item]))
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
    """
    menu = get_menu_by_menu_ID(int(payload.query.strip()))
    items = menu.items
    return Search(search_results=paginate_list(payload, items))
    
def create_search_by_item_name(payload: SearchCreate) -> Search:
    """
    Creates a new search result.

    Parameters:
        payload (SearchCreate): Object containing search data.
    
    Returns:
        Search: The created Search object.

    Description:
        This function performs a search for by item name through the item database.
        Works reguardless of capitalization or whitespace added.
    """
    
    all_items = items_load()
    items = []
    for item in all_items:
        if item.get("name").lower().strip() == payload.query.lower().strip():
            items.append(Item(**item))
    search_result=paginate_list(payload, items)
    search = Search(search_results=search_result)
    return search

def paginate_list(payload: SearchCreate, items: List[Item]) -> List[List[str]]:
    """
    Helper function to sort and paginate search results.
    
    Paramters:
        payload (SearchCreate): used to obtain method of sorting items. 
        items (List[Item]): List of items to be sorted into pages.
        
    Returns: 
        List[List[str]]: Paginated result sorted by filtering method,
        uses ITEMS_PER_PAGE to determine at most how many items to
        include on each page.
    """
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