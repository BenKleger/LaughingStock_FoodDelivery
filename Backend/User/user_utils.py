import random

from FastAPI_DB.services.menus_service import get_menu_by_menu_ID
from FastAPI_DB.services.orders_service import get_order_by_order_id, add_order_item, delete_order_item, delete_order
from FastAPI_DB.services.items_service import create_items, get_item_by_item_ID, create_items
from FastAPI_DB.services.users_service import get_user_by_id
from FastAPI_DB.repositories.user_repo import load_all as load_users, save_all as save_users
from FastAPI_DB.repositories.order_repo import load_all as load_orders, save_all as save_orders
from FastAPI_DB.repositories.menu_repo import load_all as load_menu, save_all as save_menus
from FastAPI_DB.repositories.item_repo import load_all as load_items, save_all as save_items	
from FastAPI_DB.schemas.order import Order
from FastAPI_DB.schemas.item import ItemCreate
from FastAPI_DB.schemas.user import User, Customer, Driver

"""System Variable"""
delivery_vars = {
	"rate_per_km": 0.7,
	"tax": 0.13
}

def get_order_cost(user_order_id: str, tip: float):
	"""
		Gets order cost based on distance and initial item price

		Parameters:
			user_order_id (str): order id of order being created
			tip (float): user tip

		Returns:
			cost: order cost
			distance: (randomly generated 1-25)
			

		Description:
			The function gets the order id passed into it. Looks up item cost in
			items.json database. Tacks on tax, tip, and delivery costs to get
			final order price.

			Distance is randomly generated from 1-25km.

			Delivery cost is $7 base cost, or $2 plus delivery cost. (Increased for distances over 10km)
	"""

	user_order = get_order_by_order_id(user_order_id)
	user_item = get_item_by_item_ID(user_order.item_ids[0])
	min_distance = 1
	max_distance = 25
	number_decimal_places = 2
	auto_gen_distance = round(random.uniform(min_distance, max_distance), number_decimal_places)

	price = user_item.price
	tax = price * delivery_vars["tax"]
	min_cost = 7
	cost_bump_for_long_distances = 2
	delivery_cost = min_cost if (auto_gen_distance * delivery_vars["rate_per_km"] < min_cost) else cost_bump_for_long_distances + (auto_gen_distance * delivery_vars["rate_per_km"])

	cost = price + tax + delivery_cost + tip

	return round(cost, number_decimal_places), auto_gen_distance

def check_input(allowed_values: list[str]):
	"""
	Helper function to skip the while loop for checking user input.

	Input: list of options (list[])
	Output: valid user input
	"""
	option = ""
	while(True):
		option = input().strip()
		if(option in allowed_values):
			break
		print("Invalid entry. Try again.")
	print()
	return option

def view_order_status(user):
	"""
	Lists all orders corresponding to user, with their associated statuses.
	
	Functions for drivers and customers
	
	Decrements the distance on an order when called from a customer :)
	"""

	if isinstance(user, Customer):
		customer:Customer = user
		if(len(customer.ordersList) == 0):
			print("\nNo orders associated with account.\n")
			return
		
		else:
			for order_id in customer.ordersList:
				order = get_order_by_order_id(order_id)
				if order.order_status == "accepted":
					if order.delivery_distance > 1:  
						order.delivery_distance = round(order.delivery_distance-1,2)
					else: 
						order.delivery_distance = 0
						order.order_status = "delivered"
						print("\n\nOrder has been Delivered!\n\n")
				alter_order_json(order)
				print("Order: "+ order_id+"\nStatus: " + order.order_status+"\nDistance Remaining: "+ str(order.delivery_distance)+"km\nItems:")
				if len(order.item_ids) == 0:
					print("\tNo items in order")
					return
				for item_id in order.item_ids:
					item = get_item_by_item_ID(item_id)
					print("\t"+item.name+ ": $" + str(item.price))			
				print()

	elif isinstance(user, Driver):
		driver:Driver = user
		if(len(driver.ordersTaken) == 0):
			print("\nNo orders associated with account.\n")
			return
		else:
			for order_id in driver.ordersTaken:
				order = get_order_by_order_id(order_id)
				print("Order: "+ order_id+"\nStatus: " + order.order_status+"\nDistance: " + str(order.delivery_distance)+"km\nItems:")
				if len(order.item_ids) == 0:
					print("\tNo items in order")
					return
				for item_id in order.item_ids:
					item = get_item_by_item_ID(item_id)
					print("\t"+item.name+ ": $" + str(item.price))
				print()	
	
