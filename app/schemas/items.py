from pydantic import BaseModel, Field
from typing import Optional
from enums.items import Status
from .collections import CollectionPublic
import uuid

class ItemBase(BaseModel):
    name: str = Field(max_length=100)
    description: str = Field(max_length=500)
    year: int
    status: Status
    price: float = Field(gt=0)
    

class ItemCreate(ItemBase):
    collection_id: int


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    year: Optional[int] = None
    status: Optional[Status] = None
    price: Optional[float] = None
    image_path: Optional[str] = None
    user_id: Optional[uuid.UUID] = None
    collection_id: Optional[int] = None


class ItemPublic(ItemCreate):
    id: int
    user_id: uuid.UUID
    image_path: Optional[str]
    collection: CollectionPublic