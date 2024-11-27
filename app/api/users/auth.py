from app.api.users.schemas import AuthCreateUser, UserRead
from werkzeug.security import check_password_hash
from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from datetime import timedelta
from app.api.users import crud
from app.core import settings
from app.core import logger

bp = Blueprint("auth", __name__, url_prefix=settings.api_prefix.auth)


@bp.route("/registration", methods=["POST"])
def register():
    try:
        data = AuthCreateUser.model_validate(request.json)
        user = crud.register_user(data)
        if isinstance(user, tuple):
            return user
        return (
            jsonify(
                {
                    "message": "User registered successfully",
                    "user": UserRead.model_validate(user).model_dump(),
                }
            ),
            201,
        )
    except ValidationError as err:
        logger.info({"error": "Validation error", "details": err.errors()})
        return jsonify({"error": "Validation error", "details": err.errors()}), 422
    except Exception as err:
        logger.error({"error": str(err)})
        return jsonify({"error": "Internal Server Error. Try again later"}), 500


@bp.route("/login", methods=["POST"])
def login():
    try:
        data = AuthCreateUser.model_validate(request.json)
        user = crud.get_user_by_email(data.email)
        if isinstance(user, tuple):
            return user
        if not check_password_hash(str(user.password_hash), data.password):
            logger.warning(
                f"Failed login attempt for email: {data.email} (incorrect password)"
            )
            return jsonify(error="Incorrect email or password!"), 422

        access_token = create_access_token(
            identity=user.email, expires_delta=timedelta(minutes=15)
        )
        refresh_token = create_refresh_token(identity=user.email)
        return jsonify(access_token=access_token, refresh_token=refresh_token)
    except ValidationError as err:
        logger.info(f"Validation info: {err.errors()}")
        return jsonify({"error": "Validation error", "details": err.errors()}), 422
    except Exception as err:
        logger.error({"error": str(err)})
        return jsonify({"error": "Internal Server Error. Try again later"}), 500


@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    try:
        current_user_email = get_jwt_identity()
        new_access_token = create_access_token(
            identity=current_user_email, expires_delta=timedelta(minutes=15)
        )

        return jsonify(access_token=new_access_token), 200
    except Exception as err:
        logger.error({"error": str(err)})
        return jsonify({"error": "Internal Server Error. Try again later"}), 500
