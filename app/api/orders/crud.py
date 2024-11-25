from app.api.orders.schemas import OrderItemCrateSchema, OrderUpdateSchema
from app.models import db, Order, OrderItem, Product
from sqlalchemy.exc import IntegrityError
from flask import jsonify, Response
from app.api.products import crud
from app.core import logger


def check_quantity_product_in_stock(product: Product, required_quantity: int):
    if (
        product.quantity < required_quantity
    ):  # Порівнюємо product.quantity з required_quantity без .quantity
        return (
            jsonify(
                {
                    "error": f"Insufficient quantity of product {product.name} in stock. "
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
            product = crud.get_product(i.product_id)
            if product is None:
                return (
                    jsonify({"error": f"Product with ID {i.product_id} not found"}),
                    404,
                )
            check_quantity = check_quantity_product_in_stock(product, i.quantity)
            if check_quantity is not None:
                return check_quantity
            total_price += product.price * i.quantity

        return total_price
    except Exception as err:
        logger.error(err)
        return jsonify({"error": "Internal Server Error. Try again later"}), 500


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
        return jsonify({"error": "Internal Server Error. Try again later"}), 500
    except Exception as err:
        logger.error(err)
        return jsonify({"error": "Internal Server Error. Try again later"}), 500


def get_orders() -> list[Order] | tuple[Response, int]:
    try:
        orders = Order.query.all()
        return orders
    except Exception as err:
        logger.error(err)
        return jsonify({"error": "Internal Server Error. Try again later"}), 500


def get_order_by_id(order_id: int) -> Order | tuple[Response, int]:
    try:
        order = Order.query.filter(Order.id == order_id).first()
        if order is None:
            return jsonify({"error": f"Order {order_id} not found"}), 404
        return order
    except IntegrityError as err:
        logger.error(f"Database error: {str(err)}")
        return jsonify({"error": "Internal Server Error. Try again later"}), 500
    except Exception as err:
        logger.error(err)
        return jsonify({"error": "Internal Server Error. Try again later"}), 500


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
        return jsonify({"error": "Internal Server Error. Try again later"}), 400
    except Exception as err:
        logger.error(err)
        return jsonify({"error": "Internal Server Error. Try again later"}), 500


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
        return jsonify({"error": "Internal Server Error. Try again later"}), 500
    except Exception as err:
        db.session.rollback()
        logger.error(err)
        return jsonify({"error": "Internal Server Error. Try again later"}), 500
