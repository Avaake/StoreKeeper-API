from flask import Blueprint, request, jsonify
from app.core import settings

bp = Blueprint("product", __name__, url_prefix=settings.api_prefix.product)


@bp.route("", methods=["POST"])
def create_product():
    pass


@bp.route("", methods=["GET"])
def get_products():
    pass


@bp.route("<int:product_id>", methods=["GET"])
def get_product(product_id):
    pass


@bp.route("<int:product_id>", methods=["PATCH"])
def update_product(product_id):
    pass


@bp.route("<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    pass
