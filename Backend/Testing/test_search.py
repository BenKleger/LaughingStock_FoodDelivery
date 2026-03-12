from Backend.SearchService import search

def test_create_searchService():
    """Tests creation of a basic, default search service"""
    newSearch = search.searchService()
    assert newSearch.priceRange["upperBound"] == 1000