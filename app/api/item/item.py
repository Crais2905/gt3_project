import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from sqlalchemy.future import select
from schemas.items import ItemCreate, ItemPublic, ItemUpdate
from ..services.item import  ItemCrud
from ..services.collection import CollectionCrud
from utils.filters import item_filters
from ..user.user import current_active_user
from models.models import Item, User
router = APIRouter()


@router.post('/', response_model=ItemPublic, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_data: ItemCreate,
    item_crud: ItemCrud = Depends(ItemCrud), 
    user: User = Depends(current_active_user),
    collection_crud: CollectionCrud = Depends(CollectionCrud)
):
    collection_id = item_data.model_dump()['collection_id']
    collection = await collection_crud.get_collection(collection_id)
    if collection.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your collection")

    result = await item_crud.create_item(item_data, user.id)
    return result


@router.get('/', response_model=list[ItemPublic])
async def get_items(
    offset: int = 0,
    limit: int = 10,
    filters: dict = Depends(item_filters),
    item_crud: ItemCrud = Depends(ItemCrud)
):
    print(filters)
    result = await item_crud.get_items(offset, limit, filters)
    return result

@router.get('/my', response_model=list[ItemPublic])
async def get_items(
    offset: int = 0,
    limit: int = 10,
    filters: dict = Depends(item_filters),
    item_crud: ItemCrud = Depends(ItemCrud),
    user: User = Depends(current_active_user)
):  
    filters.append(Item.user_id == user.id)
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
async def delete_item(item_id: int, item_crud: ItemCrud = Depends(ItemCrud), user: User = Depends(current_active_user)):
    item = await item_crud.get_item(item_id=item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    if item.user_id != user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your item")

    await item_crud.delete_item(item_id)
    return


@router.put('/{item_id}', response_model=ItemPublic)
async def full_update_item(
    item_id: int,
    item_data: ItemCreate, 
    item_crud: ItemCrud = Depends(ItemCrud),
    user: User = Depends(current_active_user)
):
    item = await item_crud.get_item(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    if item.user_id != user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your item")

    result = await item_crud.update_item(item_id, item_data)
    return result


@router.patch('/{item_id}', response_model=ItemPublic)
async def part_update_item(
    item_id: int,
    item_data: ItemUpdate,
    item_crud: ItemCrud = Depends(ItemCrud),
    user: User = Depends(current_active_user)
):
    item = await item_crud.get_item(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    if item.user_id != user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your item")

    result = await item_crud.update_item(item_id, item_data)
    return result 


@router.patch('/image/{item_id}', response_model=ItemPublic)
async def add_item_image(
    item_id: int,
    image: UploadFile, 
    item_crud: ItemCrud = Depends(ItemCrud),
    user: User = Depends(current_active_user)
):
    item = await item_crud.get_item(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    if item.user_id != user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your item")
    
    file_extension = image.filename.split('.')[-1]
    if file_extension not in ['jpg', 'png', 'jpeg']:
        raise HTTPException(status_code=400, detail="Unsupported extension")
    
    file_path = os.path.join('static', f'{uuid.uuid4()}.{file_extension}')
    with open(file_path, 'wb') as file:
        file.write(image.file.read())

    item.image_path = file_path
    item_crud.session.add(item)
    await item_crud.session.commit()
    await item_crud.session.refresh(item)
    return item