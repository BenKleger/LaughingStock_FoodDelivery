import random

from FastAPI_DB.services.orders_service import get_order_by_order_id
from FastAPI_DB.services.items_service import get_item_by_item_ID
from FastAPI_DB.schemas.order_cost import OrderCostCreate

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