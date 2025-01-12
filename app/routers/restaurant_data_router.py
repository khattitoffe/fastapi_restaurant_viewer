import app.database.config_restaurant_data as DB
from fastapi import APIRouter,HTTPException,Depends
from app.models.oauth_models import Token
from app.services_oauth import current_user_data
from app.models.restaurant_models import review,rating
from bson import ObjectId

router=APIRouter()

#adding limiter to endpoints form same IP


@router.get("/random")

def getRandomData(user_data:dict=Depends(current_user_data)):
    try:
        data = list(DB.collection.aggregate([{"$sample": {"size": 20}}]))
        data = [convert_objectid(doc) for doc in data]
        return data
    except Exception as e:
       raise HTTPException(status_code=500,detail=str(e))
    
def convert_objectid(doc):
    if "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["_id"] = str(doc["_id"])
    return doc
    
@router.post("/add-Review")
def addReview(review_data:review):
    check(review_data.access_token)#verifying token by check function
    user_data=current_user_data(review_data.access_token)
    try:
        DB.collection.update_one({"_id":ObjectId(review_data.id)},
                                 {"$push":{"Review":
                                           [{"username":user_data["username"],
                                             "review":review_data.review}
                                            ]}})
        return{"Message":"Review Uploaded"}
    except Exception as e:
        raise HTTPException(status_code=501,detail=str(e))
    
def check(user_data:dict=Depends(current_user_data)):
    return user_data

@router.post("/add-Rating")
def addReview(rating_data:rating):
    user_data=check(rating_data.access_token)#verifying token by check function
    try:
        rating_db=DB.collection.find_one({"_id":ObjectId(rating_data.id)},{"_id":0,"rating":1})
        if(rating_db["rating"]==None):#if the rating is null then just update the rating
            DB.collection.update_one({"_id":ObjectId(rating_data.id)},{"$set":{"rating":rating_data.rating}})
            return{"Message":"Rating Updated"}
        else:#if the rating is not null then we take the rating in db and add it with rating given be user and then divide by 2 and then update it
            new_rating=(rating_db["rating"]+rating_data.rating)/2
            DB.collection.update_one({"_id":ObjectId(rating_data.id)},{"$set":{"rating":new_rating}})
            return{"Message":"Rating Updated"}
    except Exception as e:
        raise HTTPException(status_code=501,detail=str(e))