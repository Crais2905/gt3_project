from pydantic import BaseModel, Field
from typing import Optional


class CollectionCreate(BaseModel):
    name: str = Field(max_length=100) 
    user_id: str


class CollectionUpdate(BaseModel):
    name: Optional[str]
    user_id: Optional[int]


class CollectionPublic(CollectionCreate):
    id: int