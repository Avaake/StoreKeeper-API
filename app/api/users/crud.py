from werkzeug.security import generate_password_hash

from app.api.users.schemas import UserUpdate
from app.models import db, User
from sqlalchemy.exc import IntegrityError
from flask import jsonify, Response
from app.core import logger


def create_user(
    username: str,
    email: str,
    password: str,
    role: str,
) -> User | tuple[Response, int]:
    try:
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role=role,
        )
        db.session.add(user)
        db.session.commit()
        logger.info(f"User {username}, {email} created")
        return user
    except IntegrityError as err:
        logger.error(f"Database error: {str(err)}")
        db.session.rollback()
        return jsonify({"error": "A user with this email already exists!"}), 422


def get_user(user_id: int) -> User | None:
    user = User.query.get(user_id)
    if user and user.role != "admin":
        return user
    return None


def get_users() -> list[User]:
    return User.query.filter(User.role != "admin").all()


def update_user(user_id: int, data: UserUpdate) -> User | None | tuple[Response, int]:
    try:
        user = get_user(user_id)
        if user is None:
            logger.info(f"User {user_id} not found")
            return jsonify({"error": "User not found!"}), 404

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        db.session.commit()
        return user

    except IntegrityError as err:
        db.session.rollback()
        logger.error(f"Database error: {str(err)}")
        return jsonify({"error": "Failed to update user data. Try again later"}), 400
    except Exception as err:
        db.session.rollback()
        logger.error(f"Error: {str(err)}")
        return jsonify({"error": "Failed to update user data. Try again later"}), 500


def delete_user(user_id: int) -> None | tuple[Response, int]:
    try:
        user = get_user(user_id)
        if user is None:
            logger.info(f"User {user_id} not found")
            return jsonify({"error": "User not found!"}), 404
        db.session.delete(user)
        db.session.commit()
    except IntegrityError as err:
        db.session.rollback()
        logger.error(f"Database error: {str(err)}")
        return jsonify({"error": "Failed to delete user data. Try again later"}), 400
