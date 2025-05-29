from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional



app = FastAPI(
    title = "FastAPI Basics",
    description="A project on FastAPI",
    version="1.0.0"
)



# Data model
class Item(BaseModel):
    id: int
    name:str
    description: Optional[str] = None 
    price: float = Field(..., ge=0) # To prevent negative values

# In-memory storage 
db = []


@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI Project"}


# get item by id
@app.get("/items/{item_id}")
def get_item_by_id(item_id: int):
    for item in db:
        if item[db] == item_id:
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")    

    
    

@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    for existing_item in db:
        if existing_item["id"] == item.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item with this id already exist")
    db.append(item.model_dump())
    return {"message": "Item added successfully", "item": item}


    
@app.put("/items{item_id}")
def update_item(item_id: int, item: Item):
    if item.id != item_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item id body does not match the url")
    for i, existing_item in enumerate(db):
        if existing_item["id"] == item_id:
            db[i] = item.model_dump()
            return {"message": "Item updated", "item": item}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

@app.delete("/items{item_id}")
def delete_item(item_id: int):
    for i, item in enumerate(db):
        if item["id"] == item_id:
            del db[i]
            return {"message": "Item deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


if __name__ == "__name__":
    import uvicorn
    uvicorn.run(["gunicorn","main:app","--workers","4","--worker-class","uvicorn.workers.UvicornWorker","--bind","0.0.0.0:8000","--reload"])
