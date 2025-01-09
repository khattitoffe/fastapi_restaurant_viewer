from pymongo import MongoClient


URL="mongodb://localhost:27017"
mongo=MongoClient(URL)
db=mongo["API_user"]
collection=db["users_id_pass"]

