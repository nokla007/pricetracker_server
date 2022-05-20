from typing import List
from fastapi import Depends, FastAPI, Response, status, HTTPException
from pydantic import HttpUrl
from sqlalchemy.orm import Session
from db import db, models, crud
from . import schemas
import services.ecomService as pf


models.Base.metadata.create_all(bind=db.engine)

app = FastAPI()


@app.get("/", tags=["root"])
async def root():
    return {"message": "Hello World Yo"}


@app.post("/users/create/", status_code=status.HTTP_201_CREATED, tags=["Create a user"], response_model=schemas.UserResponse)
def signup(user: schemas.User, response:Response, db: Session = Depends(db.get_db)):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    # print(user.dict())
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_302_FOUND, detail="User Exists")
    try:
        new_user = crud.create_user(db=db, user=user)
        # return schemas.UserResponse(id=new_user.id, email=new_user.email)
        return new_user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=Exception)


@app.post("/users/login/", tags=["User login"], response_model=schemas.UserResponse)
def login(user: schemas.User, response:Response, db: Session = Depends(db.get_db)):
    # print(user.dict())
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")
    if not db_user.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect Password")
    # return schemas.UserResponse(id=db_user.id, email=db_user.email)
    return db_user


@app.post("/search/{query}", tags=["Search for a product"], response_model=List[schemas.Product])
def search(query: str, response: Response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    products: List[schemas.Product] = pf.searchProduct(query)
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='No products found')
    return products


@app.post("/products/fetch/", tags=["Fetch a product by url"], response_model=schemas.ProductDB)
def fetchproduct(productURL: schemas.ProductURL, response:Response, db: Session = Depends(db.get_db)):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    url = str(productURL.url)
    productDetails: schemas.Product = pf.getProduct(url)
    if not productDetails:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    new_product = crud.get_product_by_url(db, url)
    if not new_product:
        new_product = crud.add_product(db=db, product=productDetails)
    return new_product


@app.post("/products/add/", tags=["Add a product"])
def addproduct(product: schemas.Product,response:Response, db: Session = Depends(db.get_db)):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    db_product = crud.get_product_by_url(db, url=product.url)
    if db_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Product Exists")
    try:
        new_product = crud.add_product(db=db, product=product)
        return new_product
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=Exception)


@app.get("/products/{product_id}/", tags=["Get a product"], response_model=schemas.ProductDB)
def getproduct(product_id: int, response: Response, db: Session = Depends(db.get_db)):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    db_product = crud.get_product(db, product_id=product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return db_product


@app.put("/products/{product_id}/", tags=["Update a product"], response_model=schemas.ProductDB)
def updateproduct(product_id: int, response: Response, db: Session = Depends(db.get_db)):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    db_product = crud.get_product(db, product_id=product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    newproduct = pf.getProduct(db_product.url)
    if not newproduct:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Could not update")
    try:
        updated_product = crud.update_product(
            db=db, product_id=product_id, product=newproduct)
        return updated_product
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.post("/favorites/add/", tags=["Add a favorite product"], response_model=schemas.ProductDB)
def addfavorite(favorite: schemas.Favorite, response: Response, db: Session = Depends(db.get_db)):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    try:
        new_favorite = crud.add_favorite(
            db=db, user_id=favorite.user_id, product_id=favorite.product_id)
        return new_favorite
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST)


@app.post("/favorites/remove/", tags=["Remove a favorite product"], response_model=schemas.ProductDB)
def removefavorite(favorite: schemas.Favorite, response: Response, db: Session = Depends(db.get_db)):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    try:
        removed_favorite = crud.remove_favorite(
            db=db, user_id=favorite.user_id, product_id=favorite.product_id)
        return removed_favorite
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST)


@app.get("/favorites/{user_id}", tags=["Get favorite products"])
def getproducts(user_id: int, response: Response, db: Session = Depends(db.get_db)):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    try:
        favorites = crud.get_favorites(db=db, user_id=user_id)
        return favorites
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST)
