from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import Optional,List,Union
from bson import ObjectId
from app.api.category import router as category_api 

MONGO_DETAILS = "mongodb+srv://useradmin:ZOq5aUL56Z02sfUk@keepbookserverlessinsta.2zvtn.mongodb.net/marketHub_db?retryWrites=true&w=majority"
client = AsyncIOMotorClient(MONGO_DETAILS)

router = FastAPI()

database=client.marketHub_db
category_collection=database.categories

class Category(BaseModel):
    categoryId:str = None
    categoryName:str =None
    iconName:str =None
    categoryTag:Optional[List[str]] =None #not required, array ,string

def category_data(category) -> dict:
    return{
        "categoryId": str(category["categoryId"]),
        "categoryName": str(category["categoryName"]),
        "iconName":str (category["iconName"]),
        "categoryTag":category["categoryTag"],
    }


@router.post("/create/new/category", response_model=dict)
async def create_category(category:Category):
    category_data = category.dict()
    category_data["categoryId"] = str(ObjectId())
    result = await category_collection.insert_one(category_data)
    new_category=await category_collection.findOne({"_id":result.inserted_id})
    if new_category:
        {"status":True, "message": "Category Create Successfully", "data":category_data(new_category)}
    else:
        {"status":False, "message": "Category Create Error", "data":{}}


@router.get("/get/all/category/item", response_model=Union[List[dict],dict])
async def get_category():
    categories =[]
    async for category in category_collection.find():
     categories.append(category_data(category))
     if categories:
         return {"status":True, "message": "Category found", "data":categories}
     else:
         return {"status":False, "message":"Category not Found", "data":"Not Document Found"}
     

