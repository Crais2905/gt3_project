from fastapi import APIRouter, Depends
from .user import fastapi_users, current_active_user, auth_backend
from schemas.user import UserCreate, UserRead, UserUpdate
from models.models import User


router = APIRouter()


router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth']
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth']
)