import uuid
from typing import Optional
from fastapi import Depends, Request
from fastapi_users import FastAPIUsers, BaseUserManager, models
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from models.models import User
from db import get_session
from fastapi_users.db import SQLAlchemyUserDatabase


async def get_user_db(session=Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, User)


class UserManager(BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = 'e747d31f-d08d-4349-bcfb-9eb1d2d8f6cc'
    verification_token_secret = 'e747d31f-d08d-4349-bcfb-9eb1d2d8f6cc'

    async def on_after_register(self, user, request: Optional[Request] = None):
        print(f'User {user.email} has registered')

    async def on_after_forgot_password(self, user, token, request: Optional[Request] = None):
        print(f'User: {user.email} forgot password. Reset token: {token}')

    async def on_after_request_verify(self, user, token, request: Optional[Request] = None):
        print(f'User: {user.email} sent verification request. Token: {token}')

    def parse_id(self, user_uuid: str) -> str: 
        return user_uuid

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret='e747d31f-d08d-4349-bcfb-9eb1d2d8f6cc', lifetime_seconds=3600
    )


auth_backend = AuthenticationBackend(
    name='jwt', transport=bearer_transport, get_strategy=get_jwt_strategy
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)