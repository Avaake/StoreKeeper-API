from flask_jwt_extended import jwt_required, current_user
from app.api.orders.schemas import OrderCreateSchema
from app.api.orders.utils import order_to_dict
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.api.orders import crud
from app.core import settings
from app.core import logger


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
        return jsonify({"error": "Validation error", "details": err.errors()}), 422


@bp.route("", methods=["GET"])
def get_orders():
    orders = crud.get_orders()

    return (
        jsonify({"orders": [order_to_dict(order) for order in orders]}),
        200,
    )


@bp.route("<int:order_id>", methods=["GET"])
def get_order(order_id: int):
    order = crud.get_order(order_id)

    if isinstance(order, tuple):
        return order
    return (
        jsonify({"order": order_to_dict(order)}),
        200,
    )


@bp.route("<int:order_id>", methods=["PATCH"])
def update_order(order_id: int):
    pass


@bp.route("<int:order_id>", methods=["DELETE"])
def delete_order(order_id: int):
    user = crud.delete_order(order_id)
    if isinstance(user, tuple):
        return user
    return jsonify({"success": True}), 204
