from pydantic import BaseModel, Field
from typing import Optional
import uuid

class CollectionBase(BaseModel):
    title: str = Field(max_length=100) 
    user_id: uuid.UUID


class CollectionCreate(CollectionBase):
    pass


class CollectionUpdate(BaseModel):
    title: Optional[str]
    user_id: Optional[uuid.UUID]


class CollectionPublic(CollectionCreate):
    id: int