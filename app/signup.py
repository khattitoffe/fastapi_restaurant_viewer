from email_validator import validate_email, EmailNotValidError
from passlib.context import CryptContext    
from fastapi import FastAPI,HTTPException
from pymongo import MongoClient
from app.models.signup_models import signup,db_signup
from app.database import config_user as DB

SECRET_KEY="82ec7e26f0936122f079430d773706324c51dbaf6a888877aea0ec00aa9fff64"
ALGORITHM="HS256"

pass_context=CryptContext(schemes=["bcrypt"],deprecated="auto")


def verification_on_signup(data:signup):   #here we start come form the post request of sign-up.. we verify email.. we hash the password and then we put it in the db 
   
   is_username_available(data.username) # check username availability

   try:
        is_email_valid=emailverification(data.email)   #if email is valid we hash the data

        if(is_email_valid):
            db_data=hashpassword(data)
            success=put_data_inDB(db_data)
            if(success):
                return True
            else:
                raise HTTPException(status_code=500,detail="Faild to save Data in DB")    

        else:#not valid email we do not hash
           raise HTTPException(status_code=400,detail="Invalid email address")
   except EmailNotValidError as e:
        raise HTTPException(status_code=400,detail=str(e))


def emailverification(email:str):
   return validate_email(email)
   
def hashpassword(data:signup):#here we hash the data put in json format with other fields and the return it 
   
   hash_password=pass_context.hash(data.password)

   db_signup_data={
       "username":data.username,
       "hashed_password" : hash_password,
       "email":data.email
   }

   return db_signup_data

def put_data_inDB(db_data:db_signup):#in this we put the data in mongo db collection
    try:
        '''
        uri="mongodb://localhost:27017"
        mongocli=MongoClient(uri)
        db=mongocli["API_user"]
        collection=db["users_id_pass"]
        collection.insert_one(db_data)'''
        DB.collection.insert_one(db_data)   #refer to database\config_user.py for database configurations..
        return True
    except Exception as e:
         raise HTTPException(status_code=500,detail=str(e))

def is_username_available(usernam:str):
    if(DB.collection.count_documents({"username":usernam})>0): # count_documents returns number of matches in db ..if it is greater than 0 means the username is already taken therefore we raise an exception 
     raise HTTPException(status_code=400,detail="Username already taken")