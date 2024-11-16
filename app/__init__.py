from flask import Flask
from app.core import settings


def create_app() -> Flask:
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = str(settings.db.url)
    app.config["TESTING"] = settings.testing
    app.config["JWT_SECRET_KEY"] = settings.jwt.secret_key

    from app.db import db
    from flask_migrate import Migrate

    db.init_app(app)
    Migrate(app=app, db=db.get_db())

    return app
