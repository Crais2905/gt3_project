from pydantic import BaseModel, Field
from typing import Optional
import uuid

class CollectionBase(BaseModel):
    title: str = Field(max_length=100) 


class CollectionCreate(CollectionBase):
    pass


class CollectionUpdate(BaseModel):
    title: Optional[str]


class CollectionPublic(CollectionBase):
    id: int
    user_id: uuid.UUID