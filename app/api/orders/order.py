from flask_jwt_extended import jwt_required, current_user
from app.api.orders.schemas import (
    OrderCreateSchema,
    OrderUpdateSchema,
    FilterOrderSchema,
)
from app.api.orders.utils import order_to_dict
from flask import Blueprint, request, jsonify
from app.core import settings, logger
from pydantic import ValidationError
from app.api.orders import crud


bp = Blueprint("orders", __name__, url_prefix=settings.api_prefix.orders)


@bp.route("", methods=["POST"])
@jwt_required()
def create_order():
    try:
        data = OrderCreateSchema(**request.json)
        orders = crud.create_order(user_id=current_user.id, products=data.products)

        if isinstance(orders, tuple):
            return orders

        return (
            jsonify(
                {
                    "message": "Order created successfully",
                    "order": order_to_dict(orders),
                }
            ),
            200,
        )
    except ValidationError as err:
        logger.info({"error": "Validation error", "details": err.errors()})
        return jsonify({"error": "Validation error", "details": err.errors()}), 422
    except Exception as err:
        logger.error({"error": str(err)})
        return jsonify({"error": "Internal Server Error. Try again later"}), 500


@bp.route("", methods=["GET"])
@jwt_required()
def get_orders():
    try:
        query_param = FilterOrderSchema(**request.args)
        orders = crud.get_orders_by_filter(
            status=query_param.status.name,
            start_day=query_param.start_day,
            end_day=query_param.end_day,
        )
        if isinstance(orders, tuple):
            return orders
        return (
            jsonify({"orders": [order_to_dict(order) for order in orders]}),
            200,
        )
    except ValidationError as err:
        logger.info({"error": "Validation error", "details": err.errors()})
        return jsonify({"error": "Validation error", "details": err.errors()}), 422
    except Exception as err:
        logger.error({"error": str(err)})
        return jsonify({"error": "Internal Server Error. Try again later"}), 500


@bp.route("<int:order_id>", methods=["GET"])
@jwt_required()
def get_order(order_id: int):
    try:
        order = crud.get_order_by_id(order_id)

        if isinstance(order, tuple):
            return order
        return (
            jsonify({"order": order_to_dict(order)}),
            200,
        )
    except Exception as err:
        logger.error({"error": str(err)})
        return jsonify({"error": "Internal Server Error. Try again later"}), 500


@bp.route("<int:order_id>", methods=["PATCH"])
@jwt_required()
def update_order(order_id: int):
    try:
        data = OrderUpdateSchema(**request.json)
        order = crud.update_order(order_id, data)
        if isinstance(order, tuple):
            return order
        return (
            jsonify({"order": order_to_dict(order)}),
            200,
        )
    except ValidationError as err:
        return jsonify({"error": "Validation error", "details": err.errors()}), 422
    except Exception as err:
        logger.error({"error": str(err)})
        return jsonify({"error": "Internal Server Error. Try again later"}), 500


@bp.route("<int:order_id>", methods=["DELETE"])
@jwt_required()
def delete_order(order_id: int):
    try:
        user = crud.delete_order(order_id)
        if isinstance(user, tuple):
            return user
        return jsonify(""), 204
    except Exception as err:
        logger.error({"error": str(err)})
        return jsonify({"error": "Internal Server Error. Try again later"}), 500
