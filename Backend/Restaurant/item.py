
class itemClass:

    def __init__(self, price: float = 0, ID: str = 0,name:str = "", tags: list[str] = [], rating: float = 0):
        """Initialize items with default values if none have been given."""
            
        self.itemPrice: float = price
        self.itemID: str = ID
        self.itemName: str = name
        self.itemTags: list[str] = tags
        self.itemRating: float = rating