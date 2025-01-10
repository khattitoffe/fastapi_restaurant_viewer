from fastapi import APIRouter,Request,HTTPException
from app.services_oauth import oauth,userexists_google,create_user_google,create_access_token
from authlib.integrations.base_client import OAuthError
from authlib.oauth2.rfc6749 import OAuth2Token
from datetime import timedelta
import logging 
from app.models.google_models import google_user
from app.models.oauth_models import Token

router=APIRouter()

GOOGLE_REDIRECT_URI = "http://127.0.0.1:8000/auth/callback/google"

@router.get("/google")
async def login_google(request: Request):
    return await oauth.google.authorize_redirect(request, GOOGLE_REDIRECT_URI)

@router.get("/callback/google")
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
    
