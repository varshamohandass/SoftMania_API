from fastapi import FastAPI
from pydantic import BaseModel
import json

app=FastAPI()

db = "data.json"

class Item(BaseModel):
  sno: int
  desc: str = None


@app.get("/")
def index():
  return {"result":"Hello"}

@app.get("/items/{item_id}")
async def get_item(item_id:int):
  return {"item":item_id}

@app.post("/items/")
async def store_item(item:Item):
  items = read_items_from_db()
  items.append(item.model_dump())
  store_item_to_db(items)
  return{"result":item}

def read_items_from_db():
  try:
    with open(db,'r')as file:
      items = json.load(file)
  except FileNotFoundError:
    items = []
  return items

def store_item_to_db(data):
  with open(db, 'w') as file:
    json.dump(data,file,indent = 2)
