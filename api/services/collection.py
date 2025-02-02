from fastapi import Depends
from sqlalchemy.future import select
from sqlalchemy import update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from ...models.models import Collection, Item
from schemas.collections import CollectionCreate, CollectionUpdate, CollectionPublic
from db.session import get_session


class CollectionCrud:
    def __init__(
            self,
            session: AsyncSession = Depends(get_session)
    ):
        self.session = session

    async def get_collections(self, offset: int = 0, limit: int = 3) -> list[CollectionPublic]:
        stmt = select(Collection).offset(offset).limit(limit)
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_collection(self, collection_id: int):
        stmt = select(Collection).where(Collection.id == collection_id)
        result = await self.session.scalar(stmt)
        return result

    async def create_collection(self, collection_data: CollectionCreate):
        stmt = insert(Collection).values(collection_data.model_dump()).returning(Collection)
        result = await self.session.execute(stmt)
        await self.session.commit()
        result_orm = result.scalar()
        return result_orm

    async def update_collection(self, collection_id: int, updated_collection: CollectionUpdate):
        stmt = (
            update(Collection)
            .where(Collection.id == collection_id)
            .values(updated_collection.model_dump())
            .returning(Collection)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        result_orm = result.scalar()
        return result_orm

    async def delete_collection(self, collection_id: int):
        stmt = delete(Collection).where(Collection.id == collection_id).returning(Collection)
        stmt_items = delete(Item).where(Item.collection_id == collection_id).returning(Item)

        async with self.session as conn:
            try:
                stmt_result = await conn.execute(stmt)
                stmt_items_result = await conn.execute(stmt_items)
                await conn.commit()
            except Exception as error:
                await conn.rollback()
                raise error

        result = [stmt_result.scalar(), stmt_items_result.scalars().all()]
        return result