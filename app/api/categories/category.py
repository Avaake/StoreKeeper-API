from app.api.categories.schemas import (
    CreateCategorySchema,
    CategorySchemaRead,
    CategorySchemaUpdate,
)
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.core import settings, logger
from pydantic import ValidationError
from app.api.categories import crud


bp = Blueprint("category", __name__, url_prefix=settings.api_prefix.categories)


@bp.route("", methods=["POST"])
@jwt_required()
def create_category():
    try:
        data = CreateCategorySchema(**request.json)
        category = crud.create_category(data)
        if isinstance(category, tuple):
            return category
        return (
            jsonify(
                {
                    "message": "Category created successfully",
                    "category": CategorySchemaRead.model_validate(
                        category
                    ).model_dump(),
                }
            ),
            201,
        )
    except ValidationError as err:
        logger.info({"error": "Validation error", "details": err.errors()})
        return jsonify({"error": "Validation error"}), 400
    except Exception as err:
        logger.error(err)
        return jsonify({"error": "Internal Server Error. Try again later"}), 500


@bp.route("", methods=["GET"])
@jwt_required()
def get_categories():
    try:
        categories = crud.get_categories()
        return (
            jsonify(
                {
                    "categories": [
                        CategorySchemaRead(
                            id=category.id, name=category.name
                        ).model_dump()
                        for category in categories
                    ]
                }
            ),
            200,
        )
    except Exception as err:
        logger.error(err)
        return jsonify({"error": "Internal Server Error. Try again later"}), 500


@bp.route("/<int:category_id>", methods=["GET"])
@jwt_required()
def get_category(category_id: int):
    try:
        category = crud.get_category_by_is(category_id)
        if isinstance(category, tuple):
            return category
        return (
            jsonify(
                {
                    "category": CategorySchemaRead.model_validate(
                        category
                    ).model_dump(),
                }
            ),
            200,
        )
    except Exception as err:
        logger.error(err)
        return jsonify({"error": "Internal Server Error. Try again later"}), 500


@bp.route("/<int:category_id>", methods=["PATCH"])
@jwt_required()
def update_category(category_id: int):

    try:
        data = CategorySchemaUpdate.model_validate(request.json)
        category = crud.update_category(category_id, data)
        if isinstance(category, tuple):
            return category
        return (
            jsonify(
                {"category": CategorySchemaRead.model_validate(category).model_dump()}
            ),
            200,
        )
    except ValidationError as err:
        logger.info({"error": "Validation error", "details": err.errors()})
        return jsonify({"error": "Validation error"}), 400
    except Exception as err:
        logger.error(err)
        return jsonify({"error": "Internal Server Error. Try again later"}), 500


@bp.route("/<int:category_id>", methods=["DELETE"])
@jwt_required()
def delete_category(category_id: int):
    try:
        category = crud.delete_order(category_id)
        if isinstance(category, tuple):
            return category
        return jsonify(""), 204
    except Exception as err:
        logger.error(err)
        return jsonify({"error": "Internal Server Error. Try again later"}), 500
