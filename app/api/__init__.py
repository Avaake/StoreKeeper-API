__all__ = [
    "api_bp",
]


from flask import Blueprint
from app.core import settings
from .users.auth import bp as auth_bp
from .users.user import bp as user_bp
from .categories.category import bp as category_bp
from .products.product import bp as product_bp
from .orders.order import bp as order_bp
from .reports.report import bp as report_bp
from .suppliers.supplier import bp as supplier_bp

api_bp = Blueprint("api", __name__, url_prefix=settings.api_prefix.api_v1_prefix)

api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(user_bp)
api_bp.register_blueprint(category_bp)
api_bp.register_blueprint(product_bp)
api_bp.register_blueprint(order_bp)
api_bp.register_blueprint(report_bp)
api_bp.register_blueprint(supplier_bp)
