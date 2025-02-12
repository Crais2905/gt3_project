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
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix='/auth',
    tags=['auth']
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix='/auth',
    tags=['auth']
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/auth',
    tags=['auth']
)


@router.get('/authenticated-only')
async def authenticated_only(current_user: User = Depends(current_active_user)):
    return {'message': f'Hello, {current_user.email}'}
