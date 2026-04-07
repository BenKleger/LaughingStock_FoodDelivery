from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from FastAPI_DB.routers.users import router as users_router
from FastAPI_DB.routers.orders import router as orders_router
from FastAPI_DB.routers.items import router as items_router
from FastAPI_DB.routers.menus import router as menus_router
from FastAPI_DB.routers.payment import router as payment_router
from FastAPI_DB.routers.order_cost import router as order_cost_router
from FastAPI_DB.routers.search import router as search_router
from User.login_auth import login
from FastAPI_DB.services.users_service import get_user_by_id
from User import customer_branch, driver_branch, manager_branch
from User.manager_branch import manager_branch
from User.customer_branch import customer_branch
from User.driver_branch import driver_branch


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"status": "running"}

app.include_router(users_router)
app.include_router(orders_router)
app.include_router(items_router)
app.include_router(menus_router)
app.include_router(search_router)
app.include_router(payment_router)
app.include_router(order_cost_router)

#if __name__ == "__main__":  
 #   """Main branch of operations"""
#
 #   """LOGIN (or Create account)"""
  #  while True:
   #     option = input("Select an option: '0' Login / Register, '1' Exit\n")
    #    if(option != "0" and option != "1"):
     #       print("Invalid option! Try again.")
      #      continue

#        if option == "1":
 #           break
        

  #      print()
   #     
    #    user_id = login()
     #   if user_id is None:
      #      break

       # """Depending on user type have separate functionalities."""
        #user_type = get_user_by_id(user_id).type
#        if user_type == 1:
 #           """Customer functionality"""
  #          customer_branch(user_id)
#
 #       elif user_type == 2:
  #          """Driver functionality"""
  #
   #     elif user_type == 3:
    #        """Manager functionality"""
     #       manager_branch(user_id)