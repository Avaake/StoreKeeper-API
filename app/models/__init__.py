__all__ = [
    "db",
    "Base",
    "User",
    "Category",
    "Product",
    "Order",
    "OrderItem",
]


from .db import database, Base, User, Category, Product, Order, OrderItem

db = database.get_db()
