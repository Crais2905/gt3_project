from pydantic import BaseModel, Field
from typing import Optional


class CollectionBase(BaseModel):
    name: str = Field(max_length=100) 
    user_id: int


class CollectionCreate(BaseModel):
    pass


class CollectionUpdate(BaseModel):
    name: Optional[str]
    user_id: Optional[int]


class CollectionPublic(CollectionCreate):
    id: int