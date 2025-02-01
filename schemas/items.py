from pydantic import BaseModel, Field
from typing import Optional
from enums.items import Status
from .collections import CollectionPublic
#image_path
#

class ItemBase(BaseModel):
    name: str = Field(max_length=100)
    description: str = Field(max_length=5)
    year: int
    status: Status
    price: float
    user_id: int
    collection_id: int


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    year: Optional[int]
    status: Optional[Status]
    price: Optional[float]
    image_path: Optional[str]
    user_id: Optional[int]
    collection_id: Optional[int]


class ItemPublic(ItemCreate):
    id: int
    image_path: str