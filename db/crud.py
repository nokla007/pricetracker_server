import sqlalchemy.exc as sql_exc
from sqlalchemy.orm import Session
from sqlalchemy import update

from services.gadstyle import getProduct

from . import models
import api.schemas as schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.User):
    try:
        db_user = models.User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except sql_exc.IntegrityError:
        raise Exception("User Exists")


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_product_by_url(db: Session, url: str):
    return db.query(models.Product).filter(models.Product.url == url).first()


def add_product(db: Session, product: schemas.Product):
    try:
        db_product = models.Product(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except sql_exc.IntegrityError:
        raise Exception("Product Exists")


def remove_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product


def update_product(db: Session, product_id: int, product: dict):
    try:
        db.query(models.Product).filter(
            models.Product.id == product_id).update(product)
        db.commit()
        return db.query(models.Product).filter(models.Product.id == product_id).first()
    except:
        raise Exception("Error updating database")


def add_favorite(db: Session, user_id: int, product_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        raise Exception("User does not exist")
    db_product = get_product(db, product_id)
    if not db_product:
        raise Exception("Product does not exist")
    if db_user and db_product:
        try:
            db_user.products.append(db_product)
            db.commit()
        except ValueError:
            raise Exception("Product already in favorites")
    return db_product


def get_favorites(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        return db_user.products
    else:
        raise Exception("User does not exist")


def remove_favorite(db: Session, user_id: int, product_id: int):
    db_user = get_user(db, user_id)
    db_product = get_product(db, product_id)
    if db_user and db_product:
        try:
            db_user.products.remove(db_product)
            db.commit()
        except ValueError:
            raise Exception("Product not in favorites")
    else:
        raise Exception("User or Product does not exist")
    return db_product

# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()

# def add_product(db: Session, product: schemas.Product):
#     db_product = models.Product(**product.dict())
#     db.add(db_product)
#     db.commit()
#     db.refresh(db_product)
#     return db_product

# def remove_product(db: Session, product_id: int, user_id: int):
#     db_product = db.query(models.favorites).filter(models.favorites.user_id == user_id).filter(
#         models.favorites.product_id == product_id).first()
#     db.delete(db_product)
#     db.commit()
#     return db_product

# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
