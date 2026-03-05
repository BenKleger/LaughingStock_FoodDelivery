from Restaurant.item import itemClass as item


class orderClass:
    order_index = 0
    order_list = list[item]
    order_instructions = ""

    def __init__(self, i : item):
        self.add_item(i)
        
        
    def __init__(self, list : list[item]):
        for i in list:
            self.add_item(i)


    def add_item(self, i: item):
        self.order_list[self.order_index] = i
        self.order_index += 1

    def remove_item(self, i: item):
        self.order_list.remove(i)
        self.order_index -= 1

    def remove_item(self, index: int):
        self.order_list.remove(index)
        self.order_index -= 1

    def set_order_instructions(self, instructions: str = "No special instructions :)"):
        self.order_instructions = instructions

    def get_total(self):
        total = 0
        for item in self.order_list:
            total += item.item_total
        return total
