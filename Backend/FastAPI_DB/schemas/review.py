from pydantic import BaseModel
from typing import List

class Review(BaseModel):
    review_id: str  #[restaurantId + "-" + customerName]
    restaurant_id: int
    customer_name: str
    rating: float #1-5 point scale
    comment: str = "" #optional commment field

class ReviewCreate(BaseModel):
    restaurant_id: int
    customer_name: str
    rating: float
    comment: str = "" 
