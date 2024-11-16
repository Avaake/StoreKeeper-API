from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.core import settings

bp = Blueprint("users", __name__, url_prefix=settings.api_prefix.user_auth)


@bp.route("/registration", methods=["POST"])
def register():
    return jsonify("registration")


@bp.route("/login", methods=["POST"])
def login():
    return jsonify("login")
