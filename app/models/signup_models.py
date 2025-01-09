from pydantic import BaseModel, Field

class signup(BaseModel):
    username:str
    password:str
    email:str

class db_signup(BaseModel):
    username:str
    hashed_password:str
    email:str
