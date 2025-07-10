from fastapi import APIRouter
from typing import List
from pydantic import BaseModel 

class Item(BaseModel):
    id: int
    name: str

items_db = [
    {"id":1, "name":"Manzana"},
    {"id":2, "name":"Banana"},
    {"id":3, "name":"Cereza"}
]

item_router = APIRouter()

@item_router.get("/items", response_model=List[Item])
async def get_items():
    return items_db