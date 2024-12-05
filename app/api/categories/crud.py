from app.api.categories.schemas import CreateCategorySchema, CategorySchemaUpdate
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from app.models import db, Category
from flask import jsonify, Response
from app.core import logger


def create_category(data: CreateCategorySchema) -> Category | tuple[Response, int]:
    try:
        category = Category(name=data.name)
        db.session.add(category)
        db.session.commit()
        return category
    except IntegrityError as err:
        db.session.rollback()
        logger.error(f"Database error: {str(err)}")
        return jsonify({"error": "This category already exists"}), 400
    except Exception as err:
        db.session.rollback()
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later."}), 500


def get_categories() -> list[Category] | tuple[Response, int]:
    try:
        categories = Category.query.all()
        return categories
    except Exception as err:
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later."}), 500


def get_category_by_is(category_id: int) -> Category | tuple[Response, int]:
    try:
        category = Category.query.filter_by(id=category_id).first()
        if category is None:
            raise NotFound("Category not found")
        return category
    except NotFound as not_found_err:
        logger.info(f"NotFound error: {not_found_err}")
        return jsonify({"error": str(not_found_err)}), 404
    except Exception as err:
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later."}), 500


def update_category(
    category_id: int, data: CategorySchemaUpdate
) -> Category | tuple[Response, int]:
    try:
        category = get_category_by_is(category_id)
        if isinstance(category, tuple):
            return category
        category.name = data.name
        db.session.commit()
        return category
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
        db.session.rollback()
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later."}), 500


def delete_order(category_id: int) -> tuple[Response, int]:
    try:
        category = get_category_by_is(category_id)
        if isinstance(category, tuple):
            return category
        db.session.delete(category)
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
        db.session.rollback()
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later."}), 500
