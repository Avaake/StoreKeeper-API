__all__ = [
    "db",
    "Base",
    "User",
    "Category",
    "Product",
]


from .db import database, Base, User, Category, Product

db = database.get_db()
