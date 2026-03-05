from fastapi import FastAPI
from FastAPI_DB.routers.users import router as users_router
from User.login_auth import login

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

def test_null():
    assert True is True
app.include_router(users_router)

user_id = login()
