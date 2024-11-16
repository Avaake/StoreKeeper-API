__all__ = [
    "api_bp",
]

from flask import Blueprint
from app.core import settings
from .users import bp as users_bp


api_bp = Blueprint("api", __name__, url_prefix=settings.api_prefix.api_v1_prefix)

api_bp.register_blueprint(users_bp)
