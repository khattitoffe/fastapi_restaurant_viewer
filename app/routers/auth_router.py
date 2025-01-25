from fastapi import APIRouter,Request,HTTPException
from app.services_oauth import userexists_sso,create_user_sso,create_access_token
#from app.sso import oauth
#from authlib.integrations.base_client import OAuthError
#from authlib.oauth2.rfc6749 import OAuth2Token
from datetime import timedelta
import logging 
#from app.models.google_models import google_user
from app.models.sso_model import sso
from app.models.oauth_models import Token
from app.sso import facebook_sso,git_sso,google_sso

router=APIRouter()

GOOGLE_REDIRECT_URI = "http://127.0.0.1:8000/auth/callback/google"
"""
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
    """

@router.get("/google")
async def auth_init():
    async with google_sso:
        return await google_sso.get_login_redirect(params={"prompt": "consent", "access_type": "offline"})


@router.get("/callback/google")
async def auth_callback(request: Request):
    try:
        async with google_sso:
            user_info = await google_sso.verify_and_process(request)
            print("good till here")
            if(userexists_sso(user_info.email)):
                user_data=sso(
                              email=user_info.email,
                              username=user_info.display_name
                              )
                token=create_access_token(user_data,timedelta(days=7))
                return Token(access_token=token)
            else:
                user_data=sso(
                              email=user_info.email,
                              username=user_info.display_name
                              )
                create_user_sso(user_data)
            
                token=create_access_token(user_data,timedelta(days=7))
                return Token(access_token=token)
    except Exception as e:
         print("error is here")
         raise HTTPException(status_code=401,detail=str(e))


@router.get("/facebook")
async def login_facebook():
    async with facebook_sso:
        return await facebook_sso.get_login_redirect(params={"prompt": "consent", "access_type": "offline"})

@router.get("/callback/facebook")
async def auth_callback(request: Request):
    try: ## isme ahbi access token wala code dalna hai 
        async with facebook_sso:
            user_info = await facebook_sso.verify_and_process(request)
            if(userexists_sso(user_info.email)):
                user_data=sso(
                              email=user_info.email,
                              username=user_info.display_name
                              )
                token=create_access_token(user_data,timedelta(days=7))
                return Token(access_token=token)
            else:
                user_data=sso(
                              email=user_info.email,
                              username=user_info.display_name
                              )
                create_user_sso(user_data)
            
                token=create_access_token(user_data,timedelta(days=7))
                return Token(access_token=token)
    except Exception as e:
        raise HTTPException(status_code=401,detail=str(e))
    

@router.get("/github")
async def auth_init():
    async with git_sso:
        return await git_sso.get_login_redirect()
    
@router.get("/callback/github")
async def auth_callback(request: Request):
    try:
        async with git_sso:
            user_info = await git_sso.verify_and_process(request)
            if(userexists_sso(user_info.email)):
                user_data=sso(
                              email=user_info.email,
                              username=user_info.display_name
                              )
                token=create_access_token(user_data,timedelta(days=7))
                return Token(access_token=token)
            else:
                user_data=sso(
                              email=user_info.email,
                              username=user_info.display_name
                              )
                create_user_sso(user_data)
            
                token=create_access_token(user_data,timedelta(days=7))
                return Token(access_token=token)
    except Exception as e:
        raise HTTPException(status_code=401,detail=str(e))