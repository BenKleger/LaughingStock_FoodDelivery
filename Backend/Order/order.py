from Restaurant import item

order_index = 0
order = list[item()]
order_instructions = ""

def order(i : item):
    pass

def add_item(i: item):
    order[order_index] = i
    order_index += 1

def remove_item(i: item):
    order.remove(i)
    order_index -= 1

def remove_item(index: int):
    order.remove(index)
    order_index -= 1

def set_order_instructions(instructions: str = "No special instructions :)"):
    order_instructions = instructions

