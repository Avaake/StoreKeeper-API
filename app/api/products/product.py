from app.api.products.schemas import (
    CreateProductSchema,
    ProductSchemaRead,
    UpdateProductSchema,
)
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from app.api.products import crud
from app.core import settings
from app.core import logger

bp = Blueprint("product", __name__, url_prefix=settings.api_prefix.products)


@bp.route("", methods=["POST"])
@jwt_required()
def create_product():
    try:
        data = CreateProductSchema(**request.json)
        product = crud.create_product(data)
        if isinstance(product, tuple):
            return product

        return (
            jsonify(
                {
                    "message": "Product created successfully",
                    "product": ProductSchemaRead.model_validate(product).model_dump(),
                }
            ),
            201,
        )
    except ValidationError as err:
        logger.info({"error": "Validation error", "details": err.errors()})
        return jsonify({"error": "Validation error"}), 422
    except Exception as err:
        logger.error(err)
        return jsonify({"error": "Internal Server Error. Try again later"}), 500


@bp.route("", methods=["GET"])
@jwt_required()
def get_products():
    try:
        products = crud.get_products()
        return (
            jsonify(
                {
                    "products": [
                        ProductSchemaRead.model_validate(product).model_dump()
                        for product in products
                    ]
                }
            ),
            200,
        )
    except Exception as err:
        logger.error(err)
        return jsonify({"error": "Internal Server Error. Try again later"}), 500


@bp.route("<int:product_id>", methods=["GET"])
@jwt_required()
def get_product(product_id: int):
    try:
        product = crud.get_product_by_id(product_id)
        if isinstance(product, tuple):
            return product
        return (
            jsonify(
                {"product": ProductSchemaRead.model_validate(product).model_dump()}
            ),
            200,
        )
    except Exception as err:
        logger.error(err)
        return jsonify({"error": "Internal Server Error. Try again later"}), 500


@bp.route("<int:product_id>", methods=["PATCH"])
@jwt_required()
def update_product(product_id: int):
    try:
        data = UpdateProductSchema.model_validate(request.json)
        product = crud.update_product(product_id, data)
        if isinstance(product, tuple):
            return product

        return (
            jsonify(
                {"product": ProductSchemaRead.model_validate(product).model_dump()}
            ),
            200,
        )

    except ValidationError as err:
        return jsonify({"error": "Validation error", "details": err.errors()}), 400
    except Exception as err:
        logger.error(err)
        return jsonify({"error": "Internal Server Error. Try again later"}), 500


@bp.route("<int:product_id>", methods=["DELETE"])
@jwt_required()
def delete_product(product_id: int):
    try:
        product = crud.delete_product(product_id)
        if isinstance(product, tuple):
            return product
        return jsonify(""), 204
    except Exception as err:
        logger.error(err)
        return jsonify({"error": "Internal Server Error. Try again later"}), 500
