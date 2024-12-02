from app.core import logger
from app.models import OrderItem, Product, db
from typing import Union
from sqlalchemy import desc, func
from sqlalchemy.exc import IntegrityError


def calculate_sales_report(
    product_id: Union[int, None] = None,
    category_id: Union[int, None] = None,
) -> dict:
    query = (
        db.session.query(
            Product.name,
            func.sum(OrderItem.quantity).label("total_quantity"),
            func.sum(OrderItem.price * OrderItem.quantity).label("total_revenue"),
        )
        .join(OrderItem)
        .filter(OrderItem.quantity <= 15)
    )

    if product_id:
        query = query.filter(OrderItem.product_id == product_id)
    if category_id:
        query = query.filter(Product.category_id == category_id)

    result = query.group_by(Product.name).all()

    total_sales = sum([row.total_revenue for row in result])
    total_orders = sum([row.total_quantity for row in result])

    best_selling_products: list[dict[str, Union[str, int]]] = [
        {
            "name": row.name,
            "quantity": row.total_quantity,
            "revenue": int(row.total_revenue),
        }
        for row in result
    ]

    best_selling_products.sort(key=lambda x: x["revenue"], reverse=True)

    return {
        "total_sales": int(total_sales),
        "total_orders": int(total_orders),
        "best_selling_products": best_selling_products,
    }


def list_of_items_in_short_supply(
    category_id: Union[int, None] = None
) -> list[Product]:
    try:
        products = Product.query.filter(Product.quantity <= 15)

        if category_id:
            products = products.filter(Product.category_id == category_id)
        products = products.order_by(desc(Product.quantity))
        return products.all()
    except IntegrityError as err:
        logger.error(f"Database error: {str(err)}")
    except Exception as err:
        logger.error(err)