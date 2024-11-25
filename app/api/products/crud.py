from app.models import db, Product, Category
from sqlalchemy.exc import IntegrityError
from flask import jsonify, Response
from app.api.products.schemas import (
    CreateProductSchema,
    ProductSchemaRead,
    ProductListRead,
    UpdateProductSchema,
)
from app.core import logger
from app.api.categories.crud import get_category_by_is


def create_product(data: CreateProductSchema):
    try:
        category = get_category_by_is(data.category_id)
        if isinstance(category, tuple):
            return category

        product = Product(
            name=data.name,
            description=data.description,
            price=data.price,
            quantity=data.quantity,
            category_id=data.category_id,
        )
        db.session.add(product)
        db.session.commit()
        return product
    except IntegrityError as err:
        db.session.rollback()
        logger.error(f"Database error: {str(err)}")
        return jsonify({"error": "This product already exists"}), 400
    except Exception as err:
        db.session.rollback()
        logger.error(err)


def get_products() -> list[Product]:
    try:
        products = Product.query.order_by(Product.id).all()
        return products
    except Exception as err:
        logger.error(err)


def get_product_by_id(product_id: int) -> Product | tuple[Response, int]:
    try:
        product = Product.query.get(product_id)
        if product is None:
            return jsonify({"error": f"Order {product_id} not found"}), 404
        return product
    except Exception as err:
        logger.error(err)


def update_product(product_id: int, data: UpdateProductSchema) -> Product:
    try:
        product = get_product_by_id(product_id)
        if isinstance(product, tuple):
            return product
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(product, key, value)
        db.session.commit()
        return product
    except IntegrityError as err:
        db.session.rollback()
        logger.error(f"Database error: {str(err)}")
    except Exception as err:
        db.session.rollback()
        logger.error(err)


def delete_product(product_id: int):
    try:
        product = get_product_by_id(product_id)
        if isinstance(product, tuple):
            return product
        db.session.delete(product)
        db.session.commit()
    except IntegrityError as err:
        db.session.rollback()
        logger.error(f"Database error: {str(err)}")
    except Exception as err:
        db.session.rollback()
        logger.error(err)
