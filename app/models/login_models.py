from pydantic import BaseModel

class login(BaseModel):
    username_mail:str
    password:str    