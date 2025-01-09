from pydantic import BaseModel 

class google_user(BaseModel):
    email:str
    username:str
