from pydantic import BaseModel, Field
from typing import Optional
import uuid

class CollectionBase(BaseModel):
    name: str = Field(max_length=100) 
    user_id: uuid.UUID


class CollectionCreate(BaseModel):
    pass


class CollectionUpdate(BaseModel):
    name: Optional[str]
    user_id: Optional[uuid.UUID]


class CollectionPublic(CollectionCreate):
    id: int