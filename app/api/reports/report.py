from app.api.products.schemas import ProductSchemaRead
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.core import settings, logger
from app.api.reports import utils

bp = Blueprint("reports", __name__, url_prefix=settings.api_prefix.reports)


@bp.route("/sales", methods=["GET"])
@jwt_required()
def get_sales_report():
    try:
        product_id = request.args.get("product_id", None)
        category_id = request.args.get("category_id", None)

        if product_id and category_id:
            sales_report = utils.calculate_sales_report(
                product_id=int(product_id), category_id=int(category_id)
            )
        elif product_id:
            sales_report = utils.calculate_sales_report(product_id=int(product_id))
        elif category_id:
            sales_report = utils.calculate_sales_report(category_id=int(category_id))
        else:
            sales_report = utils.calculate_sales_report()

        return jsonify(sales_report), 200
    except Exception as err:
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later"}), 500


@bp.route("/inventory", methods=["GET"])
@jwt_required()
def get_products_that_end():
    try:
        category_id = request.args.get("category_id", None)
        if category_id:
            products = utils.list_of_items_in_short_supply(category_id=int(category_id))
        else:
            products = utils.list_of_items_in_short_supply()

        return (
            jsonify(
                {
                    "message": "Products in short supply retrieved successfully.",
                    "products": [
                        ProductSchemaRead.model_validate(product).model_dump()
                        for product in products
                    ],
                }
            ),
            200,
        )
    except Exception as err:
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later"}), 500
