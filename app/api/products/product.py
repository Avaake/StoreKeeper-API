from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.api.products.schemas import (
    CreateProductSchema,
    ProductSchemaRead,
    ProductListRead,
    UpdateProductSchema,
)
from app.core import settings
from app.models import Product, db, Category
from sqlalchemy.exc import IntegrityError
from app.core import logger

bp = Blueprint("product", __name__, url_prefix=settings.api_prefix.products)


@bp.route("", methods=["POST"])
def create_product():
    try:
        data = CreateProductSchema.model_validate(request.json)
    except ValidationError as err:
        return jsonify({"error": "Validation error"}), 400

    category = Category.query.get(data.category_id)
    if not category:
        return (
            jsonify(
                {
                    "error": "Category does not exist",
                    "details": f"Category with id {data.category_id} not found",
                }
            ),
            400,
        )
    try:
        product = Product(
            name=data.name,
            description=data.description,
            price=data.price,
            quantity=data.quantity,
            category_id=data.category_id,
        )
        print(product)
        db.session.add(product)
        db.session.commit()
    except IntegrityError as err:
        db.session.rollback()
        logger.error(f"Database error: {str(err)}")
        return (
            jsonify(
                {"error": "An internal server error occurred. Please try again later."}
            ),
            500,
        )

    return jsonify(data.model_dump()), 201


@bp.route("", methods=["GET"])
def get_products():
    products = Product.query.all()
    products_list = ProductListRead(
        products=[ProductSchemaRead.model_validate(product) for product in products]
    )
    return jsonify(products_list.model_dump()), 200


@bp.route("<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    product_data = ProductSchemaRead.model_validate(product)
    return jsonify(product_data.model_dump()), 200


@bp.route("<int:product_id>", methods=["PATCH"])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)

    try:
        data = UpdateProductSchema.model_validate(request.json)
    except ValidationError as err:
        return jsonify({"error": "Validation error", "details": err.errors()}), 400

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(product, key, value)

    db.session.commit()

    return (
        jsonify(UpdateProductSchema.model_validate(product.__dict__).model_dump()),
        200,
    )


@bp.route("<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"success": True}), 204
