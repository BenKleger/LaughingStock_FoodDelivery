from ..FastAPI_DB.services.orders_service import get_order_by_order_id
# from FastAPI_DB.schemas.order import Order

        ### PLACEHOLDER ###
# Will need to figure out where to store these and how these variables are managed
delivery_vars = {
  "rate_per_km": 0.2,
  "surge_price_time": [6, 8],
  "surge_price_inf": 1.13,
  "tax": 1.13
}

surge_condition = False

def get_order_cost(user_order_id: str, tip: float, discount: float) -> float:
    user_order = get_order_by_order_id(user_order_id)

    price = user_order["order_value"] * (1 - discount)
    tax = price * user_order["tax"]
    delivery_cost = user_order["delivery_distance"] * user_order["rate_per_km"] * (delivery_vars["surge_price_inf"] if surge_condition else 1)

    cost = price + tax + delivery_cost + tip

    return round(cost, 2)