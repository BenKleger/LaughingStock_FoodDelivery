from fastapi import FastAPI
from Backend.FastAPI_DB.routers.users import router as users_router
from Backend.User.login_auth import login

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(users_router)


if __name__ == "__main__":
    user_id = login() #Use : "python -m Backend.main" to run the login function in the terminal. 
              
