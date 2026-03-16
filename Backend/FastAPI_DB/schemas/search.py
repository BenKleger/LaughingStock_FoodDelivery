from pydantic import BaseModel
from typing import List

class Search(BaseModel):
    search_results: List[List[str]]  # pages of lists of item id's matching search query,  search_results[0]
                                    # is the first page of search results, displaying first 10 items

class SearchCreate(BaseModel):
    query: str  # search query string, e.g. "pizza", "sushi", "burger"
    filter: str # price_high_to_low, price_low_to_high

