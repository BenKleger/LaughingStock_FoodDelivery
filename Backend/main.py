from fastapi import FastAPI
from FastAPI_DB.routers.users import router as users_router
from FastAPI_DB.routers.orders import router as orders_router
from FastAPI_DB.routers.items import router as items_router
from FastAPI_DB.routers.menus import router as menus_router
from User.login_auth import login
from FastAPI_DB.services.users_service import get_user_by_id
from User import customer_branch, driver_branch, manager_branch

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(users_router)
app.include_router(orders_router)
app.include_router(items_router)
app.include_router(menus_router)

if __name__ == "__main__":  
    """Main branch of operations"""

    """LOGIN (or Create account)"""
    user_id = login()

    """Depending on user type have separate functionalities."""
    user_type = get_user_by_id(user_id).type
    if user_type == 1:
        """Customer functionality"""
        customer_branch(user_id)

    elif user_type == 2:
        """Driver functionality"""
        driver_branch(user_id)

    elif user_type == 3:
        """Manager functionality"""
        manager_branch(user_id)