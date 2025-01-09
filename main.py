from typing import Union 
from fastapi import FastAPI,HTTPException
from app.signup import verification_on_signup
from app.models.signup_models import signup
from app.models.google_models import google_user
from app.models.login_models import login
from app.models.oauth_models import Token
from app.login import user_login
import logging 
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from app.services_oauth import oauth,userexists_google,create_user_google,create_access_token
from authlib.integrations.base_client import OAuthError
from authlib.oauth2.rfc6749 import OAuth2Token
from datetime import timedelta
from app.routers.token_router import router as token

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

origins = ["http://127.0.0.1:8000/google"]

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["*"],    
    allow_headers=["*"],
)


app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

@app.post("/login")
async def login(data:login):
   user_login(data)
   return {"message":"Successful Login"}

@app.post("/sign-up")
async def signup(data:signup):
    verification_on_signup(data)
    return{"message":"Succesful Sign-up"}


GOOGLE_REDIRECT_URI = "http://127.0.0.1:8000/callback/google"

app.include_router(token,prefix="/token",tags=["Token"])

@app.get("/google")
async def login_google(request: Request):
    return await oauth.google.authorize_redirect(request, GOOGLE_REDIRECT_URI)

@app.get("/callback/google")
async def auth_google(request: Request):
    logging.info("in callback")
    try:
        user_response: OAuth2Token = await oauth.google.authorize_access_token(request)
        
        logging.info("User response received.")
        user_info = user_response.get("userinfo")
        
        #return{"INFORMATION":user_info}
        if(userexists_google(user_info["email"])):
            user_data=google_user(email=user_info["email"],username=user_info["name"])
            token=create_access_token(user_data,timedelta(days=7))
            return Token(access_token=token)
        else:
            user_data=google_user(email=user_info["email"],username=user_info["name"])
            create_user_google(user_data)
            
            token=create_access_token(user_data,timedelta(days=7))

            return Token(access_token=token)
    except OAuthError:
        print("error")
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
