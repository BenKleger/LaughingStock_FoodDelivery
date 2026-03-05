
class itemClass:
    itemID: str
    itemName: str
    itemTags: list[str]
    itemPrice: float
    itemRating: float

    def __init__(self, price: float = 0, ID: str = 0,name:str = "", tags: list[str] = [], rating: float = 0):
        """Initialize items with default values if none have been given."""
        
        self.itemPrice = price
        self.itemID = ID
        self.itemName = name
        self.itemTags = tags
        self.itemRating = rating