from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from config import get_engine


engine = get_engine()
SessionLocal = async_sessionmaker(
    engine,
    autoflush=False,
    autocommit=False,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session():
    async with SessionLocal() as session:
        yield session