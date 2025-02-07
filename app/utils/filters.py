from fastapi import Query
from typing import Optional
from models.models import Item


def item_filters(
    name: Optional[str] = Query(None, description='Filter by name'),
    collection_id: Optional[int] = Query(None, description='Filter by collection id'),
    user_id: Optional[str] = Query(None, description='Filter by user id'),
    year: Optional[int] = Query(None, description='Filter by year'),
    min_price: Optional[int] = Query(None, description='Filter by min price'),
    max_price: Optional[int] = Query(None, description='Filter by max price')
):
    filters = []
    if name:
        filters.append(Item.name.ilike(f'%{name}%'))
    if collection_id:
        filters.append(Item.collection_id == collection_id)
    if user_id:
        filters.append(Item.user_id == user_id)
    if year:
        filters.append(Item.year == year)
    if min_price:
        filters.append(Item.price > min_price)
    if max_price:
        filters.append(Item.price < max_price)
    return filters