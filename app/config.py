from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from decouple import config

def get_engine() -> AsyncEngine:
    return create_async_engine(config('DATABASE_URL'), connect_args={"check_same_thread": False})