from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy import MetaData, VARCHAR, func, Text, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from app.core import settings
from datetime import datetime


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"


class Database:
    def __init__(self, base):
        self.__db = SQLAlchemy(model_class=base)

    def get_db(self) -> SQLAlchemy:
        return self.__db


database = Database(Base)


class User(database.get_db().Model):
    username: Mapped[str] = mapped_column(VARCHAR(30), nullable=False)
    email: Mapped[str] = mapped_column(VARCHAR(50), unique=True, nullable=False)
    password_hash: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.utcnow
    )
    role: Mapped[str] = mapped_column(VARCHAR(5), default="user", server_default="user")

    def __repr__(self):
        return (
            f"User(id={self.id}, username={self.username}, email={self.email}, "
            f"password_hash={self.password_hash}, created_at={self.created_at}, role={self.role})"
        )


class Category(database.get_db().Model):
    __tablename__ = "categories"
    name: Mapped[str] = mapped_column(VARCHAR(30), nullable=False, unique=True)

    products: Mapped[list["Product"]] = relationship(back_populates="category")

    def __repr__(self):
        return f"Category(id={self.id}, name={self.name})"


class Product(database.get_db().Model):
    name: Mapped[str] = mapped_column(VARCHAR(255))
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column()
    quantity: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    category: Mapped["Category"] = relationship(back_populates="products")

    def __repr__(self):
        return (
            f"Product(id={self.id}, name={self.name}, description={self.description}, "
            f"price={self.price}, quantity={self.quantity}, created_at={self.created_at}, "
            f"updated_at={self.updated_at})"
        )
