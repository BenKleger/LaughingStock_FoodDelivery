from fastapi import APIRouter
from FastAPI_DB.schemas.search import Search, SearchCreate
from FastAPI_DB.services.search_service import create_search
##TODO!!
router = APIRouter(prefix="/search", tags=["search"])

@router.post("", response_model=Search, status_code=201)
def post_item(payload: SearchCreate):
    return create_search(payload)

@router.get("/{search}", response_model=SearchCreate)
def get_search(search: str):
    return (search)