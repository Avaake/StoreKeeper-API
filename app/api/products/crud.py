from app.api.categories.crud import get_category_by_is
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from flask import jsonify, Response
from app.models import db, Product
from app.api.products.schemas import (
    CreateProductSchema,
    UpdateProductSchema,
)
from sqlalchemy import or_, func
from app.core import logger
from typing import Union


def create_product(data: CreateProductSchema) -> Product | tuple[Response, int]:
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
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later."}), 500


def get_products_by_filter(
    product_keyword: Union[str, None] = None,
    category_id: Union[int, None] = None,
    price_min: Union[str, None] = None,
    price_max: Union[str, None] = None,
) -> list[Product] | tuple[Response, int]:
    try:
        products = Product.query.order_by(Product.id)
        # search
        if product_keyword:
            products = products.filter(
                or_(
                    func.lower(Product.name).like(f"%{product_keyword}%"),
                    func.lower(Product.description).like(f"%{product_keyword}%"),
                )
            )
        # filter
        if category_id:
            products = products.filter(Product.category_id == category_id)
        if price_min:
            products = products.filter(Product.price >= price_min)
        if price_max:
            products = products.filter(Product.price <= price_max)

        return products.all()
    except Exception as err:
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later."}), 500


def get_product_by_id(product_id: int) -> Product | tuple[Response, int]:
    try:
        product = Product.query.filter_by(id=product_id).first()
        if product is None:
            raise NotFound("Product not found")
        return product
    except NotFound as not_found_err:
        logger.info(f"NotFound error: {not_found_err}")
        return jsonify({"error": str(not_found_err)}), 404
    except Exception as err:
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later."}), 500


def update_product(
    product_id: int, data: UpdateProductSchema
) -> Product | tuple[Response, int]:
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
        return (
            jsonify(
                {
                    "error": "There was an issue processing your request. Please try again later."
                }
            ),
            422,
        )
    except Exception as err:
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later."}), 500


def delete_product(product_id: int) -> Product | tuple[Response, int]:
    try:
        product = get_product_by_id(product_id)
        if isinstance(product, tuple):
            return product
        db.session.delete(product)
        db.session.commit()
    except IntegrityError as err:
        db.session.rollback()
        logger.error(f"Database error: {str(err)}")
        return (
            jsonify(
                {
                    "error": "There was an issue processing your request. Please try again later."
                }
            ),
            422,
        )
    except Exception as err:
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later."}), 500
