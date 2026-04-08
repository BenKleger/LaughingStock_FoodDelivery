from FastAPI_DB.schemas.review import Review, ReviewCreate 
from FastAPI_DB.repositories.reviews import load_all, save_all

"""Methods for handling reviews

createReview: creates a review with a given review_id and adds it to reviews json
removeReview: removes a review using the review_id. Returns a message for confirmation
getReviewsByRestaurantId: returns all reviews for a given restaurant, 
                          only returns the rating and comment fields for anonymity
"""





def createReview(payload: ReviewCreate):
    reviewId = str(payload.restaurant_id) + "-" + payload.customer_name
    review = Review(review_id=reviewId, restaurant_id=payload.restaurant_id, customer_name=payload.customer_name, rating=payload.rating, comment=payload.comment)
    reviews = load_all()
    reviews.append(review.model_dump())
    save_all(reviews)
    return review

def removeReview(review_id: str):
    reviews = load_all()
    reviews = [review for review in reviews if review["review_id"] != review_id]
    save_all(reviews)
    return {"message": "review " + review_id + " removed"}

def getReviewsByRestaurantId(restaurant_id: int):
    reviews = load_all()
    restaurant_reviews = [Review(**review).model_dump(include={"rating", "comment"}) for review in reviews if review["restaurant_id"] == restaurant_id]
    return restaurant_reviews




