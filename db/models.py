from tokenize import Floatnumber
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .db import Base


favorites = Table(
    "favorites",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    products = relationship(
        "Product", secondary=favorites, back_populates="users")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    price = Column(Float)
    image = Column(String, nullable=True)
    url = Column(String, unique=True)

    users = relationship("User", secondary=favorites,
                         back_populates="products")
