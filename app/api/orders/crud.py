from app.api.orders.schemas import OrderItemCrateSchema, OrderUpdateSchema
from app.models import db, Order, OrderItem, Product
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from flask import jsonify, Response
from app.api.products import crud
from app.core import logger
from typing import Union


def check_quantity_product_in_stock(product: Product, required_quantity: int):
    if product.quantity < required_quantity:
        return (
            jsonify(
                {
                    "error": f"Insufficient quantity of product. "
                    f"Available: {product.quantity}, required: {required_quantity}"
                }
            ),
            400,
        )
    return None


def count_total_price_and(
    products: list[OrderItemCrateSchema],
) -> int | tuple[Response, int]:
    try:
        total_price = 0
        for i in products:
            product = crud.get_product_by_id(i.product_id)
            if isinstance(product, tuple):
                return product
            check_quantity = check_quantity_product_in_stock(product, i.quantity)
            if check_quantity is not None:
                return check_quantity
            total_price += product.price * i.quantity

        return total_price
    except Exception as err:
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later."}), 500


def create_order(
    user_id: int, products: list[OrderItemCrateSchema]
) -> Order | tuple[Response, int]:
    try:
        total = count_total_price_and(products)
        if isinstance(total, tuple):
            return total
        order = Order(
            user_id=user_id,
            total_price=total,
        )
        db.session.add(order)

        for i in products:
            product = crud.get_product_by_id(i.product_id)
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


def get_orders_by_filter(
    status: Union[str, None] = None,
    start_day: Union[str, None] = None,
    end_day: Union[str, None] = None,
) -> list[Order] | tuple[Response, int]:
    try:
        orders = Order.query.order_by(Order.id)
        if status:
            orders = orders.filter(Order.status == status)

        if start_day:
            orders = orders.filter(Order.created_at >= start_day)
        if end_day:
            orders = orders.filter(Order.created_at <= end_day)

        return orders.all()
    except Exception as err:
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later."}), 500


def get_order_by_id(order_id: int) -> Order | tuple[Response, int]:
    try:
        order = Order.query.filter(Order.id == order_id).first()
        if order is None:
            raise NotFound(f"Order {order_id} not found")
        return order
    except IntegrityError as err:
        logger.error(f"Database error: {str(err)}")
    except NotFound as not_found_err:
        logger.info(f"NotFound error: {not_found_err}")
        return jsonify({"error": str(not_found_err)}), 404
    except Exception as err:
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later."}), 500


def delete_order(order_id: int) -> tuple[Response, int]:
    try:
        order = get_order_by_id(order_id)
        if isinstance(order, tuple):
            return order
        db.session.delete(order)
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
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later."}), 500


def update_order(order_id: int, data: OrderUpdateSchema):
    try:
        order = get_order_by_id(order_id)
        if isinstance(order, tuple):
            return order

        status = data.status.name if data.status else None
        if status is not None:
            if status == "cancelled":
                order.status = status
                db.session.commit()
                return order
            else:
                order.status = status

        if data.products is not None:
            for product in data.products:

                for order_item in order.order_items:
                    if order_item.product_id == product.product_id:
                        ordered_quantity = product.quantity
                        current_quantity = order_item.quantity

                        # кількість в замовленні збільшилася
                        if ordered_quantity > current_quantity:
                            difference = ordered_quantity - current_quantity
                            check_quantity = check_quantity_product_in_stock(
                                order_item.product, difference
                            )
                            if check_quantity is not None:
                                return check_quantity
                            # Оновлюємо кількість товару в замовленні та на складі
                            order_item.quantity = ordered_quantity
                            order_item.product.quantity -= difference
                        # кількість в замовленні зменшилася
                        elif ordered_quantity < current_quantity:
                            difference = current_quantity - ordered_quantity
                            order_item.quantity = ordered_quantity
                            order_item.product.quantity += difference

        db.session.commit()
        return order
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
        logger.error(f"Exception: {err}")
        return jsonify({"error": "Internal Server Error. Try again later."}), 500
