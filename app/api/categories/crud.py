from app.api.categories.schemas import CreateCategorySchema, CategorySchemaUpdate
from sqlalchemy.exc import IntegrityError
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
        logger.error(err)


def get_categories() -> list[Category]:
    try:
        categories = Category.query.all()
        return categories
    except Exception as err:
        db.session.rollback()
        logger.error(err)


def get_category_by_is(category_id: int) -> Category | tuple[Response, int]:
    try:
        category = Category.query.filter(Category.id == category_id).first()
        if category is None:
            return jsonify({"error": "Category not found"}), 404
        return category
    except Exception as err:
        db.session.rollback()
        logger.error(err)


def update_category(category_id: int, data: CategorySchemaUpdate) -> Category:
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
    except Exception as err:
        db.session.rollback()
        logger.error(err)


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
    except Exception as err:
        db.session.rollback()
        logger.error(err)
