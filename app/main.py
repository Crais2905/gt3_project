from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from db import engine
from models.models import Base
from api.collection.collection import router as collection_router 
from api.user.auth import router as auth_router
from api.item.item import router as item_router


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(collection_router, prefix="/collections", tags=["collections"])
app.include_router(auth_router, tags=["auth"])
app.include_router(item_router, prefix="/items", tags=['items'])