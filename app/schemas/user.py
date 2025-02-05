import uuid
from fastapi_users import schemas
from typing import Optional

class UserRead(schemas.BaseUser[uuid.UUID]):
    username: str
    first_name: str
    last_name: str


class UserCreate(schemas.BaseUserCreate):
    username: str
    first_name: str
    last_name: str


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]