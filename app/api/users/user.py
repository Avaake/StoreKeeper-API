from flask import Blueprint, jsonify, request
from app.api.users import crud
from app.api.users.schemas import CreateUser, UserRead, UserUpdate
from pydantic import ValidationError
from app.core import settings
from app.core import logger
from flask_jwt_extended import jwt_required, current_user

bp = Blueprint("user", __name__, url_prefix=settings.api_prefix.users)


@bp.route("", methods=["POST"])
@jwt_required()
def create_user():
    try:
        data = CreateUser(**request.json)
        if current_user.role != "admin":
            return jsonify({"error": "Only admin can create user"}), 401
        user = crud.create_user(
            username=data.username,
            email=data.email,
            password=data.password,
            role=data.role,
        )

        if isinstance(user, tuple):
            return user

        return (
            jsonify(
                {
                    "success": True,
                    "user": {
                        "username": user.username,
                        "email": user.email,
                        "role": user.role,
                    },
                }
            ),
            201,
        )
    except ValidationError as err:
        logger.info({"error": "Validation error", "details": err.errors()})
        return jsonify({"error": "Validation error", "details": err.errors()}), 422


@bp.route("", methods=["GET"])
@jwt_required()
def get_users():
    if current_user.role != "admin":
        return jsonify({"error": "Only admin can create user"}), 401
    users = crud.get_users()
    users_data = [UserRead.model_validate(user).model_dump() for user in users]
    return jsonify({"users": users_data}), 200


@bp.route("<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id: int):

    if current_user.role == "admin":
        user = crud.get_user(user_id)
        if user is None:
            logger.info(f"User {user_id} not found")
            return jsonify({"error": "User not found"}), 404
        return jsonify({"user": UserRead.model_validate(user).model_dump()}), 200

    if current_user.id == user_id:
        user = crud.get_user(user_id)
        if user is None:
            logger.info(f"User {user_id} not found")
            return jsonify({"error": "User not found"}), 404
        return jsonify({"user": UserRead.model_validate(user).model_dump()}), 200

    return (
        jsonify({"message": "Access forbidden: you can only view your own data."}),
        403,
    )


@bp.route("<int:user_id>", methods=["PATCH"])
@jwt_required()
def update_user(user_id: int):
    try:

        data = UserUpdate(**request.json)
        if current_user.role != "admin":
            return jsonify({"error": "Only admin can update user"}), 401
        user = crud.update_user(user_id, data)
        if isinstance(user, tuple):
            return user
        return jsonify({"user": UserRead.model_validate(user).model_dump()}), 200

    except ValidationError as err:
        logger.info({"error": "Validation error", "details": err.errors()})
        return jsonify({"error": "Validation error", "details": err.errors()}), 422


@bp.route("<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id: int):
    user = crud.delete_user(user_id)
    if isinstance(user, tuple):
        return user
    return jsonify({"success": True}), 204
