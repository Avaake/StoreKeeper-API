from app.api.orders.schemas import OrderItemsRead


def order_to_dict(order):
    return {
        "id": order.id,
        "user_id": order.user_id,
        "status": order.status,
        "total_price": order.total_price,
        "created_at": order.created_at,
        "order_items": [
            OrderItemsRead(
                product_id=item.product_id,
                product_name=item.product.name,
                quantity=item.quantity,
                price=item.price,
            ).model_dump()
            for item in order.order_items
        ],
    }
