from fastapi import FastAPI,HTTPException
from app.signup import verification_on_signup
from app.models.signup_models import signup
from app.models.login_models import login
from app.login import user_login
import logging 
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from app.routers.token_router import router as token
from app.routers.auth_router import router as auth
from app.routers.restaurant_data_router import router as restaurant
from app.services_oauth import login_oauth

load_dotenv()


logging.basicConfig(
    level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Format for log messages
    handlers=[
        logging.StreamHandler(),  # Log to the console
        logging.FileHandler("app.log"),  # Log to a file named app.log
    ],
)


SECRET_KEY = os.getenv("SECRET_KEY")

origins = ["http://127.0.0.1:8000"]

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["*"],    
    allow_headers=["*"],
)


app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

@app.get("/")
async def hello():
    return{"message":"This is your API running"}

@app.post("/login")
async def login(data:login):
   user_login(data)
   token=login_oauth(data)
   return {"message":"Successful Login","Access Token":token}

@app.post("/sign-up")
async def signup(data:signup):
    verification_on_signup(data)
    return{"message":"Succesful Sign-up"}


app.include_router(token,prefix="/token",tags=["Token"])#router for token 
app.include_router(auth,prefix="/auth",tags=["Auth"])#router for auth
app.include_router(restaurant,prefix="/restaurant",tags=["Restaurant"])#router for data