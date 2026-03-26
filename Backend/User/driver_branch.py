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

	return paid_orders

def accept_order(driver:Driver):
	paid_orders = driver_search()
	print("Enter a valid OrderID in the list of 'paid' orders, or 'q' to quit")
	while True:
		order_id = input()
		if order_id in paid_orders:
			break
		if order_id == 'q':
			return
		print("Invalid order ID")
	print()
	order = get_order_by_order_id(order_id)
	driver.ordersTaken.append(order_id)
	order.order_status = "accepted"
	alter_order_json(order)
	alter_user_json(driver)