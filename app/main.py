from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .db import engine
from .models.models import Base



app = FastAPI()


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)