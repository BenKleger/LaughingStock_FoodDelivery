from FastAPI_DB.services.menus_service import get_menu_by_menu_ID
from FastAPI_DB.services.orders_service import get_order_by_order_id, add_order_item, delete_order_item, delete_order
from FastAPI_DB.services.items_service import create_items, get_item_by_item_ID, create_items
from FastAPI_DB.services.users_service import get_user_by_id
from FastAPI_DB.repositories.user_repo import load_all as load_users, save_all as save_users
from FastAPI_DB.repositories.order_repo import load_all as load_orders, save_all as save_orders
from FastAPI_DB.repositories.menu_repo import load_all as load_menu, save_all as save_menus
from FastAPI_DB.repositories.item_repo import load_all as load_items, save_all as save_items	
from FastAPI_DB.schemas.order import Order
from FastAPI_DB.schemas.user import User, Customer, Driver


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



