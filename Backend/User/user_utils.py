from ..FastAPI_DB.services.orders_service import get_order_by_order_id
# from FastAPI_DB.schemas.order import Order

        ### PLACEHOLDER ###
delivery_vars = {
  "rate_per_km": 0.2,
  "surge_price_time": [6, 8],
  "surge_price_inf": 1.13,
  "tax": 1.13
}

surge_condition = True

def get_order_cost(user_order_id: str, tip: float, discount: float) -> float:
    user_order = get_order_by_order_id(user_order_id)

    price = user_order["order_value"]
    tax = price * user_order["tax"]
    delivery_cost = user_order["delivery_distance"] * user_order["rate_per_km"] * (delivery_vars["surge_price_inf"] if surge_condition else 1)

    cost = (price * (1 - discount)) + tax + delivery_cost + tip

    return cost

# As a user, I want to be able to know the total cost of the food before purchase, 
# so that I know if I’m willing to buy it.

# Acceptance criteria:
# Order list contains summary details including pricing of each individual item, 
# total cost, tax, discount, delivery free, tip%, fees. Updates to the order list are 
# reflected in summary details within ~2 seconds.
# Once an order is placed and confirmed the price remains fixed.