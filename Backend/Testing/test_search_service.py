from fastapi import HTTPException
import pytest

from ..FastAPI_DB.schemas.search import Search, SearchCreate
from ..FastAPI_DB.services.search_service import create_search
from ..FastAPI_DB.services.items_service import get_item_by_item_ID
    
def test_search_service_by_item_id():
    """
    Tests the search service to ensure that it correctly
    returns the an item when searching by item ID.
    """

    search_query = "8-Pasta"
    created_search = create_search(SearchCreate(query=search_query, filter="price_low_to_high")) 
    assert len(created_search.search_results) == 1
    assert created_search.search_results[0][0] == search_query

def test_search_service_by_restaurant_id():
    """
    Tests the search service to ensure that it correctly
    returns all items from a given restaurant when searching
    by restaurant ID.
    """
    search_query = "100"
    created_search = create_search(SearchCreate(query=search_query, filter="price_low_to_high")) 
    assert len(created_search.search_results[0]) == 10
    item0 = get_item_by_item_ID(created_search.search_results[0][0])
    item1 = get_item_by_item_ID(created_search.search_results[0][1])
    assert item0.price <= item1.price

def test_search_by_high_to_low():
    """
    Tests the search service to ensure that it correctly
    returns all items from a given restaurant when searching
    by restaurant ID.
    """
    search_query = "100"
    created_search = create_search(SearchCreate(query=search_query, filter="price_high_to_low")) 
    item0 = get_item_by_item_ID(created_search.search_results[0][0])
    item1 = get_item_by_item_ID(created_search.search_results[0][1])
    assert item0.price >= item1.price



def test_search_service_by_item_name():
    """
    Tests searching for items by name, to ensure that the search service
    returns items matching the name searched for.
    """
    search_query = "Pasta"
    created_search = create_search(SearchCreate(query=search_query, filter="price_high_to_low")) 
    item0 = get_item_by_item_ID(created_search.search_results[0][0])
    item1 = get_item_by_item_ID(created_search.search_results[0][1])
    assert item0.price >= item1.price