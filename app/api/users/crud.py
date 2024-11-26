from werkzeug.security import generate_password_hash

from app.api.users.schemas import UserUpdate, AuthCreateUser
from app.models import db, User
from sqlalchemy.exc import IntegrityError
from flask import jsonify, Response
from app.core import logger


# User
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
        return user
    except IntegrityError as err:
        logger.error(f"Database error: {str(err)}")
        db.session.rollback()
        return jsonify({"error": "A user with this email already exists!"}), 400
    except Exception as err:
        db.session.rollback()
        logger.error(f"Error: {str(err)}")


def get_user_by_id(user_id: int) -> User | None | tuple[Response, int]:
    try:
        user = User.query.get(user_id)
        if user and user.role != "admin":
            return user
        if user is None:
            return jsonify({"error": "User not found!"}), 404
        return None
    except Exception as err:
        logger.error(f"Error: {str(err)}")


def get_users() -> list[User]:
    try:
        return User.query.filter(User.role != "admin").all()
    except Exception as err:
        logger.error(f"Error: {str(err)}")


def update_user(user_id: int, data: UserUpdate) -> User | None | tuple[Response, int]:
    try:
        user = get_user_by_id(user_id)
        if isinstance(user, tuple):
            return user
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        db.session.commit()
        return user

    except IntegrityError as err:
        db.session.rollback()
        logger.error(f"Database error: {str(err)}")
    except Exception as err:
        db.session.rollback()
        logger.error(f"Error: {str(err)}")


def delete_user(user_id: int) -> None | tuple[Response, int]:
    try:
        user = get_user_by_id(user_id)
        if isinstance(user, tuple):
            return user
        db.session.delete(user)
        db.session.commit()
    except IntegrityError as err:
        db.session.rollback()
        logger.error(f"Database error: {str(err)}")
    except Exception as err:
        db.session.rollback()
        logger.error(f"Error: {str(err)}")


# Auth
def register_user(data: AuthCreateUser) -> User | tuple[Response, int]:
    try:
        user = User(
            username=data.username,
            email=data.email,
            password_hash=generate_password_hash(data.password),  # , method="pbkdf2"
        )
        db.session.add(user)
        db.session.commit()
        return user
    except IntegrityError as err:
        db.session.rollback()
        logger.error(f"Database error: {str(err)}")
        return jsonify("A user with this email already exists!"), 400
    except Exception as err:
        db.session.rollback()
        logger.error(f"Error: {str(err)}")


def get_user_by_email(email: str) -> User | tuple[Response, int]:
    try:
        user = User.query.filter_by(email=email).first()
        if user is None:
            logger.warning(f"Login attempt with non-existing email: {email}")
            return jsonify(error="Incorrect email or password!"), 401
        return user
    except Exception as err:
        db.session.rollback()
        logger.error(f"Error: {str(err)}")