def get_item_input():
	while(True):
		item_id = input()
		if item_id == "q":
			return 'q'
		try:
			return get_item_by_item_ID(item_id)
		except:
			print("Invalid Entry. Try again.")

def alter_user_json(new_user: User):
	"""
	Changes json file to include the updated information
	"""
	users = load_users()
	for user in users:
		if user.get("id") == new_user.id:
			user.update(new_user)
			break
	save_users(users)

def add_item_to_order(order_id):
	"""
	Adds item to the associated.
	"""
	print("Input item id to add to order, or 'q' to cancel editing order:")
	item = get_item_input()
	if item == 'q':
		return
	
	add_order_item(order_id, item.item_id)

def remove_item_from_order(order_id):
	order = get_order_by_order_id(order_id)
	empty = 0
	if(len(order.item_ids) == empty):
		print("No items in order!")
		return
	
	print("Item ids in order:")
	for item_id in order.item_ids:
		print(item_id)

	print("Enter an item id in the order to be removed, or 'q' to quit.")
	while(True):
		inputted_value = input()
		if inputted_value == "q":
			return 'q'
		if(inputted_value in order.item_ids):
			break
		print("Invalid Entry. Try again.")

	delete_order_item(order_id, inputted_value)
	print()

def del_order(order_id,user_id):
	"""
	Deletes the order.
	"""
	print("Are you sure you wish to delete this order? (y)-Yes, Anything else-No")
	confirm = input()
	if confirm == 'y':
		user: Customer = get_user_by_id(user_id)
		user.ordersList.remove(order_id)
		alter_user_json(user)
		delete_order(order_id)
		print("\nOrder Sucessfully Deleted!\n")

def alter_order_json(new_order: Order):
	"""
	Changes json file to include the updated information
	"""
	orders = load_orders()
	for order in orders:
		if order.get("order_id") == new_order.order_id:
			order.update(new_order)
			break
	save_orders(orders)
		
def view_menu(restaurant_id):
	menu = get_menu_by_menu_ID(str(restaurant_id)).items
	empty = 0
	if len(menu) == empty:
		print("no items/ no menu")
		return
	print("Item id \t\t Item name \t\t Price")
	for item in menu:
		print(str(item.item_id) + " \t\t" + item.name + " \t\t $" + str(item.price)) 

def add_menu_item(restaurant_id): 
	"""
	Adds a new item created by the manager to the menu and item database

	checks that item name is valid
		and that a valid float and positive price check
	"""
	print("Enter new item name or 'q' to exit")
	while(True):
		item_name = input()
		if item_name == 'q':
			return
		elif(item_name.isalpha() or (len(item_name)>4 and len(item_name)<20)): 
			break
		print("Invalid entry try again:")

	print("Enter new item price or 'q' to exit")
	while(True):
		item_price = input()
		if item_price == 'q':
			return 
		elif(isFloat(item_price) and float(item_price) > 0): 
			break
		print("Invalid entry try again:")

	item_id = str(restaurant_id) + "-" + item_name
	new_Item = ItemCreate(item_id = item_id, restaurant_id = restaurant_id, name = item_name, tags = [], price = float(item_price))
	create_items(new_Item)

	menus = load_menu()
	for menu in menus:
		if menu["menu_id"] == restaurant_id:
			menu["items"].append(new_Item.model_dump()) #note to self:model dump converts the model to dict
	save_menus(menus)
	print("Item added to menu and item database!")

def remove_menu_item(restaurant_id):
	"""
	Removes an item from the menu
	"""
	menu = get_menu_by_menu_ID(str(restaurant_id)).items
	if len(menu) == 0:
		print("No items/ no menu")
		return
	print("Enter item id to remove or 'q' to exit")
	while(True):
		user_input = input()
		if user_input == 'q':
			return
		else:
			match = False 
			for item in menu:
				if item.item_id == user_input:
					match = True
					break
			if match:
				menus = load_menu()
				for menu in menus:
					if menu["menu_id"] == restaurant_id:
						menu["items"] = [item for item in menu["items"] if item["item_id"] != user_input]
						break
				save_menus(menus)
				items = load_items()
				items = [item for item in items if item["item_id"] != user_input] 
				save_items(items)
				print("Item removed from menu and item database")
				return
			print("No such item id in menu, try again:")

def isFloat(string): 
	"""
	float check helper function 
	Returns 
		true if string can be converted to a float
		false otherwise
	"""
	try:
		float(string)
		return True
	except ValueError:
		return False



