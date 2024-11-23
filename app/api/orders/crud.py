from app.api.orders.schemas import OrderItemCrateSchema
from app.models import db, Order, OrderItem
from sqlalchemy.exc import IntegrityError
from flask import jsonify, Response
from app.api.products import crud
from app.core import logger


def count_total_price_and_check_quantity_product_in_stock(
    products: list[OrderItemCrateSchema],
) -> int | tuple[Response, int]:
    try:
        total_price = 0
        for i in products:
            product = crud.get_product(i.product_id)
            if product is None:
                return (
                    jsonify({"error": f"Product with ID {i.product_id} not found"}),
                    404,
                )
            if product.quantity < i.quantity:
                return (
                    jsonify(
                        {
                            "error": f"Недостатня кількість товару {product.name} на складі. "
                            f"В наявності: {product.quantity}"
                        }
                    ),
                    400,
                )

            total_price += product.price * i.quantity

        return total_price
    except Exception as err:
        logger.error(err)
        return jsonify({"error": "Internal Server Error"}), 500


def create_order(
    user_id: int, products: list[OrderItemCrateSchema]
) -> Order | tuple[Response, int]:
    try:
        total = count_total_price_and_check_quantity_product_in_stock(products)
        if isinstance(total, tuple):
            return total
        order = Order(
            user_id=user_id,
            total_price=total,
        )
        db.session.add(order)

        for i in products:
            product = crud.get_product(i.product_id)
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=i.quantity,
                price=product.price,
            )
            db.session.add(order_item)

            product.quantity -= i.quantity

        db.session.commit()
        return order
    except IntegrityError as err:
        db.session.rollback()
        logger.error(f"Database error: {str(err)}")
        return jsonify({"error": "Failed to process order. Try again later"}), 500
    except Exception as err:
        logger.error(err)
        return jsonify({"error": "Internal Server Error"}), 500


def get_orders() -> list[Order] | tuple[Response, int]:
    try:
        orders = Order.query.all()
        return orders
    except Exception as err:
        logger.error(err)
        return jsonify({"error": "Internal Server Error"}), 500


def get_order(order_id: int) -> Order | tuple[Response, int]:
    try:
        order = Order.query.filter(Order.id == order_id).first()
        if order is None:
            return jsonify({"error": f"Order {order_id} not found"}), 404
        return order
    except IntegrityError as err:
        logger.error(f"Database error: {str(err)}")
        return jsonify({"error": "Internal Server Error"}), 500
    except Exception as err:
        logger.error(err)
        return jsonify({"error": "Internal Server Error"}), 500


def delete_order(order_id: int) -> tuple[Response, int]:
    try:
        order = get_order(order_id)
        if isinstance(order, tuple):
            return order
        db.session.delete(order)
        db.session.commit()
    except IntegrityError as err:
        db.session.rollback()
        logger.error(f"Database error: {str(err)}")
        return jsonify({"error": "Failed to delete order data. Try again later"}), 400
    except Exception as err:
        logger.error(err)
        return jsonify({"error": "Internal Server Error"}), 500
