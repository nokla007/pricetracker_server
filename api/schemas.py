from pydantic import BaseModel, HttpUrl, EmailStr
from typing import Optional


class User(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr


class Product(BaseModel):
    title: str
    price: float
    image: Optional[HttpUrl] = None
    url: HttpUrl


class ProductResponse(Product):
    id: int


class ProductURL(BaseModel):
    url: HttpUrl
