from FastAPI_DB.services.users_service import get_user_by_id
from FastAPI_DB.repositories.user_repo import load_all as load_users
from FastAPI_DB.repositories.order_repo import load_all as load_orders	
from FastAPI_DB.schemas.user import Manager
from User.user_utils import check_input, alter_user_json, view_menu, add_menu_item, remove_menu_item

#By Aiden
def manager_branch(user_id):
	"""	
	Responsible for all manager logic in main branch.

	Allows manager users to:
		0. View and select what restaurant they manage. (including create a new restauarant)
		1. View their restaurant's menu
		2. Edit their restauarant's menu
		3. Logout
	"""
	while(True):
		Manger: Manager = get_user_by_id(user_id)
		print("Select Valid Option: '0' Manage restuarant, '1' View/edit your restuarant's menu, '2' Log out")
		option = check_input(["0","1","2"])
		if (option == "0"): 
			manage_restaurants(user_id)
		elif(option == "1"):
			manage_menu(user_id)
		elif(option == "2"):
			return

def manage_restaurants(user_id):
	"""
	Allows a manager to add/change their associated restaurant, or create a new one.
	"""
	while(True):
		print("'0' Select your restaurant, '1' create new restaurant, '2' exit")
		option = check_input(["0","1","2"])
		if option == "0":
			select_restaurant(user_id)
		elif option == "1":
			create_restaurant(user_id)
		elif option == "2":
			return


def select_restaurant(user_id):

	"""
	Select your restaurant

	checks if user inputs a valid restaurant id
	"""
	unowned_restaurants = get_unownedRestuarants()
	unowned_restaurants.sort()
	empty = 0
	if len(unowned_restaurants) == empty:
		print("No restaurants available to manage. Please create a new restaurant.")
		return
	
	print("Resuarant Id: ")
	for restaurant_id in unowned_restaurants:
		print(restaurant_id)
	print("Enter the restaurant Id you want to manage. Enter 0(default value) for none, or 'q' to exit")
	while(True):
		user_input = input()
		if user_input == 'q':
			return
		if(int(user_input) in unowned_restaurants): 
			manager:Manager = get_user_by_id(user_id)
			manager.restaurantId = int(user_input)
			alter_user_json(manager)
			print("Restaurant assigned!")
			return
		else:
			print("Invalid entry. Try again:")
		

def get_unownedRestuarants():
	""" 
	Returns restaurants not associated with an manager
	"""
	all_restaurants = []
	for order in load_orders():
		if order["restaurant_id"] not in all_restaurants:
			all_restaurants.append(order["restaurant_id"])

	owned = get_ownedRestuarants()
	return [id for id in all_restaurants if id not in owned]

def get_ownedRestuarants(): 
	""" 
	Returns restaurants associated with an manager
	"""
	owned = [users["restaurantId"] for users in load_users() if users["type"] == 3 and users.get("restaurantId") != None]
	return owned

def create_restaurant(user_id): 
	"""
	This method assumes resaurantIds 1-100 exist, and checks if any other input restaurants are already used.
  And allow the user to input up to restaurant 999
	"""

	print("Enter your new restaurant id(101-999) or 'q' to exit")
	while(True):
		user_input = input()
		if user_input == 'q':
			return
		if (not(user_input.isdigit()) or int(user_input) in get_unownedRestuarants() or int(user_input) in get_ownedRestuarants() or int(user_input) > 999): #check if input is a valid id
			print("Invalid entry, try again:")
		else:
			manager = get_user_by_id(user_id)
			manager.restaurantId = int(user_input)
			alter_user_json(manager)
			print("Restaurant created and assigned!")
			return

def manage_menu(user_id):
	"""
	Allows a manager to view and change their menu items
	"""
	manager = get_user_by_id(user_id)
	no_restaurant = 0
	if manager.restaurantId == no_restaurant:
		print("No restaurant assigned. Please select or create a restaurant first.")
		return

	while(True): 
		print("'0' View menu, '1' Add item, '2' Remove item, '3' Exit")
		user_input = check_input(["0","1","2", "3"])
		if user_input == '0':
			view_menu(manager.restaurantId)
		elif user_input == '1':
			add_menu_item(manager.restaurantId)
		elif user_input == '2':
			remove_menu_item(manager.restaurantId)
		elif user_input == '3':
			return