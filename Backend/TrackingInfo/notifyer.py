import datetime
from ..FastAPI_DB.services.orders_service import get_order_by_order_id

def order_created(order_id: str):
    print("\n\nNotification:    Order ", order_id, " is successfully created\n\n")

def order_status_chage(order_id: str):
    print("\n\nNotification:    Order ", order_id, " status changed to ", 
          get_order_by_order_id(order_id).order_status, " at ", str(datetime.datetime.now())[17:19], "\n\n")