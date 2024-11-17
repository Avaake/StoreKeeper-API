__all__ = ["db", "Base", "User"]


from .db import database, Base, User

db = database.get_db()
