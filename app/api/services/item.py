from fastapi import Depends
from sqlalchemy.future import select
from sqlalchemy import update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from ...models.models import Collection, Item
from schemas.items import ItemCreate, ItemUpdate, ItemPublic
from db.session import get_session



class ItemCrud:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get_item(self, item_id: int):
        stmt = select(Item).where(Item.id == item_id)
        return await self.session.scalar(stmt)
    

    async def create_item(self, item_data: ItemCreate):
        stmt = insert(Item).values(item_data.model_dump()).returning(Item)
        result = await self.session.execute(stmt)
        await self.session.commit()
        created_book = result.scalar()
        return created_book
    

    async def update_item(self, item_id: int, item_data: ItemUpdate):
        values = item_data.model_dump(exclude_unset=True)
        stmt = update(Item).where(Item.id == item_id).values(values).returning(Item)
        result = await self.session.execute(stmt)
        await self.session.commit()

        updated_item = result.scalar()
        return updated_item
    

    async def delete_item(self, item_id: int):
        stmt = delete(Item).where(Item.id == item_id).returning(Item)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar()