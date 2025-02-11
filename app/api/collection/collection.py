from fastapi import APIRouter, Depends, HTTPException, status
from schemas.collections import CollectionCreate, CollectionUpdate, CollectionPublic
from ..services.collection import CollectionCrud
from utils.filters import collection_filters
from models.models import User
from api.user.auth import current_active_user
from typing import List

router = APIRouter()


@router.post('/', response_model=CollectionPublic, status_code=status.HTTP_201_CREATED)
async def create_collection(
    collection_data: CollectionCreate,
    collection_crud: CollectionCrud = Depends(CollectionCrud),
    user: User = Depends(current_active_user)):
    collection = await collection_crud.create_collection(collection_data=collection_data, user_id=user.id)
    return collection


@router.get('/', response_model=List[CollectionPublic])
async def get_collections(
    offset: int = 0, 
    limit: int = 5, 
    collection_crud: CollectionCrud = Depends(CollectionCrud),
    filters: dict = Depends(collection_filters)
):
    result = await collection_crud.get_collections(offset, limit, filters)
    return result


@router.get('/{collection_id}', response_model=CollectionPublic)
async def get_collection(collection_id: int, collection_crud: CollectionCrud = Depends(CollectionCrud)):
    collection = await collection_crud.get_collection(collection_id)
    if not collection:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Collection not found')
    return collection


@router.delete('/{collection_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection(
    collection_id: int,
    collection_crud: CollectionCrud = Depends(CollectionCrud),
    user: User = Depends(current_active_user)
):
    collection = await collection_crud.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Collection not found')
    if collection.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your collection")

    await collection_crud.delete_collection(collection_id)
    return


@router.put('/{collection_id}', response_model=CollectionPublic)
async def full_update_collection(
    collection_id: int,
    collection_data: CollectionCreate, 
    collection_crud: CollectionCrud = Depends(CollectionCrud),
    user: User = Depends(current_active_user)
):
    collection = await collection_crud.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Collection not found')
    if collection.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your collection")

    result = await collection_crud.update_collection(collection_id, collection_data)
    return result 