from fastapi import APIRouter, Depends, HTTPException, status
from schemas.collections import CollectionCreate, CollectionUpdate, CollectionPublic
from ..services.collection import CollectionCrud

router = APIRouter()


@router.post('/', response_model=CollectionPublic, status_code=status.HTTP_201_CREATED)
async def create_collection(collection_data: CollectionCreate, collection_crud: CollectionCrud = Depends(CollectionCrud)):
    collection = await collection_crud.create_collection(collection_data=collection_data)
    return collection