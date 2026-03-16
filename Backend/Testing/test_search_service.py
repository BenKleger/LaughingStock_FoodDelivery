from fastapi import HTTPException
import pytest

from ..FastAPI_DB.schemas.search import Search, SearchCreate
from ..FastAPI_DB.services.search_service import create_search
    
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
    print(created_search.search_results)
    assert len(created_search.search_results[0]) == 10