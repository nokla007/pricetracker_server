from typing import List
from fastapi import FastAPI
from pydantic import HttpUrl

from db import db, models
from . import schemas
import services.ecomService as pf


# models.metadata.create_all(bind=db.engine)

app = FastAPI()


@app.get("/", tags=["root"])
async def root():
    return {"message": "Hello World Yo"}


@app.post("/users/create/", tags=["Create a user"], response_model=schemas.UserResponse)
async def creatUser(user: schemas.User):
    print(user.dict())
    return user


@app.post("/users/login/", tags=["User login"], response_model=schemas.UserResponse)
async def creatUser(user: schemas.User):
    print(user.dict())
    return user


@app.post("/products/fetch/", tags=["Fetch a product by url"])
async def getproduct2(productURL: schemas.ProductURL):
    url = str(productURL.url)
    productDetails: schemas.Product = pf.getProduct(url)
    return productDetails


@app.post("products/search/{query}", tags=["Search for a product"])
async def search(query: str):
    products: List[schemas.Product] = pf.searchProduct(query)
    return products


@app.get("/favorites/{user_id}", tags=["Get a product"])
async def getproduct(user_id: str):
    return {"user_id": user_id}


@app.get("/products/{product_id}/", tags=["Get a product"])
async def getproduct(product_id: str):
    return {"product_id": product_id}
