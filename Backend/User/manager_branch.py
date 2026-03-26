from FastAPI_DB.services.users_service import get_user_by_id
from FastAPI_DB.repositories.user_repo import load_all as load_users
from FastAPI_DB.repositories.order_repo import load_all as load_orders	
from FastAPI_DB.repositories.menu_repo import load_all as load_menu, save_all as save_menus	
from FastAPI_DB.repositories.item_repo import load_all as load_items, save_all as save_items	
from FastAPI_DB.schemas.user import Manager
from User.user_utils import check_input, alter_user_json, isFloat
from fastapi import HTTPException
from FastAPI_DB.services.menus_service import get_menu_by_menu_ID
from FastAPI_DB.schemas.item import Item, ItemCreate
from FastAPI_DB.services.items_service import create_items

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
		
def view_menu(restaurant_id):
	try:
		menu = get_menu_by_menu_ID(str(restaurant_id)).items
	except HTTPException:
		print("no items/ no menu")
		return
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

	menu_exists = any(menu["menu_id"] == restaurant_id for menu in menus) #checks if a menu for manager alr exists
	if not menu_exists:
		new_menu = {"menu_id": restaurant_id, "items": [new_Item.model_dump()]}
		menus.append(new_menu)
	else:
		for menu in menus:
			if menu["menu_id"] == restaurant_id:
				menu["items"].append(new_Item.model_dump()) #note to self:model dump converts the model to dict
				break

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
