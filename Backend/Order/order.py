from Backend.Restaurant.item import item

class order:
    def __init__(self, i : item):
        """initializes order with an item"""
        
        self.order_size: int = 0
        self.order_ID: str = ""
        self.order_list: list[item] = []
        self.order_instructions = ""
        
        if isinstance(i, item):
           self.add_item(i)
        else:
            raise Exception("Invalid type for initialization item")
            pass #TODO Exception behaviour    
       
    def add_item(self, i: item):
        if isinstance(i,item):
            self.order_list.append(i)
            self.order_size += 1
        else:
            # TODO Exception behaviour.
            pass

    def remove_item(self, i):
        """Removes an item using the item itself or the index of an item"""
        if type(i) == int:
            if i < self.order_size:
                self.order_list.pop(i)
                self.order_size -= 1
            else:
                # TODO Exception behaviour.
                pass
        elif isinstance(i,item):
            if self.order_list.__contains__(i):
                self.order_list.remove(i)
                self.order_size -= 1
            else:
                # TODO Exception behaviour.
                pass
        else:
            # TODO Exception behaviour.
            pass


    def set_order_instructions(self, instructions: str = "No special instructions :)"):
        """Sets order instructions :)"""
        if type(instructions) == 'str':
            self.order_instructions = instructions
        else:
            pass #TODO exceptional behaviour


    def get_total(self):
        """Gets the total value of the order, not including tips or taxes"""
        total = 0
        for item in self.order_list:
            total += item.itemPrice
        return total