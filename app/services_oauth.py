from fastapi import HTTPException
from datetime import timedelta, datetime, UTC
from typing import Annotated
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from authlib.integrations.starlette_client import OAuth
import os
from starlette.config import Config
import app.database.config_user as DB
from app.models.google_models import google_user
from app.models.oauth_models import Token
from jose import JWTError,jwt

oauth_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID') or None
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET') or None

if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise Exception('Missing env variables')

config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}

starlette_config = Config(environ=config_data)

oauth = OAuth(starlette_config)

oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)


def userexists_google(email:str)->bool:
   if DB.collection.count_documents({"email":email})==0:#count_document returns the number of matches in db if 0 that means no user exitst
      return False
   return True


def create_user_google(data:google_user):#gets data from api endpoints 
   put_data_inDB(data)#call the below funciton
   
def put_data_inDB(data:google_user):#puts the data in the database
   try:
      DB.collection.insert_one(data.model_dump())#getting a type error when inserting .. so converting to dict by model_dump function(dicT() funtion was deprecated by pydantic)
   except Exception as e:
      raise HTTPException(status_code=500,detail=str(e))
   


   #-------ACCESS TOKEN FUNC----------#

def create_access_token(data:google_user,expire_time:timedelta):
   expire_time=datetime.now(UTC)+expire_time
   encode={
      "email":data.email,
      "username":data.username,
      "expire time":expire_time.timestamp()
   }
   try:
      new_token=jwt.encode(encode,os.getenv("SESSION_SECRET_KEY"),algorithm="HS256")
      return new_token
   except Exception as e:
      raise HTTPException(status_code=400,detail=str(e))


def refresh_access_token(data:google_user,expire_time:timedelta):
   return create_access_token(data,expire_time)

def decode_access_token(token:str):
   try:
      user_data=jwt.decode(token,os.getenv("SESSION_SECRET_KEY"),algorithms="HS256")
      return user_data
   except Exception as e:
      raise HTTPException(status_code=400,detail=str(e))

def current_user_data(token:str):
   user_data=decode_access_token(token)

   email=user_data["email"]

   if(DB.collection.count_documents({"email":email})==0):
      raise HTTPException(status_code=500,detail="Invalid Access Token Recieved")
   return user_data
   
def is_token_expired(token:str):
   user_data=decode_access_token(token)

   expire_time=user_data["expire time"]
   if datetime.fromtimestamp(expire_time,UTC)>datetime.now(UTC):
      return False
   return True