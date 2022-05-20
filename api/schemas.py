from pydantic import BaseModel, HttpUrl, EmailStr
from typing import Optional


class User(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class Product(BaseModel):
    title: str
    price: float
    image: Optional[HttpUrl] = None
    url: HttpUrl


class ProductDB(Product):
    id: int
    class Config:
        orm_mode = True


class ProductURL(BaseModel):
    url: HttpUrl

class Favorite(BaseModel):
    user_id: int
    product_id: int