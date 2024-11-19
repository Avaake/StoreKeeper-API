from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from app.api.users.schemas import AuthCreateUser
from pydantic import ValidationError
from app.models import db, User
from app.core import settings
from app.core import logger

bp = Blueprint("user", __name__, url_prefix=settings.api_prefix.user)


@bp.route("", methods=["POST"])
def create_user():
    pass


@bp.route("", methods=["GET"])
def get_users():
    pass


@bp.route("<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    pass


@bp.route("<int:user_id>", methods=["PATCH"])
def update_user(user_id: int):
    pass


@bp.route("<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int):
    pass
