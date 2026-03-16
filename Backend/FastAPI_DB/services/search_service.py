from typing import List
from fastapi import HTTPException

from ..schemas.search import Search, SearchCreate
from .menus_service import get_menu_by_menu_ID
from .items_service import get_item_by_item_ID
from .orders_service import list_orders


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

        Finally it will check if the user is searching for 
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
                # TODO add searching the entire itemdb for any possible matches
                pass
            except:
                return Search(search_results=[])

def create_search_by_restaurant_ID(payload: SearchCreate, menu) -> Search:
    """
    Helper function to create_search, searches by restaurant ID.

    Parameters:
        payload (SearchCreate): Object containing search data.
    
    Returns:
        Search: The created Search object.

    Description:
        This function performs a search for the given query and filter.
        TODO
    """
    
def create_search_by_item_name(payload: SearchCreate) -> Search:
    """
    Creates a new search result.

    Parameters:
        payload (SearchCreate): Object containing search data.
    
    Returns:
        Search: The created Search object.

    Description:
        This function performs a search for the given query and filter.
        TODO
    """

def paginate_list(payload: SearchCreate, items: List[str]) -> List[List[str]]:
    """
    Helper function to sort and paginate search results.
    
    Paramters:
        payload (SearchCreate): used to obtain method of sorting items. 
        items (List[str]): List of items to be sorted into pages.
        
    Returns: 
        List[List[str]]: Paginated result sorted by filtering method.
        
    """

