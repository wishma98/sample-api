from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# Initialize the FastAPI app
app = FastAPI()

# Define the data model for an Item using Pydantic
class Item(BaseModel):
    id: int
    name: str
    description: str = None
    price: float
    available: bool = True

# In-memory "database" for items
items = []

# Create an item
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    items.append(item)
    return item

# Get all items
@app.get("/items/", response_model=List[Item])
async def get_items():
    return items

# Get a specific item by ID
@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# Update an item by ID
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, updated_item: Item):
    for idx, item in enumerate(items):
        if item.id == item_id:
            items[idx] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

# Delete an item by ID
@app.delete("/items/{item_id}", response_model=Item)
async def delete_item(item_id: int):
    for idx, item in enumerate(items):
        if item.id == item_id:
            deleted_item = items.pop(idx)
            return deleted_item
    raise HTTPException(status_code=404, detail="Item not found")
