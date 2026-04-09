from fastapi import APIRouter
from FastAPI_DB.schemas.review import Review, ReviewCreate
from FastAPI_DB.services.reviews_service import createReview, removeReview, getReviewsByRestaurantId

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/create", status_code=201)
def createReview_endpoint(payload: ReviewCreate):
    return createReview(payload)

@router.delete("/delete/{review_id}", status_code=200)
def removeReview_endpoint(review_id: str):
    return removeReview(review_id)

@router.get("/restaurant/{restaurant_id}")
def getReviewsByRestaurantId_endpoint(restaurant_id: int):
    return getReviewsByRestaurantId(restaurant_id)