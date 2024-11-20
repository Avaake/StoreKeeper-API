from app.api.categories.schemas import (
    CreateCategorySchema,
    CategorySchemaRead,
    CategoryListRead,
)
from flask_jwt_extended import current_user, jwt_required
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from app.core import settings, logger
from pydantic import ValidationError
from app.models import Category, db


bp = Blueprint("category", __name__, url_prefix=settings.api_prefix.category)


@bp.route("", methods=["POST"])
# @jwt_required()
def create_category():
    try:
        data = CreateCategorySchema.model_validate(request.json)
    except ValidationError as err:
        logger.info({"error": "Validation error", "details": err.errors()})
        return jsonify({"error": "Validation error"}), 400

    try:
        new_category = Category(name=data.name)
        db.session.add(new_category)
        db.session.commit()
        logger.info(f"created {new_category.name} category.")
    except IntegrityError as err:
        db.session.rollback()
        logger.error(f"Integrity error: {err.params}")
        return jsonify("Така категорія вже існує!"), 400

    return jsonify(data.model_dump()), 201


@bp.route("", methods=["GET"])
# @jwt_required()
def get_categories():
    categories = Category.query.all()

    categories_list = CategoryListRead(
        categories=[
            CategorySchemaRead.model_validate(category) for category in categories
        ]
    )
    return jsonify(categories_list.model_dump()), 200


@bp.route("/<int:category_id>", methods=["GET"])
# @jwt_required()
def get_category(category_id: int):
    category = Category.query.get_or_404(category_id)
    category_data = CategorySchemaRead.model_validate(category)
    return jsonify(category_data.model_dump()), 200


@bp.route("/<int:category_id>", methods=["PUT", "PATCH"])
# @jwt_required()
def update_category(category_id: int):
    category = Category.query.get_or_404(category_id)

    try:
        data = CategorySchemaRead.model_validate(request.json or {})
    except ValidationError as err:
        logger.info({"error": "Validation error", "details": err.errors()})
        return jsonify({"error": "Validation error"}), 400

    category.name = data.name
    data.id = category.id
    db.session.commit()
    logger.info(f"updated category {category.name}.")
    return jsonify(data.model_dump()), 200


@bp.route("/<int:category_id>", methods=["DELETE"])
# @jwt_required()
def delete_category(category_id: int):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    logger.info(f"deleted {category.name} category.")
    return jsonify({"success": True}), 204
