import uuid
from sqlalchemy import String, Integer, ForeignKey, Text, Numeric, Enum, UUID
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship
from fastapi_users.db import SQLAlchemyBaseUserTable
from ..enums.items import Status


Base = declarative_base()


class Collection(Base):
    __tablename__ = 'collections'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('users.id'), nullable=False)
    user: Mapped['User'] = relationship("User", back_populates='collections', lazy='selectin')
    items: Mapped[list["Item"]] = relationship("Item", back_populates="collection", cascade="all, delete-orphan")

class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    year: Mapped[int] = mapped_column(Integer, nullable=True)
    status: Mapped['Status'] = mapped_column(Enum(Status), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    image_path: Mapped[str] = mapped_column(String, nullable=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('users.id'), nullable=False)
    user: Mapped['User'] = relationship("User", back_populates='items', lazy='selectin')
    collection_id: Mapped[int] = mapped_column(Integer, ForeignKey('collections.id'), nullable=False)
    collection: Mapped[Collection] = relationship("Collection", back_populates="items", lazy="selectin")


class User(SQLAlchemyBaseUserTable, Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    items: Mapped[list["Item"]] = relationship("Item", back_populates="user", cascade="all, delete-orphan")
    collections: Mapped[list[Collection]] = relationship("Collection", back_populates='user', cascade="all, delete-orphan")