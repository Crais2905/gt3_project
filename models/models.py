import uuid
from sqlalchemy import String, Integer, ForeignKey, Text, Numeric
from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from fastapi_users.db import SQLAlchemyBaseUserTable
from ..enums.items import Status
from enum import Enum

Base = declarative_base()


class Collection(Base):
    __tablename__ = 'collections'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)


class Item(Base):
    __tablename__ = 'items'

    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    year: Mapped[int] = mapped_column(Integer, nullable=True)
    status: Mapped['Status'] = mapped_column(Enum(Status), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    image_path: Mapped[str] = mapped_column(String, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    collection_id: Mapped[int] = mapped_column(Integer, ForeignKey('collection.id'), nullable=False)


class User(SQLAlchemyBaseUserTable, Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
