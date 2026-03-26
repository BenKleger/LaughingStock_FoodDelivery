from FastAPI_DB.services.orders_service import get_order_by_order_id
from FastAPI_DB.services.users_service import get_user_by_id
from FastAPI_DB.schemas.user import Driver
from User.user_utils import check_input, view_order_status, alter_order_json, alter_user_json, load_orders

#By Ben
def driver_branch(user_id):
	"""	
	Responsible for all driver logic in main branch.

	Allows driver users to:
		0. Search for available orders (in "paid" status)
		1. View current orders taken
		2. View distance for an order taken
		3. start delivery of a taken order
		3. Logout
	"""
	while(True): 
		driver: Driver = get_user_by_id(user_id)
		print("Select Valid Option: '0' Search paid orders (awaiting drivers), '1' View Orders Accepted, '2' Accept an order, '3' Log out")
		option = check_input(["0","1","2", "3"])
		print()
		if (option == "0"): 
			driver_search()
		elif (option == "1"):
			view_order_status(driver) 
		elif (option == "2"):
			accept_order(driver)
		elif (option == "3"):
			break

def driver_search():
	"""
	Returns:
		list of order IDs in the 'paid' status
	prints: 
		Availible orders for pickup (in 'paid' status)				
	"""
	orders = load_orders()
	paid_orders = []
	for order in orders:
		if order.get("order_status") == "paid":
			paid_orders.append(order.get("order_id"))
	
	for orderID in paid_orders:
		order = get_order_by_order_id(orderID)
		print("OrderID:", order.order_id, "\nStatus:",order.order_status,"\nOrder Distance:", str(order.delivery_distance), "\nOrder Value", str(order.order_value))
	
	if(len(paid_orders) == 0):
		print("There are no paid orders available!")
		return []
 
	return paid_orders

def accept_order(driver:Driver):
	paid_orders = driver_search()
	if(len(paid_orders) == 0):
		return
	
	paid_order_list_dict:dict = {}
	i: int = 0
	for orderID in paid_orders:
		order = get_order_by_order_id(orderID)
		if order.order_status == "paid":
			paid_order_list_dict[i] = orderID
			i += 1

	print("Select order to accept:")
	for key,value in paid_order_list_dict.items():
		print("Enter '" + str(key) + "' for order with ID: " + value)
	print("Enter 'q' to exit")
 
	while(True):
		inputted_value = input()
		if inputted_value == 'q':
			return
		try:
			if int(inputted_value) in paid_order_list_dict:
				break
			print("Invalid entry. Try again.")
		except:
			print("Invalid entry. Try again.")
	print()
	order_id = paid_order_list_dict[int(inputted_value)]
	order = get_order_by_order_id(order_id)
	driver.ordersTaken.append(order_id)
	order.order_status = "accepted"
	alter_order_json(order)
	alter_user_json(driver)