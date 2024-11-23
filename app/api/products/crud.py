from app.models import db, Product
from sqlalchemy.exc import IntegrityError
from flask import jsonify, Response


def get_product(product_id: int):
    return Product.query.get(product_id)
