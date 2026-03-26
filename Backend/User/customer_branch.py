import random
import datetime

from FastAPI_DB.services.orders_service import get_order_by_order_id, create_orders
from FastAPI_DB.services.items_service import get_item_by_item_ID
from FastAPI_DB.services.search_service import create_search
from FastAPI_DB.services.users_service import get_user_by_id
from FastAPI_DB.services.payment_processor_service import process_payment
from FastAPI_DB.schemas.search import SearchCreate, Search
from FastAPI_DB.schemas.order import OrderCreate, Order
from FastAPI_DB.schemas.user import Customer
from FastAPI_DB.schemas.payment_processor import PaymentProcessorCreate
from User.user_utils import check_input, alter_user_json, view_order_status, add_item_to_order, remove_item_from_order, get_item_input, del_order

#By Ben
def customer_branch(user_id: str):
	"""
	Responsible for all customer logic in main branch.

	Allows customer users to do multiple of the following:
		0. Search (by restauarants, items, or item_ids)
		1. View order status on all of their orders
		2. Create or Edit (assuming it is in being_created status) an order
		3. Logout
	
		
	"""
	while(True): 
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
			break

def search():
	"""
	Allows user to first select their filtering option,
	then allows them to enter their search query,
	prints: 
		Paginated search query results
		Allowing user to go forward or back pages, or exit.
	"""
	while(True):
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
		while(valid_search): 
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
			print()

def display_page(search: Search, index: int):
	"""
	Displays page number index of the search.

	Returns:
		True if items are within the search.
		False if no items with the given query exist.
	"""
	if(len(search.search_results) == 0):
		print("No search results\n")
		return False 
	
	num_pages = len(search.search_results)
	print("Page " + str(index%num_pages+1) + " of "+ str(num_pages))
	print("Item id   \tPrice")
	
	for j in range(len(search.search_results[index%num_pages])):
		item = get_item_by_item_ID(search.search_results[index%num_pages][j])
		print(str(item.item_id) + "  \t$" + str(item.price))
	return True

def create_or_edit_order(user_id):
	"""
	Lists all orders corresponding to user
	"""
	while(True): 
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
	print()
	date_digits = 10
	low_distance = 1
	high_distance = 25
	num_decimals = 2
	delivery_fee = 7
	new_order_create = OrderCreate(restaurant_id=item.restaurant_id, 
							food_item = item.name,
							order_time = str(datetime.datetime.now())[:date_digits], 
							delivery_time = "TBD", 
							delivery_distance = round(random.uniform(low_distance, high_distance), num_decimals), 
							order_value = delivery_fee + item.price, 
							delivery_method = "Car", 
							traffic_condition = "Clear", 
							weather_condition = "Sunny",
							item_ids = [str(item.restaurant_id) + "-" + item.name],
							order_status="being_created")
	new_order = create_orders(new_order_create)
	customer.ordersList.append(new_order.order_id)
	alter_user_json(customer)
	print("\n\nOrder Sucessfully Added!\n\n")
 
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
	print()
	order_id = order_list_dict[int(inputted_value)]
	while(True): 
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
  
def complete_order(order_id, user_id):
	"""
	Prompts the user to input a payment method
	
	updates status to "paid" if everything is valid
	"""
	user: Customer = get_user_by_id(user_id).model_dump()
	order: Order = get_order_by_order_id(order_id).model_dump()
	processor = PaymentProcessorCreate(customer=user,order=order)
	print("Select payment method: '0': Credit, '1': Debit, '2': Apple Pay, '3': Paypal")
	option = check_input(["0", "1", "2", "3"])
	while(True):
		try:
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
			else:
				print("Invalid payment method. Please try again.")
		except:
				print("Invalid payment method. Please try again.")