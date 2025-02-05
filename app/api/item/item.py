from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select
from schemas.items import ItemCreate, ItemPublic, ItemUpdate
from ..services.item import  ItemCrud
from utils.filters import item_filters

router = APIRouter()


@router.post('/', response_model=ItemPublic, status_code=201)
async def create_item(item_data: ItemCreate, item_crud: ItemCrud = Depends(ItemCrud)):
    result = await item_crud.create_item(item_data)
    return result


@router.get('/', response_model=list[ItemPublic])
async def get_items(
    offset: int = 0,
    limit: int = 10,
    filters: dict = Depends(item_filters),
    item_crud: ItemCrud = Depends(ItemCrud)
):
    result = await item_crud.get_items(offset, limit, filters)
    return result