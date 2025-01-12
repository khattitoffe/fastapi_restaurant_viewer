from pymongo import MongoClient

URL="mongodb://localhost:27017"
mongo=MongoClient(URL)
db=mongo['restaurant_db']
collection=db['restaurant_info']