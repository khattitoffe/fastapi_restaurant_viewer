from pydantic import BaseModel

class sso(BaseModel):
    email:str
    username:str