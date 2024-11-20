from flask import Flask
from app.core import settings


def create_app() -> Flask:
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = str(settings.db.url)
    app.config["TESTING"] = settings.testing
    app.config["JWT_SECRET_KEY"] = settings.jwt.secret_key

    from app.models import db
    from flask_migrate import Migrate
    from flask_jwt_extended import JWTManager

    db.init_app(app)
    Migrate(app=app, db=db)
    JWTManager(app=app)

    from app.api import api_bp

    app.register_blueprint(api_bp)
    # print(app.url_map)
    return app
