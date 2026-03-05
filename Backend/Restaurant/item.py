
class itemClass:
    itemID: str
    itemName: str
    itemTags: list[str]
    itemPrice: float
    itemRating: float

    def __init__(self, ID: str = 0,name:str = "", tags: list[str] = [""], price: float = 0, rating: float = 0):
        self.itemID = ID
        self.itemName = name
        self.itemTags = tags
        self.itemPrice = price
        self.itemRating = rating