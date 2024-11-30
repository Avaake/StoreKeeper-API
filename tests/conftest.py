from werkzeug.security import generate_password_hash
from app.models import db, User, Category, Product, Order, OrderItem
from app.core import test_settings
from app import create_app
import pytest


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app()

    flask_app.config["SQLALCHEMY_DATABASE_URI"] = str(test_settings.db.url)
    flask_app.config["TESTING"] = test_settings.testing
    flask_app.config["JWT_SECRET_KEY"] = test_settings.jwt.secret_key

    with flask_app.test_client() as test_client:
        with flask_app.app_context():
            yield test_client


@pytest.fixture(scope="module")
def init_db(test_client):
    db.create_all()

    admin_user = User(
        username="admin",
        email="admin@gmail.com",
        password_hash=generate_password_hash(password="admin"),
        role="admin",
    )
    sem_user = User(
        username="sem",
        email="sem@gmail.com",
        password_hash=generate_password_hash(password="sem_password"),
    )

    db.session.add(admin_user)
    db.session.add(sem_user)
    db.session.commit()

    apple_category = Category(name="apple")
    samsung_category = Category(name="samsung")
    db.session.add_all([apple_category, samsung_category])
    db.session.commit()

    product1 = Product(
        name="macbook air",
        description="macbook air description",
        price=60000,
        quantity=11,
        category_id=1,
    )
    product2 = Product(
        name="samsung 4a",
        description="samsung 4a description",
        price=7000,
        quantity=5,
        category_id=2,
    )
    product3 = Product(
        name="aphone 16",
        description="iphone 16 description",
        price=40000,
        quantity=2,
        category_id=1,
    )
    db.session.add_all([product1, product2, product3])
    db.session.commit()

    order1 = Order(user_id=2, total_price=188000)
    order_item1 = OrderItem(order_id=1, product_id=1, quantity=2, price=120000)
    order_item2 = OrderItem(order_id=1, product_id=3, quantity=1, price=40000)
    order_item3 = OrderItem(order_id=1, product_id=2, quantity=4, price=28000)
    db.session.add(order1)
    db.session.add_all([order_item1, order_item2, order_item3])
    db.session.commit()

    yield

    db.session.remove()
    db.drop_all()


@pytest.fixture(scope="module")
def admin_token(test_client):
    response = test_client.post(
        "api/v1/auth/login",
        json={
            "email": "admin@gmail.com",
            "password": "admin",
        },
    )

    yield response.json["access_token"], response.json["refresh_token"]


@pytest.fixture(scope="module")
def sem_token(test_client):
    response = test_client.post(
        "api/v1/auth/login",
        json={
            "email": "sem@gmail.com",
            "password": "sem_password",
        },
    )

    yield response.json["access_token"], response.json["refresh_token"]
