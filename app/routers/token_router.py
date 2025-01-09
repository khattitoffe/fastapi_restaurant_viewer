from fastapi import APIRouter 
from app.models.oauth_models import Token
from app.services_oauth import decode_access_token,is_token_expired,current_user_data,refresh_access_token
from datetime import timedelta
from app.models.google_models import google_user

router=APIRouter()

@router.post("/is-expired")
async def is_expired(token:Token):
    
    if(is_token_expired(token.access_token)):
        return {"Status":"Token Expired"}
    return {"Status":"Token Valid"}

@router.post("/refresh")
async def refresh(token:Token):

    if(is_token_expired(token.access_token)):
        return {"Message":"Session Expired. Login again"}
    
    user_data=decode_access_token(token.access_token)
    data=google_user(email=user_data["email"],username=user_data["username"])

    return Token(access_token=refresh_access_token(data,timedelta(days=7)))
    

@router.post("/get-user-data")
async def getUserData(token:Token):
    return current_user_data(token.access_token)