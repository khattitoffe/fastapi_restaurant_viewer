from email_validator import validate_email, EmailNotValidError
from fastapi import HTTPException
from app.models.login_models import login
import app.database.config_user as DB
from passlib.context import CryptContext 


pass_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def user_login(data:login):
  
  is_email_valid=emailverification(data.username_mail)#checking if email is in db

  if(is_email_valid):  # true if email is in db
     success=verifypassword_email(data.username_mail,data.password) # matching the entered password with the password in db 
     if success:
        return 
     else :
        raise HTTPException(status_code=400,detail="Invalid Password")
     
  else:  #email not in db.. 
    is_username_valid=usernameverification(data.username_mail) #now we check if username is in db
    if(is_username_valid): #true if username is in database 
       success=verifypassword_username(data.username_mail,data.password) # matching the entered password with the password in db 
       if success:
        return
       else :
        raise HTTPException(status_code=400,detail="Invalid Password")
    else:
       raise HTTPException(status_code=400,detail="Invalid Username of Email")




def emailverification(email:str):

   if DB.collection.count_documents({"email":email})==0:#count_document returns the number of matches in db if 0 that means no user exitst
      return False
   else :
      return True

def usernameverification(username:str):
   if DB.collection.count_documents({"username":username})==0:
      return False
   else :
      return True


def verifypassword_username(username:str ,password:str):
   user=DB.collection.find_one({"username":username})

   hashed_password=user["hashed_password"]
   return pass_context.verify(password,hashed_password)


def verifypassword_email(email:str ,password:str):
   user=DB.collection.find_one({"email":email})

   hashed_password=user["hashed_password"]
   return pass_context.verify(password,hashed_password)