from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy import MetaData, VARCHAR, func, Text, ForeignKey, DECIMAL, Enum
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
    role: Mapped[str] = mapped_column(
        VARCHAR(15), default="user", server_default="user"
    )

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
    name: Mapped[str] = mapped_column(VARCHAR(255), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column()
    quantity: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )

    category: Mapped["Category"] = relationship(back_populates="products")
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="product")

    def __repr__(self):
        return (
            f"Product(id={self.id}, name={self.name}, description={self.description}, "
            f"price={self.price}, quantity={self.quantity}, created_at={self.created_at}, "
            f"updated_at={self.updated_at})"
        )


class Order(database.get_db().Model):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(
        Enum("pending", "completed", "cancelled", name="order_status"),
        server_default="pending",
    )
    total_price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"Order(id={self.id}, user_id={self.user_id}, status={self.status}, "
            f"total_price={self.total_price}, created_at={self.created_at}, updated_at={self.updated_at})"
        )


class OrderItem(database.get_db().Model):
    __tablename__ = "order_items"
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="SET NULL"), nullable=True
    )
    quantity: Mapped[int] = mapped_column()
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    order: Mapped["Order"] = relationship(back_populates="order_items")

    product: Mapped["Product"] = relationship(back_populates="order_items")

    def __repr__(self):
        return (
            f"OrderItem(id={self.id}, order_id={self.order_id}, product_id={self.product_id}, "
            f"quantity={self.quantity}, price={self.price})"
        )


class Supplier(database.get_db().Model):
    name: Mapped[str] = mapped_column(VARCHAR(255), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(VARCHAR(50), nullable=True)
    phone_number: Mapped[str] = mapped_column(VARCHAR(20), nullable=True)
    address: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    supplies: Mapped[list["Supply"]] = relationship(back_populates="supplier")

    def __repr__(self):
        return (
            f"Supplier(id={self.id}, name={self.name}, email={self.email}, "
            f"phone_number={self.phone_number}, address={self.address})"
        )


class Supply(database.get_db().Model):
    __tablename__ = "supplies"
    product_name: Mapped[str] = mapped_column(VARCHAR(255))
    quantity: Mapped[int] = mapped_column()
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.id", ondelete="SET NULL"), nullable=True
    )
    delivery_date: Mapped[datetime] = mapped_column()
    status: Mapped[str] = mapped_column(
        Enum("pending", "delivery", "cancelled", name="supply_status"),
        server_default="pending",
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    supplier: Mapped["Supplier"] = relationship(back_populates="supplies")

    def __repr__(self):
        return (
            f"Supply(id={self.id}, product_name={self.product_name}, quantity={self.quantity}, price={self.price}, "
            f"supplier_id={self.supplier_id}, delivery_date={self.delivery_date}, "
            f"created_at={self.created_at}, updated_at={self.updated_at})"
        )
