from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json


app = FastAPI()
DATBASE_FILE = 'data.json'

class Item(BaseModel):
    sno : int =None
    desc : str =None
    to_be_deleted : list =None

class UpdateItem(BaseModel):
    sno: int
    desc: str = None

class ItemList(BaseModel):
    data: List[Item]

# class MultipleItem(BaseModel):
#    sno_lst: List[Item]

@app.post("/dummypath")
async def get_body(item_list:ItemList):
    items = read_items_from_db()
    for item in item_list:
        items.append(json.dumps(item))
        store_item_to_db(items)
    return item_list
     
    

@app.get("/")
async def index():
    items = read_items_from_db()
    return items

@app.get("/items/{item_id}")
async def get_item(item_id:int):
    items = read_items_from_db()
    # if item_id <0 or item_id >= len(items):
    #     raise HTTPException(status_code = 404, detail ="item not found")
    # return {"item":items[item_id]}
    for item in items:
      if item['sno'] == item_id:
        return item
    else:
      return f"item{item_id} not found"
  

@app.post("/items")
async def store_item(item:Item):
    items = read_items_from_db()
    items.append(item.model_dump())
    store_item_to_db(items)
    return {"result": item}

@app.post("/delete-multiple/")
async def delete_multiple_items_from_db(item:Item):
  #  delete_list= item['to_be_deleted']
   return item
  #  items = read_items_from_db()
  #  for item in items:
  #     for i in delete_list:
  #        if item['sno']==i:
  #           items.remove(item)
  #           store_item_to_db(items)
   

@app.delete("/items/{item_id}")
async def delete_item_from_db(item_id:int):
  items = read_items_from_db()
  for item in items:
    if item['sno'] == item_id:
      items.remove(item)
    store_item_to_db(items)
    return f'{item} has been deleted'
  else:
    return f'item{item_id} not found'
  
@app.delete("/delete-items")
async def delete_all_items_from_db():
  items = read_items_from_db()
  items.clear()
  store_item_to_db(items)
  return items
  
@app.put("/items/{item_id}")
async def change_item_in_db(item:UpdateItem, item_id:int):
  items = read_items_from_db()
  for db_item in items:
    if db_item['sno'] == item_id:
      db_item['desc'] = item.desc
  store_item_to_db(items)

# @app.post("multi_list/")
# async def todo_list(lst:MultipleItem):
#    return lst

   

def read_items_from_db():
    try:
        with open(DATBASE_FILE,'r') as file:
            items=json.load(file)
    except FileNotFoundError:
        items =[]
    return items

def store_item_to_db(data):
    with open(DATBASE_FILE,'w') as file:
        json.dump(data,file,indent=2)