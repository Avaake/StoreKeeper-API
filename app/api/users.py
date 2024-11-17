from flask import Blueprint, jsonify, request, Response
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.core import settings
from pydantic import ValidationError
from app.api.schemas import CreateUser
from sqlalchemy.exc import IntegrityError
from app.models import db, User
from app.core import logger

bp = Blueprint("users", __name__, url_prefix=settings.api_prefix.user_auth)


@bp.route("/registration", methods=["POST"])
def register():
    try:
        logger.info("Start registration process")
        data = CreateUser(**request.json)
        logger.info(f"User data validated: {data.dict()}")
    except ValidationError as err:
        logger.info(f"Validation info: {err.errors()}")
        return jsonify(err.errors()), 422

    try:
        user = User(
            username=data.username,
            email=data.email,
            password_hash=generate_password_hash(data.password),  # , method="pbkdf2"
        )
        db.session.add(user)
        db.session.commit()
        logger.info(f"User {user.username} created successfully.")
    except IntegrityError as err:
        db.session.rollback()
        logger.error(f"Integrity error: {err.params}")
        return jsonify("A user with this email already exists!"), 400

    logger.info(f"Registration successful for {data.email}")
    return jsonify(data.dict()), 201


@bp.route("/login", methods=["POST"])
def login():
    try:
        logger.info("Start login process")
        data = CreateUser(**request.json)
        logger.info(f"User data validated: {data.dict()}")
    except ValidationError as err:
        logger.info(f"Validation info: {err.errors()}")
        return jsonify(err.errors()), 422

    user = db.session.query(User).filter_by(email=data.email).first()
    if not user:
        logger.warning(f"Login attempt with non-existing email: {data.email}")
        return jsonify(error="Incorrect email or password!"), 401

    if not check_password_hash(user.password_hash, data.password):
        logger.warning(
            f"Failed login attempt for email: {data.email} (incorrect password)"
        )
        return jsonify(error="Incorrect email or password!"), 401

    access_token = create_access_token(identity=user.email)
    logger.info(f"Successful login for email: {data.email}")
    return jsonify(access_token=access_token)
