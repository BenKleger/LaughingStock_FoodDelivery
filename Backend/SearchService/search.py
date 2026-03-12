# from Backend.Restaurant import restaurant
from Backend.Restaurant import menu, item

class searchService:

    def __init__(self, searchTerm: str = "", itemTags: list[str] = [],
             restaurantType: str = "", restaurantRating: dict = {"lowerBound": 0, "upperBound": 5},
             itemRating: dict = {"lowerBound": 0, "upperBound": 5},
             priceRange: dict = {"lowerBound": 0, "upperBound": 1000}):
        self.searchTerm = searchTerm
        self.itemTags = itemTags
        self.restaurantType = restaurantType
        self.restaurantRating = restaurantRating
        self.itemRating = itemRating
        self.priceRange = priceRange

    