import random
import json
import datetime


from FastAPI_DB.services.orders_service import get_order_by_order_id, create_orders, add_order_item, delete_order_item, delete_order
from FastAPI_DB.services.items_service import get_item_by_item_ID
from FastAPI_DB.services.search_service import create_search
from FastAPI_DB.services.users_service import get_user_by_id
from FastAPI_DB.services.payment_processor_service import process_payment, validatePaymentMethod
from FastAPI_DB.repositories.user_repo import load_all as load_users, save_all as save_users
from FastAPI_DB.repositories.order_repo import load_all as load_orders, save_all as save_orders
from FastAPI_DB.schemas.search import SearchCreate, Search
from FastAPI_DB.schemas.order import OrderCreate, Order
from FastAPI_DB.schemas.user import User, Customer, Driver, Manager
from FastAPI_DB.schemas.payment_processor import PaymentProcessorCreate

# System variables
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

			Delivery cost is 7 base cost, or $2 plus delivery cost. (Increased for distances over 10km)
	"""

	user_order = get_order_by_order_id(user_order_id)
	user_item = get_item_by_item_ID(user_order.item_ids[0])

	auto_gen_distance = round(random.uniform(1, 25), 2)

	price = user_item.price
	tax = price * delivery_vars["tax"]
	delivery_cost = 7 if (auto_gen_distance * delivery_vars["rate_per_km"] < 7) else 2 + (auto_gen_distance * delivery_vars["rate_per_km"])

	cost = price + tax + delivery_cost + tip

	return round(cost, 2), round(auto_gen_distance, 2)

def customer_branch(user_id: str):
	"""
	Responsible for all customer logic in main branch.

	Allows customer users to:
		0. Search (by restauarants, items, or item_ids)
		1. View order status on all of their orders
		2. Create or Edit (assuming it is in being_created status) an order
		3. Logout
	"""
	while(True): # for repeated actions
		customer: Customer = get_user_by_id(user_id)
		print("Select Valid Option: '0' Search, '1' View Order Status, '2' Create or Edit Order, '3' Log out")
		option = check_input(["0","1","2","3"])
		if (option == "0"): 
			search()
		elif (option == "1"):
			view_order_status(customer) 
		elif (option == "2"):
			create_or_edit_order(user_id)
		elif (option == "3"):
			#write back customer with changes to the DB #TODO
			break

def check_input(allowed_values: list[str]):
	"""
	Helper function to skip the while loop for checking user input.

	Input: list of options (int[])
	Output: valid user input
	"""
	option = ""
	while(True):
		option = input().strip()
		if(option in allowed_values):
			break
		print("Invalid entry. Try again.")
	return option

def search():
	"""
	Allows user to first select their filtering option,
	then allows them to enter their search query,
	prints: 
		Paginated search query results
		Allowing user to go forward or back pages, or exit.
	"""
	while(True): # for repeated searches
		print("Select Valid Option: '0' Search by price low to high, '1' Search by price high to low, '2' Exit search engine")
		option = check_input(["0","1","2"])
		if option == "0":
			search_filter = "price_low_to_high"
		elif option == "1":
			search_filter = "price_high_to_low"
		else:
			break
		
		print("Enter your search query")
		search_query = input()
		
		search:Search = create_search(SearchCreate(query=search_query, filter=search_filter))
		index = 0
		valid_search = display_page(search, index)
		while(valid_search): # for repeated changes in page
			print("\nSelect Valid Option: '0' Next Page, '1' Previous Page, '2' Exit Search")
			option = check_input(["0","1","2"])
			if option == "0":
				index+=1
				display_page(search,index)
			elif option == "1":
				index-=1
				display_page(search,index)
			else:
				break
	
def display_page(search: Search, index: int):
	"""
	Displays page number index of the search.

	Returns:
		True if items are within the search.
		False if no items with the given query exist.
	"""
	if(len(search.search_results) == 0):
		print("No search results\n")
		return False #
	
	num_pages = len(search.search_results)
	print("Page " + str(index%num_pages+1) + " of "+ str(num_pages))
	print("Item id   \tPrice")
	
	for j in range(len(search.search_results[index%num_pages])):
		item = get_item_by_item_ID(search.search_results[index%num_pages][j])
		print(str(item.item_id) + "  \t$" + str(item.price))
	return True

def view_order_status(customer: Customer):
	"""
	Lists all orders corresponding to user, with their associated statuses.
	
	No separate options in this function.
	"""

	if(len(customer.ordersList) == 0):
		print("\nNo orders associated with account.\n")
		return
	
	else:
		for order_id in customer.ordersList:
			order = get_order_by_order_id(order_id)
			print("Order: "+ order_id+"\nStatus: " + order.order_status+"\nItems:")
			if len(order.item_ids) == 0:
				print("\tNo items in order")
				return
			for item_id in order.item_ids:
				item = get_item_by_item_ID(item_id)
				print("\t"+item.name+ ": $" + str(item.price))			
			print()

def create_or_edit_order(user_id):
	"""
	Lists all orders corresponding to user
	"""
	while(True): # for repeated actions
		print("Select Valid Option: '0' Create Order, '1' Edit Order, '2' Exit Order Changes")
		customer:Customer = get_user_by_id(user_id)
		option = check_input(["0","1","2"])

		if option == "0":
			create_new_order(customer)
		elif option == "1":
			edit_order(customer)
		else:
			break

def create_new_order(customer: Customer):
	"""
	Creates an order, adding it to both the order database (json), as well as
	the user's orderlist
	"""
	print("Input item id to initialize order, or 'q' to cancel order creation:")
	item = get_item_input()
	if item == 'q':
		return
	new_order_create = OrderCreate(restaurant_id=item.restaurant_id, 
							food_item = item.name,
							order_time = str(datetime.datetime.now())[:10], 
							delivery_time = "TBD", 
							delivery_distance = round(random.uniform(1, 25), 2), 
							order_value = 7 + item.price, 
							delivery_method = "Car", 
							traffic_condition = "Clear", 
							weather_condition = "Sunny",
							item_ids = [str(item.restaurant_id) + "-" + item.name],
							order_status="being_created")
	new_order = create_orders(new_order_create)
	customer.ordersList.append(new_order.order_id)
	alter_user_json(customer)
	print("\n\nOrder Sucessfully Added!\n\n")
	
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

def edit_order(customer:Customer):
	"""
	Allows the user to add, remove items from created orders, or complete orders that are in the 'being_created' status
	"""
	
	if(len(customer.ordersList) == 0):
		print("\nNo orders associated with account to edit.\n")
		return
	
	order_list_dict:dict = {}
	i: int = 0
	for orderID in customer.ordersList:
		order = get_order_by_order_id(orderID)
		if order.order_status == "being_created":
			order_list_dict[i] = orderID
			i += 1

	print("Select order to edit:")
	for key,value in order_list_dict.items():
		print("Enter '" + str(key) + "' for order with ID: " + value)
	print("Enter 'q' to exit")

	while(True):
		inputted_value = input()
		if inputted_value == 'q':
			return
		try:
			if int(inputted_value) in order_list_dict:
				break
			print("Invalid entry. Try again.")
		except:
			print("Invalid entry. Try again.")
		
	order_id = order_list_dict[int(inputted_value)]
	while(True): # Can do multiple things in an order
		print("Input '0' To add items, '1' to remove items, '2' to delete the order, '3' to complete order or '4' to quit editing this order")
		option = -1
		option = check_input(["0","1","2","3","4"])
		
		if option == '0': 
			add_item_to_order(order_id)
		elif option == '1': 
			remove_item_from_order(order_id)
		elif option == '2':
			del_order(order_id,customer.id)
			break
		elif option == '3':
			complete_order(order_id,customer.id)
			break
		else: return

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
	if(len(order.item_ids) == 0):
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
		print("Order Sucessfully Deleted!")
		return

def complete_order(order_id, user_id):
	"""
	Prompts the user to input a payment method
	"""
	user: Customer = get_user_by_id(user_id).model_dump()
	order: Order = get_order_by_order_id(order_id).model_dump()
	processor = PaymentProcessorCreate(customer=user,order=order)
	print("Select payment method: '0': Credit, '1': Debit, '2': Apple Pay, '3': Paypal")
	option = check_input(["0", "1", "2", "3"])
	while(True):
		if(option == "0" or option == "1"):
			if option == "0": processor.payment_method = "CREDIT"
			else: processor.payment_method = "DEBIT"
			print("Note: 4 and fifteen 1s is a valid card number")
			processor.payment_number = input("Card number: ")
			processor.payment_pin = input("Payment pin (CVV): ")
			processor.card_holder_name = input("Card holder name: ")
			processor.billing_address = input("Billing address: ")
			print("Note: postal code format is A1A 1A1")
			processor.postal_code = input("Postal code: ")
		if(option == "2" or option =="3"):
			if option == "2": processor.payment_method = "APPLEPAY"
			else: processor.payment_method = "PAYPAL"
			print("Note: email format is name@domain.TLD")
			processor.email = input("Payment email: ")
			processor.email_password = input("Email password: ")
		if process_payment(processor): break
		# updates status to "paid" if everything is valid
		else:
			print("Invalid payment method. Please try again.")
	print("Successeful!")

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

def driver_branch():
	"""	
	Responsible for all driver logic in main branch.

	Allows driver users to:
		0. Search for available orders (in "sent" status)
		1. View current orders taken
		2. View distance for an order taken
		3. start delivery of a taken order
		3. Logout
	"""

def manager_branch():
	"""	
	Responsible for all manager logic in main branch.

	Allows manager users to:
		0. View and select what restaurant they manage. (including create a new restauarant)
		1. View their restaurant's menu
		2. Edit their restauarant's menu
		3. Logout
	"""