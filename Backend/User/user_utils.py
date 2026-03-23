import random

from FastAPI_DB.services.orders_service import get_order_by_order_id
from FastAPI_DB.services.items_service import get_item_by_item_ID
from FastAPI_DB.services.search_service import create_search
from FastAPI_DB.schemas.search import SearchCreate, Search

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
		print("Select Valid Option: \n(0) Search\n(1) View Order Status\n(2) Create or Edit Order\n(3) Log out")
		while(True): # for ensuring valid actions
			option = input()
			if (option == "0" or option == "1" or option == "2" or option == "3"):
				break
			print("Invalid Entry. Try Again.")
		if (option == "0"): 
			search()
		elif (option == "1"):
			view_order_status(user_id) 
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
	while(True): # for repeated searches
		print("Select Valid Option: \n(0) Search by price low to high\n(1) Search by price high to low\n(2) Exit search engine")
		while(True): # for ensuring valid entry of filter
				option = input()
				if (option == "0" or option == "1" or option == "2"):
					break
				print("Invalid Entry. Try Again.")
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
			print("\nSelect Valid Option: \n(0) Next Page\n(1) Previous Page\n(2) Exit Search")
			while(True): # for ensuring valid entry of filter
				option = input()
				if (option == "0" or option == "1" or option == "2"):
					break
				print("Invalid Entry. Try Again.")
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
	print("Page " + str(index%num_pages+1) + " of "+ str(num_pages+1))
	
	for j in range(len(search.search_results[index%num_pages])):
		item = get_item_by_item_ID(search.search_results[index%num_pages][j])
		print(str(item.item_id) + "  \t" + str(item.price))
	pass
	return True

def view_order_status(user_id):
	"""
	Lists all orders corresponding to user, with their associated statuses.
	
	"""
	pass

def create_or_edit_order(user_id):
	"""
	Lists all orders corresponding to user
	"""
	pass

def driver_branch():
	pass

def manager_branch():
	pass