from fastapi import APIRouter
from FastAPI_DB.schemas.search import Search, SearchCreate
from FastAPI_DB.services.search_service import create_search
router = APIRouter(prefix="/search", tags=["search"])

@router.post("", 
             response_model=Search, 
             summary = "Search items",
             description="""
            Parameters: 
                A search query and filter ('price_low_to_high' or 'price_high_to_low'), 
            Returns: 
                A paginated search response.
            Description:
                Allows user to enter a string describing one of the following:
                A restaurant, the name of an item, a specific item ID
            """
)

def post_item(payload: SearchCreate):
    return create_search(payload)
