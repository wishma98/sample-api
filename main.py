from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId
from typing import List,Optional, Union
from app.api.category import router as category_api 


# MongoDB connection setup
MONGO_DETAILS = "mongodb+srv://useradmin:ZOq5aUL56Z02sfUk@keepbookserverlessinsta.2zvtn.mongodb.net"  # Update this to your MongoDB URI
client = AsyncIOMotorClient(MONGO_DETAILS)

# Define the database and collections
database = client.advertisement_db
advertisement_collection = database.advertisements

# FastAPI app
app = FastAPI()

# Helper function to format MongoDB ObjectId
def advertisement_helper(advertisement) -> dict:
    return {
        "advertisementId": str(advertisement["advertisementId"]),
        "userId": str(advertisement["userId"]),
        "advertisementName": advertisement["advertisementName"],
        "deviceType": advertisement["deviceType"],
        "targetingCities": advertisement["targetingCities"],
        "advertisementInterest": advertisement["advertisementInterest"],
        "category": advertisement["category"],
        "creativeType": advertisement["creativeType"],
        "creativeProperties": advertisement["creativeProperties"],
        "advertisementImage": advertisement["advertisementImage"],
        "imageRatios": advertisement["imageRatios"],
        "title": advertisement["title"],
        "description": advertisement["description"],
        "advertisementUrl": advertisement["advertisementUrl"],
        "actionButtonName": advertisement["actionButtonName"],
    }

# Pydantic models
class Advertisement(BaseModel):
    advertisementId: str = None
    userId: str = None
    advertisementName: str = None
    deviceType: Optional[str] = None
    targetingCities: Optional[List[str]] = []
    advertisementInterest: Optional[List[str]] = []
    category: Optional[List[str]] = []
    creativeType:Optional[str] = None
    creativeProperties:Optional[str] = None
    advertisementImage:Optional[str] = None
    imageRatios: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    advertisementUrl: Optional[str] = None
    actionButtonName: Optional[str] = None

# CRUD operations for advertisements (new collection)
@app.post("/create/new/advertisement", response_model=dict)
async def create_advertisement(advertisement: Advertisement):
    advertisement_data = advertisement.dict()
    advertisement_data["advertisementId"] = str(ObjectId()) 
    result = await advertisement_collection.insert_one(advertisement_data)
    new_advertisement = await advertisement_collection.find_one({"_id": result.inserted_id})
    if new_advertisement:
        return {"status": True, "message": "Advertisement create successful", "data":advertisement_helper(new_advertisement)}
    else:
        return {"status": False, "message": "Advertisement create error", "data":{}}

@app.get("/get/all/advertisements", response_model=Union[List[dict], dict])
async def get_advertisements():
    advertisements = []
    async for advertisement in advertisement_collection.find():
        advertisements.append(advertisement_helper(advertisement))  # Convert ObjectId
    if advertisements:
        return {"status": True, "message": "Advertisements found", "data": advertisements}
    else:
        return {"status": False, "message": "Advertisements not found", "data": "No documents found"}

@app.get("/get/advertisement/by/{advertisementId}", response_model=dict)
async def get_advertisement(advertisementId: str):
    advertisement = await advertisement_collection.find_one({"advertisementId": ObjectId(advertisementId)})
    if advertisement:
         return {"status": True, "message": "Advertisement found", "data": advertisement}
    else:
        return {"status": False, "message": "Advertisement not found", "data": {}}

app.include_router(category_api,prefix="/api")