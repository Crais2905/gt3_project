from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select
from schemas.items import ItemCreate, ItemPublic, ItemUpdate
from ..services.item import  ItemCrud
from utils.filters import item_filters

router = APIRouter()


@router.post('/', response_model=ItemPublic, status_code=status.HTTP_201_CREATED)
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


@router.get('/{item_id}', response_model=ItemPublic)
async def get_itenm(item_id: int, item_crud: ItemCrud = Depends(ItemCrud)):
    item = await item_crud.get_item(item_id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return item


@router.delete('/{item_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, item_crud: ItemCrud = Depends(ItemCrud)):
    item = await item_crud.get_item(item_id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    await item_crud.delete_item(item_id)
    return