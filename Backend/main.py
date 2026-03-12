from fastapi import FastAPI
from FastAPI_DB.routers.users import router as users_router
from FastAPI_DB.routers.orders import router as orders_router
from FastAPI_DB.routers.items import router as items_router
from FastAPI_DB.routers.menus import router as menus_router
from User.login_auth import login

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(users_router)
app.include_router(orders_router)
app.include_router(items_router)
app.include_router(menus_router)

user_id = login()