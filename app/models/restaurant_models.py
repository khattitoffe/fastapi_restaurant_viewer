from pydantic import BaseModel

class review(BaseModel):
    access_token:str
    id:str
    review:str

class rating(BaseModel):
    access_token:str
    id:str
    rating:int
